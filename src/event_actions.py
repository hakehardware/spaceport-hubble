from src.api import API
from src.logger import logger

class EventActions:
    @staticmethod
    def action_faster_proving_method_found(event, api_base_url):
        # Insert Farm
        API.insert_farm({
            'farmer_id': event['event_container_alias'],
            'farm_index': event['event_data']['farm_index'],
            'farm_fastest_mode': event['event_data']['fastest_mode']
        }, api_base_url)

    @staticmethod
    def action_identified_farm_id(event, api_base_url):
        API.insert_farm({
            'farmer_id': event['event_container_alias'],
            'farm_index': event['event_data']['farm_index'],
            'farm_id': event['event_data']['farm_id']
        }, api_base_url)

    @staticmethod
    def action_identified_genesis_hash(event, api_base_url):
        API.insert_farm({
            'farmer_id': event['event_container_alias'],
            'farm_index': event['event_data']['farm_index'],
            'farm_genesis_hash': event['event_data']['genesis_hash']
        }, api_base_url)

    @staticmethod
    def action_identified_public_key(event, api_base_url):
        API.insert_farm({
            'farmer_id': event['event_container_alias'],
            'farm_index': event['event_data']['farm_index'],
            'farm_public_key': event['event_data']['public_key']
        }, api_base_url)

    @staticmethod
    def action_identified_allocated_space(event, api_base_url):
        API.insert_farm({
            'farmer_id': event['event_container_alias'],
            'farm_index': event['event_data']['farm_index'],
            'farm_size': event['event_data']['allocated_space']
        }, api_base_url)

    @staticmethod
    def action_identified_farm_directory(event, api_base_url):
        API.insert_farm({
            'farmer_id': event['event_container_alias'],
            'farm_index': event['event_data']['farm_index'],
            'farm_directory': event['event_data']['directory']
        }, api_base_url)

    @staticmethod
    def action_replotting_sector(event, api_base_url):
        API.insert_farm({
            'farmer_id': event['event_container_alias'],
            'farm_index': event['event_data']['farm_index'],
            'farm_latest_sector': event['event_data']['sector_index'],
            'farm_plot_progress': event['event_data']['percent'],
            'farm_initial_plot_complete': 1
        }, api_base_url)

    @staticmethod
    def action_plotting_sector(event, api_base_url):
        API.insert_farm({
            'farmer_id': event['event_container_alias'],
            'farm_index': event['event_data']['farm_index'],
            'farm_latest_sector': event['event_data']['sector_index'],
            'farm_plot_progress': event['event_data']['percent'],
            'farm_initial_plot_complete': 0
        }, api_base_url)

    @staticmethod
    def action_replotting_complete(event, api_base_url):
        API.insert_farm({
            'farmer_id': event['event_container_alias'],
            'farm_index': event['event_data']['farm_index'],
            'farm_plot_progress': 100,
            'farm_initial_plot_complete': 1
        }, api_base_url)

    @staticmethod
    def action_initial_plotting_complete(event, api_base_url):
        API.insert_farm({
            'farmer_id': event['event_container_alias'],
            'farm_index': event['event_data']['farm_index'],
            'farm_plot_progress': 100,
            'farm_initial_plot_complete': 1
        }, api_base_url)

    @staticmethod
    def action_plot_sector_request(event, api_base_url):
        # API.insert_incomplete_sector({
        #     'plotter_id': event['event_container_alias'],
        #     'sector_index': event['event_data']['sector_index'],
        #     'public_key': event['event_data']['public_key'],
        #     'complete': 0,
        #     'event_datetime': event['event_datetime']
        # }, api_base_url)
        pass

    @staticmethod
    def action_finished_plot_sector_request(event, api_base_url):
        # This needs to be updated so that sectors are deleted when completed
        # and only sectors actively being plotted exist
        # Then there will be a separate table that manages recording of sector plots

        # API.update_complete_sector({
        #     'plotter_id': event['event_container_alias'],
        #     'sector_index': event['event_data']['sector_index'],
        #     'public_key': event['event_data']['public_key'],
        #     'complete': 1,
        #     'event_datetime': event['event_datetime']
        # }, api_base_url)
        pass
    
