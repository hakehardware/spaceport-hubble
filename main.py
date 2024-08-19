import argparse
from src.logger import logger
from src.event_manager import EventManager

def main():
    parser = argparse.ArgumentParser(description='Spaceport - Event Manager')

    parser.add_argument('--host_ip', type=str, required=True, help='Host IP')
    parser.add_argument('--chronicle_ip', type=str, required=True, help='Chronicle IP')

    args = parser.parse_args()

    config = {
        'host_ip': args.host_ip,
        'chronicle_ip': args.chronicle_ip
    }

    logger.info(f"Got Config: {config}")

    EventManager(config).run()

if __name__ == "__main__":
    main()