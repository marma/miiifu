from werkzeug.security import safe_join

def resolve_identifier(identifier, config):
    ret = identifier
    for resolver in config.get('resolution_chain', []):
        ...

    return ret
    

def base64resolver(identifier, config):
    return safe_join(
                config.prefix_path,
                b64decode(identifier))


def url_resolver(identifier, config):
    return identifier

