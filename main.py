import argparse
from src.logger import logger
from src.event_manager import EventManager
import socket

def main():
    parser = argparse.ArgumentParser(description='Spaceport - Hubble')
    parser.add_argument('--api_base_url', type=str, required=True, help='API Base URL')
    args = parser.parse_args()

    config = {
        'host_ip': None,
        'api_base_url': args.api_base_url
    }

    # Connect to an external IP to get the local IP address (host IP in host network mode)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        config['host_ip'] = s.getsockname()[0]

    except Exception as e:
        logger.error(f"Error getting host_ip, it will be set to None", exc_info=e)
    
    finally:
        s.close()

    logger.info(f"Got Config: {config}")

    EventManager(config).run()

if __name__ == "__main__":
    main()