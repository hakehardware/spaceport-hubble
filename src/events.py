from src.data_extraction import DataExtraction
from src.event_actions import EventActions

events = [
    {
        'event_name': 'NATs Connected',
        'event_description': 'Container has connected to NATs',
        'event_type': 'NATs',
        'event_pattern': r"^async_nats: event: connected$",
        'event_action': EventActions.action_nats_connected,
        'event_data_extraction': None
    },
    {
        'event_name': 'NATs Disconnected',
        'event_description': 'Container has disconnected from NATs',
        'event_type': 'NATs',
        'event_pattern': r"^async_nats: event: disconnected$",
        'event_action': None,
        'event_data_extraction': None
    },
    {
        'event_name': 'NATs IO Error',
        'event_description': 'There was an IO Error in NATs',
        'event_type': 'NATs',
        'event_pattern': r"^async_nats: event: client error: nats: IO error$",
        'event_action': None,
        'event_data_extraction': None
    },
    {
        'event_name': 'Shutting Down',
        'event_description': 'Container received SIGTERM, shutting down.',
        'event_type': 'Container',
        'event_pattern': r"^subspace_farmer::utils: Received SIGTERM, shutting down farmer...$",
        'event_action': None,
        'event_data_extraction': None
    },
    {
        'event_name': 'Cache Created',
        'event_description': 'Cache was created by the cluster cache container',
        'event_type': 'Cache',
        'event_pattern': r"Created cache cache_id=(?P<cache_id>\w+) max_num_elements=(?P<max_num_elements>\d+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_created_cache
    },
    {
        'event_name': 'Connecting to Node RPC',
        'event_description': 'A connection is being established with the Node RPC',
        'event_type': 'Controller',
        'event_pattern': r"Connecting to node RPC url=(?P<url>\S+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_node_rpc_url
    },
    {
        'event_name': 'Downloading segment headers from Node',
        'event_description': 'The segment headers are being downloaded from the Node',
        'event_type': 'Controller, Farmer',
        'event_pattern': r"Downloading all segment headers from node",
        'event_action': None,
        'event_data_extraction': None
    },
    {
        'event_name': 'Downloaded all segment headers from Node successfully',
        'event_description': 'All segment headers from the Node have been downloaded successfully',
        'event_type': 'Controller, Farmer',
        'event_pattern': r"Downloaded all segment headers from node successfully",
        'event_action': None,
        'event_data_extraction': None
    },
    {
        'event_name': 'DSN instance configured',
        'event_description': 'The DSN instance has been configured',
        'event_type': 'Controller',
        'event_pattern': r"DSN instance configured\. allow_non_global_addresses_in_dht=(?P<allow_non_global_addresses_in_dht>\w+) peer_id=(?P<peer_id>\w+) protocol_version=(?P<protocol_version>\S+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_dsn_configuration
    },
    {
        'event_name': 'Local peer ID established',
        'event_description': 'The local peer ID has been created',
        'event_type': 'Controller',
        'event_pattern': r"libp2p_swarm: local_peer_id=(?P<local_peer_id>\w+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_local_peer_id
    },
    {
        'event_name': 'DSN Listening',
        'event_description': 'The DSN is listening on specified address',
        'event_type': 'Controller',
        'event_pattern': r"DSN listening on (?P<dsn_listening_address>.+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_dsn_listening_address
    },
    {
        'event_name': 'New Cache discovered',
        'event_description': 'The controller has discovered a new cache',
        'event_type': 'Controller',
        'event_pattern': r"New cache discovered.*cache_id=(?P<cache_id>\w+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_cache_id
    },
    {
        'event_name': 'Initializing piece cache',
        'event_description': 'Initializing piece cache',
        'event_type': 'Controller',
        'event_pattern': r"Initializing piece cache",
        'event_action': None,
        'event_data_extraction': None
    },
    {
        'event_name': 'Synchronizing piece cache',
        'event_description': 'Synchronizing piece cache',
        'event_type': 'Controller',
        'event_pattern': r"Synchronizing piece cache",
        'event_action': None,
        'event_data_extraction': None
    },
    {
        'event_name': 'Newly discovered fram initializing',
        'event_description': 'A new farm has been discovered and is being initialized',
        'event_type': 'Controller',
        'event_pattern': r"Discovered new farm.*farm_index=(?P<farm_index>\d+)\s+farm_id=(?P<farm_id>\w+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_new_farm_initializing
    },
    {
        'event_name': 'Newly discovered farm initialized successfully',
        'event_description': 'A new farm has been initialized successfully',
        'event_type': 'Controller',
        'event_pattern': r"Farm initialized successfully.*farm_index=(?P<farm_index>\d+)\s+farm_id=(?P<farm_id>\w+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_new_farm_initialized
    },
    {
        'event_name': 'Piece cache syncing',
        'event_description': 'The piece cache is syncing',
        'event_type': 'Controller',
        'event_pattern': r"Piece cache sync\s+(?P<percentage>\d+\.\d+)%",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_piece_cache_sync_percent
    },
    {
        'event_name': 'Received invalid piece from peer',
        'event_description': 'Received invalid piece from peer',
        'event_type': 'Controller',
        'event_pattern': r"Received invalid piece from peer piece_index=(?P<piece_index>\d+)\s+source_peer_id=(?P<source_peer_id>\w+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_invalid_piece_from_peer
    },
    {
        'event_name': 'Finished piece cache synchronization',
        'event_description': 'Finished piece cache synchronization',
        'event_type': 'Controller',
        'event_pattern': r"Finished piece cache synchronization",
        'event_action': None,
        'event_data_extraction': None
    },
    {
        'event_name': 'Syncing piece cache to the latest history size',
        'event_description': 'Syncing piece cache to the latest history size',
        'event_type': 'Controller',
        'event_pattern': r"Syncing piece cache to the latest history size",
        'event_action': None,
        'event_data_extraction': None
    },
    {
        'event_name': 'Finished syncing piece cache to the latest history size',
        'event_description': 'Finished syncing piece cache to the latest history size',
        'event_type': 'Controller',
        'event_pattern': r"Finished syncing piece cache to the latest history size",
        'event_action': None,
        'event_data_extraction': None
    },
    {
        'event_name': 'Farm creation failed',
        'event_description': 'Farm creation failed',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Farm creation failed error=(?P<error>.+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_farm_creation_failed
    },
    {
        'event_name': 'Checking plot cache contents',
        'event_description': 'Checking plot cache contents',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Checking plot cache contents",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_check_plot_cache_contents
    },
    {
        'event_name': 'Finished checking plot cache contents',
        'event_description': 'Finished checking plot cache contents',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Finished checking plot cache contents",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_finished_check_plot_cache_contents
    },
    {
        'event_name': 'Benchmarking faster proving method',
        'event_description': 'Benchmarking faster proving method',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Benchmarking faster proving method",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_benchmarking_faster_proving
    },
    {
        'event_name': 'Benchmarking faster proving method',
        'event_description': 'Benchmarking faster proving method',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Faster proving method found fastest_mode=(?P<fastest_mode>\w+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_faster_proving_method_found
    },
    {
        'event_name': 'Identified Farm ID',
        'event_description': 'Identified Farm ID',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*ID:\s+(?P<ID>\w+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_identified_farm_id
    },
    {
        'event_name': 'Identified Genesis hash',
        'event_description': 'Identified Genesis hash',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Genesis hash:\s+(?P<genesis_hash>0x\w+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_identified_genesis_hash
    },
    {
        'event_name': 'Identified Public key',
        'event_description': 'Identified Public key',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Genesis hash:\s+(?P<genesis_hash>0x\w+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_identified_public_key
    },
    {
        'event_name': 'Identified Allocated space',
        'event_description': 'Identified Allocated space',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Allocated space:\s+(?P<allocated_space>\d+\.\d+\s+[TGM]iB)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_identified_allocated_space
    },
    {
        'event_name': 'Identified Farm Directory',
        'event_description': 'Identified Farm Directory',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Allocated space:\s+(?P<allocated_space>\d+\.\d+\s+[TGM]iB)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_identified_directory
    },
    {
        'event_name': 'Subscribing to archived segments',
        'event_description': 'Subscribing to archived segments',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Subscribing to archived segments",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_sub_archived_segments
    },
    {
        'event_name': 'Subscribing to slot info notifications',
        'event_description': 'Subscribing to slot info notifications',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Subscribing to slot info notifications",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_sub_slot_info_notifications
    },
    {
        'event_name': 'Subscribing to reward signing notifications',
        'event_description': 'Subscribing to reward signing notifications',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Subscribing to reward signing notifications",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_sub_reward_signing_notifications
    },
    {
        'event_name': 'Replotting sector',
        'event_description': 'Replotting sector',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}:\{sector_index=(?P<sector_index>\d+)\}.*Replotting sector \((?P<percent>\d+\.\d+)% complete\)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_replotting_sector
    },
    {
        'event_name': 'Plotting sector',
        'event_description': 'Plotting sector',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}:\{sector_index=(?P<sector_index>\d+)\}.*Plotting sector \((?P<percent>\d+\.\d+)% complete\)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_plotting_sector
    },
    {
        'event_name': 'Successfully signed reward hash',
        'event_description': 'Successfully signed reward hash',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Successfully signed reward hash (?P<reward_hash>0x\w+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_signed_reward_hash
    },
    {
        'event_name': 'Replotting complete',
        'event_description': 'Replotting complete',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Replotting complete",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_replotting_complete
    },
    {
        'event_name': 'Failed to send sector chunk',
        'event_description': 'Failed to send sector chunk',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}:\{sector_index=(?P<sector_index>\d+)\}.*Failed to send sector chunk error=(?P<error>.+)$",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_failed_to_send_sector_chunk
    },
    {
        'event_name': 'Initial plotting complete',
        'event_description': 'Initial plotting complete',
        'event_type': 'Farmer',
        'event_pattern': r"\{farm_index=(?P<farm_index>\d+)\}.*Initial plotting complete",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_initial_plotting_complete
    },
    {
        'event_name': 'Multiple L3 cache groups detected',
        'event_description': 'Multiple L3 cache groups detected',
        'event_type': 'Plotter',
        'event_pattern': r"Multiple L3 cache groups detected l3_cache_groups=(?P<l3_cache_groups>\d+)",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_multiple_cache_groups
    },
    {
        'event_name': 'Preparing plotting thread pools',
        'event_description': 'Preparing plotting thread pools',
        'event_type': 'Plotter',
        'event_pattern': r"plotting_thread_pool_core_indices=\[(.*?)\]",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_plotting_thread_pool_cores
    },
    {
        'event_name': 'Preparing replotting thread pools',
        'event_description': 'Preparing replotting thread pools',
        'event_type': 'Plotter',
        'event_pattern': r"replotting_thread_pool_core_indices=\[(.*?)\]",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_replotting_thread_pool_cores
    },
    {
        'event_name': 'Plot sector request',
        'event_description': 'Plot sector request',
        'event_type': 'Plotter',
        'event_pattern': r"\{public_key=(?P<public_key>\w+)\s+sector_index=(?P<sector_index>\d+)\}.*Plot sector request",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_plot_sector_request
    },
    {
        'event_name': 'Finished plotting sector successfully',
        'event_description': 'Finished plotting sector successfully',
        'event_type': 'Plotter',
        'event_pattern': r"\{public_key=(?P<public_key>\w+)\s+sector_index=(?P<sector_index>\d+)\}.*Finished plotting sector successfully",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_finished_plot_sector_request
    },
    {
        'event_name': 'Acknowledgement wait timed out for plot sector request',
        'event_description': 'Acknowledgement wait timed out for plot sector request. Is controller/NATs offline?',
        'event_type': 'Plotter',
        'event_pattern': r"\{public_key=(?P<public_key>\w+)\s+sector_index=(?P<sector_index>\d+)\}.*Acknowledgement wait timed out",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_acknowledgement_wait_timed_out
    },
    {
        'event_name': 'Response sending ended early',
        'event_description': 'Response sending ended early. Is controller/NATs offline?',
        'event_type': 'Plotter',
        'event_pattern': r"\{public_key=(?P<public_key>\w+)\s+sector_index=(?P<sector_index>\d+)\}.*Response sending ended early",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_acknowledgement_wait_timed_out
    },
    {
        'event_name': 'Failed to send progress update',
        'event_description': 'Failed to send progress update. Is controller/NATs offline?',
        'event_type': 'Plotter',
        'event_pattern': r"\{public_key=(?P<public_key>\w+)\s+sector_index=(?P<sector_index>\d+)\}.*Failed to send progress update error=(?P<error>.+)$",
        'event_action': None,
        'event_data_extraction': DataExtraction.extract_failed_to_send_progress
    },
]