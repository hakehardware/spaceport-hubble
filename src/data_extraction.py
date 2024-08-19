import re

class Helpers:
    @staticmethod
    def extract_cpu_sets(text):
        cpu_sets = re.findall(r'CpuSet\((.*?)\)', text)
        split_values = []
        for cpu_set in cpu_sets:
            split_values.extend(cpu_set.split(','))
        return split_values  

class DataExtraction:
    @staticmethod
    def extract_created_cache(match):
        return {
            'cache_id': match.group('cache_id'),
            'max_num_elements': match.group('max_num_elements')
        }
    
    @staticmethod
    def extract_node_rpc_url(match):
        return {
            'node_rpc_url': match.group('url')
        }
    
    @staticmethod
    def extract_dsn_configuration(match):
        return {
            'allow_non_global_addresses_in_dht': match.group('allow_non_global_addresses_in_dht'),
            'peer_id': match.group('peer_id'),
            'protocol_version': match.group('protocol_version')
        }
    
    @staticmethod
    def extract_local_peer_id(match):
        return {
            'local_peer_id': match.group('local_peer_id')
        }
    
    @staticmethod
    def extract_dsn_listening_address(match):
        return {
            'dsn_address': match.group('dsn_listening_address')
        }
    
    @staticmethod
    def extract_cache_id(match):
        return {
            'cache_id': match.group('cache_id')
        }
    
    @staticmethod
    def extract_new_farm_initializing(match):
        return {
            'farm_index': match.group('farm_index'),
            'farm_id': match.group('farm_id')
        }
    
    @staticmethod
    def extract_new_farm_initialized(match):
        return {
            'farm_index': match.group('farm_index'),
            'farm_id': match.group('farm_id')
        }
    
    @staticmethod
    def extract_piece_cache_sync_percent(match):
        return {
            'piece_cache_sync_percent': match.group('percentage')
        }
    
    @staticmethod
    def extract_invalid_piece_from_peer(match):
        return {
            'piece_index': match.group('piece_index'),
            'source_peer_id': match.group('source_peer_id')
        }
    
    # Cluster Farmer
    @staticmethod
    def extract_farm_creation_failed(match):
        return {
            'farm_index': match.group('farm_index'),
            'error': match.group('error')
        }
    
    @staticmethod
    def extract_check_plot_cache_contents(match):
        return {
            'farm_index': match.group('farm_index')
        }
    
    @staticmethod
    def extract_finished_check_plot_cache_contents(match):
        return {
            'farm_index': match.group('farm_index')
        }
    
    @staticmethod
    def extract_benchmarking_faster_proving(match):
        return {
            'farm_index': match.group('farm_index')
        }
    
    @staticmethod
    def extract_faster_proving_method_found(match):
        return {
            'farm_index': match.group('farm_index'),
            'fastest_mode': match.group('fastest_mode')
        }
    
    @staticmethod
    def extract_identified_farm_id(match):
        return {
            'farm_id': match.group('ID'),
            'farm_index': match.group('farm_index')
        }
    
    @staticmethod
    def extract_identified_genesis_hash(match):
        return {
            'genesis_hash': match.group('genesis_hash'),
            'farm_index': match.group('farm_index')
        }
    
    @staticmethod
    def extract_identified_public_key(match):
        return {
            'genesis_hash': match.group('genesis_hash'),
            'farm_index': match.group('farm_index')
        }
    
    @staticmethod
    def extract_identified_allocated_space(match):
        return {
            'farm_index': match.group('farm_index'),
            'allocated_space': match.group('allocated_space')
        }
    
    @staticmethod
    def extract_identified_directory(match):
        return {
            'farm_index': match.group('farm_index'),
            'directory': match.group('directory')
        }
    
    @staticmethod
    def extract_sub_archived_segments(match):
        return {
            'farm_index': match.group('farm_index')
        }
    
    @staticmethod
    def extract_sub_slot_info_notifications(match):
        return {
            'farm_index': match.group('farm_index')
        }
    
    @staticmethod
    def extract_sub_reward_signing_notifications(match):
        return {
            'farm_index': match.group('farm_index')
        }
    
    @staticmethod
    def extract_replotting_sector(match):
        return {
            'farm_index': match.group('farm_index'),
            'sector_index': match.group('sector_index'),
            'farm_index': match.group('percent'),
        }
    
    @staticmethod
    def extract_plotting_sector(match):
        return {
            'farm_index': match.group('farm_index'),
            'sector_index': match.group('sector_index'),
            'percent': match.group('percent'),
        }
    
    @staticmethod
    def extract_signed_reward_hash(match):
        return {
            'farm_index': match.group('farm_index'),
            'reward_hash': match.group('reward_hash')
        }
    
    @staticmethod
    def extract_replotting_complete(match):
        return {
            'farm_index': match.group('farm_index')
        }
    
    @staticmethod
    def extract_failed_to_send_sector_chunk(match):
        return {
            'farm_index': match.group('farm_index'),
            'sector_index': match.group('sector_index'),
            'error': match.group('error')
        }
    
    @staticmethod
    def extract_initial_plotting_complete(match):
        return {
            'farm_index': match.group('farm_index')
        }
    
    # Plotter
    @staticmethod
    def extract_multiple_cache_groups(match):
        return {
            'l3_cache_groups': match.group('l3_cache_groups')
        }
    
    @staticmethod
    def extract_plotting_thread_pool_cores(match):
        plotting_cores = Helpers.extract_cpu_sets(match.group(1))
        return {
            'plotting_cores': plotting_cores
        }
    
    @staticmethod
    def extract_replotting_thread_pool_cores(match):
        replotting_cores = Helpers.extract_cpu_sets(match.group(1))
        return {
            'replotting_cores': replotting_cores
        }
    
    @staticmethod
    def extract_plot_sector_request(match):
        return {
            'public_key': match.group('public_key'),
            'sector_index': match.group('sector_index')
        }
    
    @staticmethod
    def extract_finished_plot_sector_request(match):
        return {
            'public_key': match.group('public_key'),
            'sector_index': match.group('sector_index')
        }
    
    @staticmethod
    def extract_acknowledgement_wait_timed_out(match):
        return {
            'public_key': match.group('public_key'),
            'sector_index': match.group('sector_index')
        }
    
    @staticmethod
    def extract_response_sending_ended_early(match):
        return {
            'public_key': match.group('public_key'),
            'sector_index': match.group('sector_index')
        }
    
    @staticmethod
    def extract_failed_to_send_progress(match):
        return {
            'public_key': match.group('public_key'),
            'sector_index': match.group('sector_index'),
            'error': match.group('error')
        }
    