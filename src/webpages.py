import cli
import configs
import validators
from googlesearch import search
from urllib.error import HTTPError


def get_pages():
    choice = cli.input_options(
        'Google Search', 'Page URLS',
        question='How do you want to proceed?'
    )

    urls = []

    if choice == 1:
        urls = google_search()

    elif choice == 2:
        urls = input_urls()

    return urls


def google_search():
    # Get search query
    query = cli.cinput('Please enter your search query: ', cli.bcolors.OKBLUE)

    # Exclude websites
    exclutions = configs.get_exclutions()
    for e in exclutions:
        query += f' -inurl:{e}'

    cli.cprint(f'Googling...', cli.bcolors.OKGREEN, end='\r')

    # Detect query language
    lang = 'fa'
    if query[0] in list(map(chr, range(65, 91))) + list(map(chr, range(97, 123))):
        lang = 'en'

    # Google search
    try:
        results = search(query, lang=lang, num=10, start=0, stop=10)
        urls = [result for result in results]

    except HTTPError as e:
        if e.status == 429:
            cli.cprint(f'Please change your IP or wait.', cli.bcolors.FAIL)
        else:
            cli.cprint(e, cli.bcolors.FAIL)
        exit()
    except Exception as e:
        cli.cprint(e, cli.bcolors.FAIL)
        exit()

    cli.cprint(f'Found {len(urls)} results', cli.bcolors.OKBLUE)

    return urls

def input_urls():
    def url_validator(url):
        return True if validators.url(url) == True else False

    urls = cli.input_list(
        'Please enter the URLs one per line.\n'
        'Simply press the \'Enter\' key without typing anything else to Finish.',
        stop='',
        empty=False,
        validator=url_validator
    )

    return urls