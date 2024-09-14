import docker
import threading
import sys
from datetime import datetime

from src.logger import logger
from src.log_parser import LogParser
from src.asset_monitor import AssetMonitor
from src.api import API

class EventManager:
    def __init__(self, config) -> None:
        self.host_ip = config['host_ip']
        self.api_base_url = config['api_base_url']
        self.docker_client = docker.from_env()
        self.stop_event = threading.Event()
        self.containers = []

    def normalize_date(self, date_str):
        # Truncate the fractional seconds to 6 digits
        truncated_date_str = date_str[:26] + 'Z'
        # Parse the input date string
        dt = datetime.strptime(truncated_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Return the formatted date string
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_container_ip(self, container):
        try:
            # Get the network mode of the container
            network_mode = container.attrs.get('HostConfig', {}).get('NetworkMode', '')
            
            # Get the IP address based on the network mode
            container_ip = container.attrs.get('NetworkSettings', {}).get('Networks', {}).get(network_mode, {}).get('IPAddress', '')
            
            # If IP address is not found using the network mode, search through the networks
            if not container_ip:
                networks = container.attrs.get('NetworkSettings', {}).get('Networks', {})
                for network_name, network_data in networks.items():
                    if network_data.get('NetworkID') == network_mode:
                        container_ip = network_data.get('IPAddress', '')
                        break

            return container_ip
        except Exception as e:
            print(f"Error getting container IP: {e}")
            return None
        
    def get_nats_url(self, command):
        if not command:
            return 0
        
        for c in command:
            if 'nats://' in c:
                return c
            
        return None
    
    def get_container_type(self, command):
        if 'cache' in command and 'cluster' in command:
            container_type = 'CLUSTER_CACHE'
        elif 'controller' in command and 'cluster' in command:
            container_type = 'CLUSTER_CONTROLLER'
        elif 'farmer' in command and 'cluster' in command:
            container_type = 'CLUSTER_FARMER'
        elif 'plotter' in command and 'cluster' in command:
            container_type = 'CLUSTER_PLOTTER'
        else:
            container_type = 'FARMER'

        return container_type

    def get_containers(self):
        try:
            containers = self.docker_client.containers.list(all=True)
            for container in containers:

                container_label = container.attrs['Config']['Labels'].get('com.spaceport.name')
                image = container.image.tags[0]

                if 'ghcr.io/autonomys/node' in image or 'autonomys_node' in image:
                    self.containers.append({
                        'container_id': container.id,
                        'container_type': 'NODE',
                        'container_alias': container_label if container_label else container.name
                    })

                elif 'ghcr.io/autonomys/farmer' in image or 'autonomys_farmer' in image:
                    self.containers.append({
                        'container_id': container.id,
                        'container_type': self.get_container_type(container.attrs['Config']['Cmd']),
                        'container_alias': container_label if container_label else container.name
                    })

                elif 'nats' in image:
                    self.containers.append({
                        'container_id': container.id,
                        'container_type': 'NATS',
                        'container_alias': container_label if container_label else container.name
                    })

            if len(self.containers) == 0:
                logger.error('No containers found. Are you sure they are running?')
                sys.exit(1)

        except Exception as e:
            logger.error(f'Error getting container:', exc_info=e)
            sys.exit(1)

    def launch_parser_thread(self, container):
        LogParser(container, self.docker_client, self.stop_event, self.api_base_url).start()

    def launch_asset_thread(self):
        AssetMonitor(self.containers, self.docker_client, self.stop_event, self.api_base_url).start()

    def run(self):
        try:
            self.get_containers()

            threads = []

            for container in self.containers:
                thread = threading.Thread(
                    target=self.launch_parser_thread,
                    args=(container,)
                )
                threads.append(thread)
                thread.start()

            # Launch a thread here for AssetMonitor() and pass self.containers
            asset_monitor_thread = threading.Thread(
                target=self.launch_asset_thread
            )
            threads.append(asset_monitor_thread)
            asset_monitor_thread.start()

            for thread in threads:
                thread.join()

        except KeyboardInterrupt:
            print("Stop signal received. Gracefully shutting down monitors.")
            self.stop_event.set()  # Ensure the stop event is set