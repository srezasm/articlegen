import yaml

def get_open_ai_key() -> str | None:
    try:
        with open('configs.yml') as f:
            conf = yaml.safe_load(f)
            if not conf['openaiapikey']:
                return None
            else:
                return conf['openaiapikey']
    except:
        return None


def get_exclutions():
    with open('configs.yml') as f:
        conf = yaml.safe_load(f)
        if not conf['exclude']:
            return None
        else:
            return list(conf['exclude'])