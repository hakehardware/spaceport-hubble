import argparse
from src.logger import logger
from src.event_manager import EventManager

def main():
    parser = argparse.ArgumentParser(description='Spaceport - Event Manager')

    parser.add_argument('--host_ip', type=str, required=True, help='Host IP')
    parser.add_argument('--api_base_url', type=str, required=True, help='API Base URL')

    args = parser.parse_args()

    config = {
        'host_ip': args.host_ip,
        'api_base_url': args.api_base_url
    }

    logger.info(f"Got Config: {config}")

    EventManager(config).run()

if __name__ == "__main__":
    main()