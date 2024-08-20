import docker
import threading
import sys

from src.logger import logger
from src.log_parser import LogParser

class EventManager:
    def __init__(self, config) -> None:
        self.host_ip = config['host_ip']
        self.api_base_url = config['api_base_url']
        self.docker_client = docker.from_env()
        self.stop_event = threading.Event()
        self.containers = []

    def get_container_type(self, command):
        if 'cache' in command and 'cluster' in command:
            container_type = 'cluster_cache'
        elif 'controller' in command and 'cluster' in command:
            container_type = 'cluster_controller'
        elif 'farmer' in command and 'cluster' in command:
            container_type = 'cluster_farmer'
        elif 'plotter' in command and 'cluster' in command:
            container_type = 'cluster_plotter'
        else:
            container_type = 'farmer'

        return container_type

    def get_containers(self):
        try:
            containers = self.docker_client.containers.list(all=True)
            for container in containers:
                container_label = container.attrs['Config']['Labels'].get('com.spaceport.name')
                logger.info(container.image.tags[0])

                if 'ghcr.io/autonomys/node' in container.image.tags[0]:
                    self.containers.append({
                        'container_type': 'node',
                        'container_id': container.id,
                        'container_alias': container_label if container_label else container.name
                    })

                elif 'ghcr.io/autonomys/farmer' in container.image.tags[0]:
                    self.containers.append({
                        'container_type': self.get_container_type(container.attrs['Config']['Cmd']),
                        'container_id': container.id,
                        'container_alias': container_label if container_label else container.name
                    })

                elif 'nats' in container.image.tags[0]:
                    self.containers.append({
                        'container_type': 'nats',
                        'container_id': container.id,
                        'container_alias': container_label if container_label else container.name
                    })

            if len(self.containers) == 0:
                logger.error('No containers found. Are you sure they are running?')
                sys.exit(1)

            for container in self.containers:
                logger.info(container)

        except Exception as e:
            logger.error(f'Error getting container:', exc_info=e)
            sys.exit(1)

    def launch_thread(self, container):
        LogParser(container, self.docker_client, self.stop_event, self.api_base_url).start()

    def run(self):
        try:
            self.get_containers()

            threads = []

            for container in self.containers:
                thread = threading.Thread(
                    target=self.launch_thread,
                    args=(container,)
                )
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        except KeyboardInterrupt:
            print("Stop signal received. Gracefully shutting down monitors.")
            self.stop_event.set()  # Ensure the stop event is set



