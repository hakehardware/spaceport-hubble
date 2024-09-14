from src.logger import logger
from src.utils import ContainerUtils
from src.api import API
import docker

class AssetMonitor:
    def __init__(self, containers, docker_client, stop_event, api_base_url) -> None:
        self.containers = containers
        self.docker_client = docker_client
        self.stop_event = stop_event
        self.api_base_url = api_base_url

    def upsert_container(self, container_data):
        API.upsert_container(container_data, self.api_base_url)

    def upsert_node(self, container_data):
        pass

    def upsert_farmer(self, container_data):
        pass

    def upsert_cluster_cache(self, container_data, nats_url):
        pass

    def upsert_cluster_controller(self, container_data, nats_url):
        pass

    def upsert_cluster_plotter(self, container_data, nats_url):
        pass

    def upsert_cluster_farmer(self, container_data, nats_url):
        pass

    def start(self) -> None:
        logger.info(f"Starting Asset Monitor for {len(self.containers)} contianers.")

        while not self.stop_event.is_set():

            for container in self.containers:

                try:
                    docker_container = self.docker_client.containers.get(container['container_id'])

                    container_data = {
                        'id': docker_container.id,
                        'type': container['container_type'],
                        'alias': container['container_alias'],
                        'status': docker_container.status.upper(),
                        'image': docker_container.image.tags[0],
                        'startedAt': ContainerUtils.normalize_date(docker_container.attrs.get('State').get('StartedAt')),
                        'ip': ContainerUtils.get_container_ip(docker_container)
                    }
                    self.upsert_container(container_data)

                    # if 'CLUSTER' in container_data['type']:
                    #     nats_url = ContainerUtils.get_nats_url(docker_container.attrs['Config']['Cmd'])

                    #     if 'PLOTTER' in container_data['type']: self.upsert_cluster_plotter(container_data, nats_url)

                    # if container_data['type'] == 'NODE': self.upsert_node()

                except docker.errors.NotFound:
                    logger.warning(f"Container with ID {container['container_id']} not found. Removing from monitoring list.")
                    self.containers.remove(container)
                    continue

                except Exception as e:
                    logger.error(f"Error in asset_monitor.py for {container['container_id']}", exc_info=e)


            self.stop_event.wait(30)
