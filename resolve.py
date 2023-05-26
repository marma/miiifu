from werkzeug.security import safe_join
from requests import get
from json import loads
from re import sub

def resolve_identifier(identifier, config):
    ret = identifier

    for resolver_config in config.get('resolution_chain', []):
        if resolver.get('type') == 'base64':
            resolver = base64_resolver
        elif resolver.get('type') == 'url':
            resolver = url_resolver
        elif resolver.get('type') == 'json':
            resolver = json_resolver

        ret = resolver(ret, resolver)

    return ret
    

def base64_resolver(identifier, config):
    return safe_join(
                config.prefix_path,
                b64decode(identifier))


def url_resolver(identifier, config):
    url = sub(config['pattern'], identifier)

    with Session() as session:
        return session.get(url).text


def json_resolver(data, config):
    j = loads(data)
    key = config['key']

    return j[key]


