from src.logger import logger
import requests
import sys
import time

class API:
    @staticmethod
    def insert_event(event, api_base_url):
        local_url = f"{api_base_url}/api/events"
        try:
            logger.info(f"Inserting Event @ {local_url} for event {event['name']}")
            response = requests.post(local_url, json=event)

            if response.status_code >= 300:
                logger.error(response.text)

        except Exception as e:
            logger.error(f"Error:", exc_info=e)

    def upsert_container(container, api_base_url):
        local_url = f"{api_base_url}/api/containers"
        try:
            logger.info(f"Upserting container @ {local_url} with alias {container['alias']}")
            response = requests.post(local_url, json=container)
            if response.status_code >= 300:
                logger.error(response.text)

        except Exception as e:
            logger.error(f"Error:", exc_info=e)

    @staticmethod
    def get_last_event_for_container_id(container_id, api_base_url):
        local_url = f"{api_base_url}/api/events?containerId={container_id}&take=1"

        logger.info(f"Getting Last Container Event @ {local_url}")
        response = requests.get(local_url)

        if response.status_code < 300:
            return response.json()
        else:
            logger.error(f"Error getting events {response.json().get('message')}")
            return None