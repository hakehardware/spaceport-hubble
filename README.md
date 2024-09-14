## Spaceport - Hubble
Hubble scrapes Autonomys container logs and pushes them to Cosmos.

### Installation
The best way to install Hubble is to use the dockerhub image:

[Hubble](https://hub.docker.com/r/hakehardware/spaceport-hubble)

More indepth instructions which include installation of Cosmos can be found on my Substack here:
[Spaceport Guide](https://hakedev.substack.com/p/spaceport-guide)


#### Abbreviated Instructions
In Portainer, or via docker-compose deploy:
```yml
services:
  hubble:
    container_name: spaceport-hubble
    image: hakehardware/spaceport-hubble:0.0.2-hotfix2
    restart: unless-stopped
    environment:
      - TZ=America/Phoenix
    command: ["python", "main.py", "--api_base_url", "http://192.168.69.12:9955"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    network_mode: host
```

Make sure to update the api_base_url with whatever URL Cosmos is deployed at. Also update the version to the latest available.

Hubble should only be deployed after Cosmos as it will immediately begin sending events to the API.

#### Container Metadata
Hubble scrapes container metadata, and it's recommended to label your Autonomys containers to give them an Alias for easy readability on Cosmos. For instance, in this docker-compose you can see a label is provided. This will get picked up by Hubble:

```yml
  farmer_controller:
    container_name: autonomys_controller
    image: ghcr.io/autonomys/farmer:gemini-3h-2024-jul-29
    volumes:
      - /home/hakehardware/autonomys_cluster/controller:/controller
    command:
      [
        "cluster",
        "--nats-server", "nats://172.25.0.102:4222",
        "controller",
        "--base-path", "/controller",
        "--node-rpc-url", "ws://172.25.0.101:9944"
      ]
    labels:
      com.spaceport.name: "Terminator Controller"
    environment:
      - TZ=America/Phoenix
    networks:
      autonomys-network:
        ipv4_address: 172.25.0.103
```

In Hubble this container will have the label "Terminator Controller" instead of the container_name of "autonomys_controller". This is more human readable and is recommended. Note that you must use the label "com.spaceport.name"

### Advanced

#### Build your own image
If you wish to build the image yourself locally, a dockerfile is included for this purpose.  With docker installed run:

```bash
git clone https://github.com/hakehardware/spaceport-hubble.git
cd spaceport-hubble
docker build -t custom-hubble-build .
```

Now in Portainer, or your docker-compose, you could reference the image as "custom-hubble-build". 

#### Custom Autonomys images
If you build your own Autonomys images you will need to either update the image names that hubble looks for (in event_manager.py) or make sure to build your images to be either:
1. autonomys_node for your Node
1. autonomys_farmer for your Farmer

The script is already programmed to look for images that contain that string, so if your image is named one of those it will pick it up.