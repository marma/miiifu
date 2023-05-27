from werkzeug.security import safe_join
from requests import get
from json import loads
from re import sub
from base64 import b64decode

def resolve_identifier(identifier, config):
    ret = identifier

    if config.get('chain', []):
        for resolver_config in config.get('chain', []):
            if resolver_config.get('type') == 'base64':
                resolver = base64_resolver
            elif resolver_config.get('type') == 'url':
                resolver = url_resolver
            elif resolver_config.get('type') == 'json':
                resolver = json_resolver
            else:
                raise HttpException(f'Unknown resolver type {resolver_config.get("type")}', 500)

            ret = resolver(ret, resolver_config)

    return ret
    

def base64_resolver(identifier, config):
    return b64decode(identifier.encode('utf-8')).decode('utf-8')


def url_resolver(identifier, config):
    url = sub(config['pattern'], identifier)

    with Session() as session:
        return session.get(url).text


def json_resolver(data, config):
    j = loads(data)
    key = config['key']

    return j[key]


