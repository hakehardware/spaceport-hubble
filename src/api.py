from src.logger import logger
import requests
import sys
import time

class API:
    @staticmethod
    def push(local_url, event):
        max_retries = 10
        retries = 0

        while True:
            try:
                response = requests.post(local_url, json=event)
                if response.status_code >= 300:
                    logger.info(event)
                    logger.error(response.json())
                    time.sleep(10)
                    
                return response

            except Exception as e:
                if retries == max_retries:
                    logger.error('Max retries reached. Exiting...')
                    sys.exit(1)
                retries+=1
                logger.error(f"Retries: {retries}, Max allowed: {max_retries}", exc_info=e)
                time.sleep(1)

    @staticmethod
    def insert_event(event, api_base_url):
        local_url = f"{api_base_url}/insert/event"
        response = API.push(local_url, event)

    @staticmethod
    def get_last_event_for_container_id(container_id, api_base_url):
        local_url = f"{api_base_url}/get/events?sort_column=event_datetime&event_container_id={container_id}&limit=1"
        response = requests.get(local_url)
        json_data = response.json()

        if response.status_code < 300:
            return json_data.get('data')
        else:
            logger.error(f"Error getting events {json_data.get('message')}")
            return None