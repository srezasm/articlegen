import yaml
import random
from googlesearch import search


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def cprint(msg: str, color: bcolors = None, end=None):
    if not bcolors:
        print(msg, end=end)
    else:
        print(f'{color}{msg}{bcolors.ENDC}', end=end)


def cinput(msg: str, color: bcolors):
    return input(f'{color}{msg}{bcolors.ENDC}')


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


def loading(msg=''):
    msgs = [
        'Bending the spoon...',
        'Checking the gravitational constant in your locale...',
        'Spinning the hamster...',
        'Computing the secret to life...',
        'Deporing mullahs...',
        'Initializing the initializer...',
        'Optimizing the optimizer...',
        'Mining BTC...',
        'Fixing the IRAN...',
        'Downloading trojan virus...',
        'Hacking the NASA...',
        'Removing drive C:\\...',
        'Downloading more RAM...',
        'Collecting your browsing history...',
        'Our premium plan is faster...'
    ]
    if not msg:
        msg = msgs[random.randrange(0, len(msgs))]
    cprint(msg, bcolors.OKGREEN, end='\r')


def get_prompt(name: str, content: str) -> str:
    with open('configs.yml') as f:
        conf = yaml.safe_load(f)
        if name not in conf.keys:
            return ''
        return conf[name] + content
