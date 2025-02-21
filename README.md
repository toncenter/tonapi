![splash_http_api](https://user-images.githubusercontent.com/1449561/154847286-989a6c51-1615-45e1-b40f-aec7c13014fa.png)

# HTTP API for [The Open Network](https://ton.org)

[![PyPI](https://img.shields.io/pypi/v/ton-http-api?color=blue)](https://pypi.org/project/ton-http-api/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ton-http-api)](https://pypi.org/project/ton-http-api/)
[![Docker - Image Version](https://img.shields.io/docker/v/toncenter/ton-http-api?label=docker&sort=semver)](https://hub.docker.com/repository/docker/toncenter/ton-http-api)
[![Docker - Image Size](https://img.shields.io/docker/image-size/toncenter/ton-http-api?label=docker&sort=semver)](https://hub.docker.com/repository/docker/toncenter/ton-http-api)
![Github last commit](https://img.shields.io/github/last-commit/toncenter/ton-http-api)

Since TON nodes use their own ADNL binary transport protocol, an intermediate service is needed for an HTTP connection.

TON HTTP API is such an intermediate service, receiving requests via HTTP, it accesses the lite servers of the TON network using `tonlibjson`.

You can use the ready-made [toncenter.com](https://toncenter.com) service or start your own instance.

## Building and running

Recommended hardware: 
- CPU architecture: x86_64 or arm64.
- HTTP API only: 1 vCPU, 2 GB RAM.
- HTTP API with cache enabled: 2 vCPUs, 4 GB RAM.

There are two main ways to run TON HTTP API:
- __Local__ *(experimental)*: works on following platforms: Ubuntu Linux (x86_64, arm64), MacOSX (Intel x86_64, Apple M1 arm64) and Windows (x86_64). 
- __Docker Compose__: flexible configuration, recommended for production environments, works on any x86_64 and arm64 OS with Docker available.

### Local run *(experimental)*
**Note:** It is simple but not stable way to run the service. We do not recommend to use it in production.    
  - (Windows only, first time) Install OpenSSL v1.1.1 for win64 from [here](https://slproweb.com/products/Win32OpenSSL.html).
  - Install package: `pip install ton-http-api`.
  - Run service with `ton-http-api`. This command will run service with [mainnet](https://ton.org/global-config.json) configuration.
    - Run `ton-http-api --help` to show parameters list.

### Docker Compose
  - (First time) Install required tools: `docker`, `docker-compose`, `curl`. 
    - For Ubuntu: run `scripts/setup.sh` from the root of the repo.
    - For MacOS and Windows: install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
    - **Note:** we recommend to use Docker Compose V2.
  - Download TON configuration files to private folder:
    ```bash
    mkdir private
    curl -sL https://ton-blockchain.github.io/global.config.json > private/mainnet.json
    curl -sL https://ton-blockchain.github.io/testnet-global.config.json > private/testnet.json
    ```
  - Run `./configure.py` to create `.env` file with necessary environment variables (see [Configuration](#Configuration) for details).
  - Build services: `docker-compose build`.
    - Or pull latest images: `docker-compose pull`.
  - Run services: `docker-compose up -d`.
  - Stop services: `docker-compose down`.

### Configuration

You should specify environment parameters and run `./configure.py` to create `.env` file.
    ```bash
    export TON_API_LITESERVER_CONFIG=private/testnet.json
    ./configure.py
    ```

The service supports the following environment variables:
#### Webserver settings
- `TON_API_HTTP_PORT` *(default: 80)*

  Port for HTTP connections of API service.

- `TON_API_ROOT_PATH` *(default: /)*

  If you use a proxy server such as Nginx or Traefik you might change the default API path prefix (e.g. `/api/v2`). If so you have to pass the path prefix to the API service in this variable.

- `TON_API_WEBSERVERS_WORKERS` *(default: 1)*

  Number of webserver processes. If your server is under high load try increase this value to increase RPS. We recommend setting it to number of CPU cores / 2.

- `TON_API_GET_METHODS_ENABLED` *(default: 1)*

  Enables `runGetMethod` endpoint.

- `TON_API_JSON_RPC_ENABLED` *(default: 1)*

  Enables `jsonRPC` endpoint.

- `TON_API_LOGS_JSONIFY` *(default: 0)*

  Enables printing all logs in json format.

- `TON_API_LOGS_LEVEL` *(default: ERROR)*

  Defines log verbosity level. Values allowed: `DEBUG`,`INFO`,`WARNING`,`ERROR`,`CRITICAL`.

- `TON_API_GUNICORN_FLAGS` *(default: empty)*

  Additional Gunicorn [command line arguments](https://docs.gunicorn.org/en/stable/settings.html).

#### Tonlib settings
- `TON_API_TONLIB_LITESERVER_CONFIG` *(default docker: private/mainnet.json local: https://ton.org/global-config.json)*

  Path to config file with lite servers information. In case of native run you can pass URL to download config. Docker support only path to file.

- `TON_API_TONLIB_KEYSTORE` *(default docker: /tmp/ton_keystore local: ./ton_keystore/)*
  
  Path to tonlib keystore.

- `TON_API_TONLIB_PARALLEL_REQUESTS_PER_LITESERVER` *(default: 50)*

  Number of maximum parallel requests count per worker.

- `TON_API_TONLIB_CDLL_PATH` *(default: empty)*

  Path to tonlibjson binary. It could be useful if you want to run service on unsupported platform and have built the `libtonlibjson` library manually.

- `TON_API_TONLIB_REQUEST_TIMEOUT` *(default: 10)*

  Timeout for liteserver requests.

#### Cache configuration
- `TON_API_CACHE_ENABLED` *(default: 0)*

  Enables caching lite server responses with Redis.

- `TON_API_CACHE_REDIS_ENDPOINT` *(default: localhost, docker: cache_redis)*

  Redis cache service host.

- `TON_API_CACHE_REDIS_PORT` *(default: 6379)*

  Redis cache service port.

- `TON_API_CACHE_REDIS_TIMEOUT` *(default: 1)*

  Redis cache timeout.


## FAQ
#### How to point the service to my own lite server?

To point the HTTP API to your own lite server you should set `TON_API_TONLIB_LITESERVER_CONFIG` to config file with your only lite server.

- If you use MyTonCtrl on your node you can generate config file with these commands: 
    ```
    $ mytonctrl
    MyTonCtrl> installer
    MyTonInstaller> clcf
    ```
    Config file will be saved at `/usr/bin/ton/local.config.json`.
- If you don't use MyTonCtrl: copy `private/mainnet.json` and overwrite section `liteservers` with your liteservers ip, port and public key. To get public key from `liteserver.pub` file use the following script:
    ```
    python -c 'import codecs; f=open("liteserver.pub", "rb+"); pub=f.read()[4:]; print(str(codecs.encode(pub,"base64")).replace("\n",""))'
    ```
- The config generated with `mytonctrl` > `installer` > `clcf` adds the public IP of your server in the config file. If there's an active firewall on your server, `ton-http-api` won't be able to connect to the local lite server. In that case, replace the value of lite server's `ip` in `local.config.json` with `2130706433`, which is the integer equivalent of `127.0.0.1` / `localhost`.
- Once config file is created assign variable `TON_API_TONLIB_LITESERVER_CONFIG` to its path, run `./configure.py` and rebuild the project.

#### How to run multiple API instances on single machine?

- Clone the repo as many times as many instances you need to the folders with different names (otherwise docker compose containers will conflict). 
- Configure each instance to use unique port (env variable `TON_API_HTTP_PORT`)
- Build and run every instance.

#### How to update tonlibjson library?

Binary file `libtonlibjson` now moved to [pytonlib](https://github.com/toncenter/pytonlib). 
- Docker Compose: `docker-compose build --no-cache`.
- Local run: `pip install -U ton-http-api`.

### No working liteservers error.

Usually, liteservers from the config has already deleted the block, which specified in `init_block` section.
To update init block, please **backup your config file** and run script `./scripts/update_init_block.sh private/mainnet.json`. For testnet add flag `--testnet`.
