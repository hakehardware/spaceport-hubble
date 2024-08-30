import sys
import re

from src.logger import logger
from datetime import datetime, timezone
from src.events import events
from src.api import API

class LogParser:
    def __init__(self, container, docker_client, stop_event, api_base_url) -> None:
        self.container_id = container['container_id']
        self.container_alias = container['container_alias']
        self.container_type = container['container_type']
        self.docker_client = docker_client
        self.stop_event = stop_event
        self.api_base_url = api_base_url
        self.container = None

    def upsert_farmer(self, container):
        command = container.attrs['Config']['Cmd']

        reward_address = None
        reward_address_index = command.index('--reward-address')
        if not reward_address_index:
            logger.warn('Unable to extract reward address.')
        else:
            reward_address = command[reward_address_index + 1]

        farmer = {
            'farmer_id': self.container_alias,
            'container_id': self.container_id,
            'farmer_reward_address': reward_address,
            'farmer_status': 1
        }

        # API.insert_farmer(farmer, self.api_base_url)

    def normalize_date(self, date_str):
        # Truncate the fractional seconds to 6 digits
        truncated_date_str = date_str[:26] + 'Z'

        # Parse the input date string
        dt = datetime.strptime(truncated_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Return the formatted date string
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    def normalize_log(self, log_str):
        try:
            log_pattern = re.compile(
                r'(?P<datetime>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)\s+(?P<level>\w+)\s+(?P<data>.+)'
            )
            match = log_pattern.match(log_str)
            
            if match:
                return {
                    'event_datetime': match.group("datetime"),
                    'event_level': match.group("level"),
                    'event_data': match.group("data")
                }
            
            else:
                return None
            
        except Exception as e:
            logger.error(f"Error normalizing log:", exc_info=e)

    def parse_event(self, normalized_log):
        try:
            for e in events:
                match = re.search(e['event_pattern'], normalized_log['event_data'])
                if match:

                    event = {
                        'name': e['event_name'],
                        'type': e['event_type'],
                        'level': normalized_log['event_level'],
                        'containerAlias': self.container_alias,
                        'containerId': self.container_id,
                        'containerType': self.container_type,
                        'data': e['event_data_extraction'](match) if e['event_data_extraction'] else {},
                        'eventTime': normalized_log['event_datetime']
                    }

                    # if e['event_action']: e['event_action'](event, self.api_base_url)

                    return event
                
            return None

        except Exception as e:
            logger.error(f"Error parsing event from normalized log:", exc_info=e)
            logger.error(normalized_log)

    def start(self):
        logger.info(f"Starting Stream Parser for {self.container_alias} of type {self.container_type}.")

        container = self.docker_client.containers.get(self.container_id)
        if not container:
            logger.error(f"Unable to get container for container id: {self.container_id}")
            sys.exit(1)

        if self.container_type == 'cluster_farmer': self.upsert_farmer(container)

        while not self.stop_event.is_set():
            try:
                container.reload()  

                if container.status != 'running':
                    logger.warn(f"Container must be running, current status: {container.status}")
                    self.stop_event.wait(30)
                    continue
                
                last_event = API.get_last_event_for_container_id(self.container_id, self.api_base_url)

                if len(last_event) > 0:
                    event_time_str = last_event[0].get('eventTime')
                    logger.info(f"Getting Logs Since: {event_time_str} for {self.container_id}")
                    start = datetime.fromisoformat(event_time_str.replace('Z', '+00:00'))
                else:
                    start = datetime.min.replace(tzinfo=timezone.utc)

                generator = container.logs(since=start, stdout=True, stderr=True, stream=True)
                for log in generator:
                    try:
                        if self.stop_event.is_set():
                            break

                        # Convert raw log into a normalized log
                        normalized_log = self.normalize_log(log.decode('utf-8').strip())
                        if not normalized_log:
                            continue

                        # Parse normalized log into an event
                        event = self.parse_event(normalized_log)
                        if not event:
                            continue

                        # Insert event into db
                        API.insert_event(event, self.api_base_url)

                    except Exception as e:
                        logger.error(f"Error in generator for {self.container_alias}:", exc_info=e)

            except Exception as e:
                logger.error(f"Error in monitor_stream for {self.container_alias}", exc_info=e)
                self.stop_event.wait(30)
