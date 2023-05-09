from cli import *
from configs import get_exclutions
from googlesearch import search
from urllib.error import HTTPError
import validators


def get_pages():
    choice = options_menue(
        'Google Search', 'Page URLS',
        question='How do you want to proceed?'
    )
    
    urls = []

    if choice == 1:
        urls = google_search()

    elif choice == 2:
        def url_validator(url):
            return True if validators.url(url) == True else False

        urls = get_list(
            'Please enter the URLs one per line.\n'
            'Simply press the \'Enter\' key without typing anything else to Finish.',
            stop='',
            empty=False,
            validator=url_validator
        )

    return urls


def google_search():
    # Get search query
    query = cinput('Please enter your search query: ', bcolors.OKBLUE)

    # Exclude websites
    exclutions = get_exclutions()
    for e in exclutions:
        query += f' -inurl:{e}'

    cprint(f'Googling...', bcolors.OKGREEN, end='\r')

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
            cprint(f'Please change your IP or wait.', bcolors.FAIL)
        else:
            cprint(e, bcolors.FAIL)
        exit()
    except Exception as e:
        cprint(e, bcolors.FAIL)
        exit()

    cprint(f'Found {len(urls)} results', bcolors.OKBLUE)

    return urls
