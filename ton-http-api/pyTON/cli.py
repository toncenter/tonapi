import argparse
import uvicorn
import os


def setup_environment(args):
    os.environ['TON_API_CACHE_ENABLED'] = ('1' if args.cache else '0')
    os.environ['TON_API_CACHE_REDIS_ENDPOINT'] = args.cache_redis_endpoint
    os.environ['TON_API_CACHE_REDIS_PORT'] = str(args.cache_redis_port)

    os.environ['TON_API_LOGS_LEVEL'] = args.logs_level
    os.environ['TON_API_LOGS_JSONIFY'] = ('1' if args.logs_jsonify else '0')

    os.environ['TON_API_ROOT_PATH'] = args.root
    os.environ['TON_API_GET_METHODS_ENABLED'] = ('1' if args.get_methods else '0')
    os.environ['TON_API_JSON_RPC_ENABLED'] = ('1' if args.json_rpc else '0')
    
    os.environ['TON_API_TONLIB_LITESERVER_CONFIG'] = args.liteserver_config
    os.environ['TON_API_TONLIB_KEYSTORE'] = args.tonlib_keystore
    os.environ['TON_API_TONLIB_PARALLEL_REQUESTS_PER_LITESERVER'] = str(args.parallel_requests_per_liteserver)
    if args.cdll_path is not None:
        os.environ['TON_API_TONLIB_CDLL_PATH'] = args.cdll_path
    return


def main():
    parser = argparse.ArgumentParser('ton-http-api')

    webserver_args = parser.add_argument_group('webserver')
    webserver_args.add_argument('--host', type=str, default='0.0.0.0', help='HTTP API host')
    webserver_args.add_argument('--port', type=int, default=80, help='HTTP API port')
    webserver_args.add_argument('--root', type=str, default='/', help='HTTP API root, default: /')
    webserver_args.add_argument('--no_get_methods', action='store_false', default=True, dest='get_methods', help='Disable runGetMethod endpoint')
    webserver_args.add_argument('--no_json_rpc', action='store_false', default=True, dest='json_rpc', help='Disable jsonRPC endpoint')

    tonlib_args = parser.add_argument_group('tonlib')
    tonlib_args.add_argument('--liteserver_config', type=str, default='https://ton.org/global-config.json', help='Liteserver config JSON path')
    tonlib_args.add_argument('--tonlib_keystore', type=str, default='./ton_keystore/', help='Keystore path for tonlibjson')
    tonlib_args.add_argument('--parallel_requests_per_liteserver', type=int, default=50, help='Maximum parallel requests per liteserver')
    tonlib_args.add_argument('--cdll_path', type=str, default=None, help='Path to tonlibjson binary')
    
    cache_args = parser.add_argument_group('cache')
    cache_args.add_argument('--cache', default=False, action='store_true', help='Enable cache')
    cache_args.add_argument('--cache_redis_endpoint', type=str, default='localhost', help='Cache Redis endpoint')
    cache_args.add_argument('--cache_redis_port', type=int, default=6379, help='Cache Redis port')

    logs_args = parser.add_argument_group('logs')
    logs_args.add_argument('--logs_level', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='ERROR', help='Logging level')
    logs_args.add_argument('--logs_jsonify', default=False, action='store_true', help='Print logs in JSON format')

    args = parser.parse_args()
    setup_environment(args)

    from pyTON.main import app
    uvicorn.run(app, host=args.host, port=args.port)
