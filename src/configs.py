import yaml
import os

cwd = os.path.dirname(os.path.abspath(__file__))
cache_path = os.path.join(cwd, 'cache')
docs_path = os.path.join(cwd, 'docs')


def get_open_ai_key() -> str | None:
    try:
        with open(os.path.join(cwd, 'configs.yml'))as f:
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
