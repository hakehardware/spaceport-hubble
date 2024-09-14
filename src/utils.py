from datetime import datetime

class ContainerUtils:
    @staticmethod
    def normalize_date(date_str):
        # Truncate the fractional seconds to 6 digits
        truncated_date_str = date_str[:26] + 'Z'
        # Parse the input date string
        dt = datetime.strptime(truncated_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Return the formatted date string
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def get_container_type(command):
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
    
    @staticmethod
    def get_nats_url(command):
        if not command:
            return 0
        
        for c in command:
            if 'nats://' in c:
                return c
            
        return None
    
    @staticmethod
    def get_container_ip(container):
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
    
    @staticmethod
    def get_container_data(container):
        return True