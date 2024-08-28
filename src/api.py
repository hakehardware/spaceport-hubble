from src.logger import logger
import requests
import sys
import time

class API:
    @staticmethod
    def push(local_url, data):
        max_retries = 10
        retries = 0

        while True:
            try:
                response = requests.post(local_url, json=data)
                if response.status_code >= 300:
                    logger.info(data)
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
    def insert_container(container, api_base_url):
        local_url = f"{api_base_url}/insert/container"
        response = API.push(local_url, container)

    @staticmethod
    def insert_farmer(farmer, api_base_url):
        local_url = f"{api_base_url}/insert/farmer"
        response = API.push(local_url, farmer)

    @staticmethod
    def insert_farm(data, api_base_url):
        local_url = f"{api_base_url}/insert/farm"
        response = API.push(local_url, data)

    @staticmethod
    def insert_incomplete_sector(data, api_base_url):
        local_url = f"{api_base_url}/insert/incomplete_sector"
        response = API.push(local_url, data)

    @staticmethod
    def update_complete_sector(data, api_base_url):
        local_url = f"{api_base_url}/insert/complete_sector"
        response = API.push(local_url, data)


    @staticmethod
    def get_farm_with_public_key(public_key, api_base_url):
        local_url = f"{api_base_url}/get/farms?sort_column=farmer_id&farm_public_key={public_key}"
        response = requests.get(local_url)
        json_data = response.json()

        if response.status_code < 300:
            return json_data.get('data')
        else:
            logger.error(f"Error getting events {json_data.get('message')}")
            return None
        
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