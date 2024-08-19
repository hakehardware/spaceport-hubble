import sys
import re

from src.logger import logger
from datetime import datetime, timezone
from src.events import events

class LogParser:
    def __init__(self, container, docker_client, stop_event, chronicle_ip) -> None:
        self.container_id = container['container_id']
        self.container_alias = container['container_alias']
        self.container_type = container['container_type']
        self.docker_client = docker_client
        self.stop_event = stop_event
        self.chronicle_ip = chronicle_ip
        self.container = None

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
                    'event_datetime': self.normalize_date(match.group("datetime")),
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

                    return {
                        'event_name': e['event_name'],
                        'event_type': e['event_type'],
                        'event_level': normalized_log['event_level'],
                        'event_datetime': normalized_log['event_datetime'],
                        'event_container_id': self.container_id,
                        'event_container_alias': self.container_alias,
                        'event_container_type': self.container_type,
                        'event_data': e['event_data_extraction'](match) if e['event_data_extraction'] else None
                    }
                
            return None

        except Exception as e:
            logger.error(f"Error parsing event from normalized log:", exc_info=e)

    def start(self):
        logger.info(f"Starting Stream Parser for {self.container_alias} of type {self.container_type}.")

        container = self.docker_client.containers.get(self.container_id)
        if not container:
            logger.error(f"Unable to get container for container id: {self.container_id}")
            sys.exit(1)

        while not self.stop_event.is_set():
            try:
                container.reload()  

                if container.status != 'running':
                    logger.warn(f"Container must be running, current status: {container.status}")
                    self.stop_event.wait(30)
                    continue

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

                        logger.info(event)

                    except Exception as e:
                        logger.error(f"Error in generator for {self.container_alias}:", exc_info=e)

            except Exception as e:
                logger.error(f"Error in monitor_stream for {self.container_alias}", exc_info=e)
                self.stop_event.wait(30)
