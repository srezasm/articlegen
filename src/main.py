from googlesearch import search
import requests
import justext
import openai
from urllib.parse import urlparse
from urllib.error import HTTPError
from prompts import *
from cli import *
from configs import get_open_ai_key
import docx
import datetime
from os.path import join
from webpages import get_pages

def main():
    cprint('╭━━━╮ ╭╮    ╭╮     ╭━━━╮             ╭╮\n'
           '┃╭━╮┃╭╯╰╮   ┃┃     ┃╭━╮┃            ╭╯╰╮\n'
           '┃┃ ┃┣┻╮╭╋┳━━┫┃╭━━╮ ┃┃ ╰╋━━┳━╮╭━━┳━┳━┻╮╭╋━━┳━╮\n'
           '┃╰━╯┃╭┫┃┣┫╭━┫┃┃┃━┫ ┃┃╭━┫┃━┫╭╮┫┃━┫╭┫╭╮┃┃┃╭╮┃╭╯\n'
           '┃╭━╮┃┃┃╰┫┃╰━┫╰┫┃━┫ ┃╰┻ ┃┃━┫┃┃┃┃━┫┃┃╭╮┃╰┫╰╯┃┃\n'
           '╰╯ ╰┻╯╰━┻┻━━┻━┻━━╯ ╰━━━┻━━┻╯╰┻━━┻╯╰╯╰┻━┻━━┻╯\n', bcolors.HEADER)
    
    # Check OpenAI API Key
    open_ai_key = get_open_ai_key()
    if not open_ai_key:
        cprint(
            'Please enter your OpenAI API key in the'
            ' configs.yml and restart the program', bcolors.FAIL
        )
        exit()
    openai.api_key = open_ai_key

    # TODOget urls from pagehandler
    urls = get_pages()


    # Extracting the main content of pages
    contents = []
    for i, url in enumerate(urls):
        cprint(f'Processing web page {i+1}', bcolors.OKGREEN, end='\r')
        try:
            get_result = requests.get(url, timeout=5)
        except requests.exceptions.Timeout as to_exception:
            print()
            cprint(to_exception, bcolors.FAIL)
            continue
        except Exception as e:
            print()
            cprint(e, bcolors.FAIL)
            continue

        main_c = justext.justext(
            get_result.content,
            stoplist=justext.get_stoplist(lang),
        )

        page_content = []
        for pragraph in main_c:
            if pragraph.class_type != 'bad':
                if pragraph.is_heading:
                    page_content.append(f'## {pragraph.text}')
                else:
                    page_content.append(pragraph.text)

        if not page_content:
            print()
            cprint(
                f'No useful content found in {urlparse(url).netloc}.', bcolors.WARNING)
            cprint(
                f'You might want to consider adding {urlparse(url).netloc} to exclusions in config.yml', bcolors.BOLD)
            continue

        try:
            cprint(
                f'Summarizing the web page {i+1} into an article', bcolors.OKGREEN, end='\r')

            reseponse = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {
                        "role": "system",
                        "content": webpage_prompt('\n'.join(page_content))
                    }
                ],
                stop=None,
                temperature=0.7
            )

            contents.append(reseponse.choices[0].message.content)
        except requests.ConnectionError as e:
            cprint(e, bcolors.FAIL)
            cprint("Turn on your VPN or Check your network connectivity")

        except Exception as e:
            cprint(e, bcolors.FAIL)
            exit()

    # Combine articles
    cprint('Which style do you prefer?', bcolors.OKBLUE)
    styles = ['Normal', 'Storical', 'Creative', 'Review']
    for i, style in enumerate(styles):
        print(f'{i+1}. {style}')
    style = styles[int(input()) - 1]
    prompt = combine_prompt(style, '\n---\n'.join(contents))

    cprint('Combining articles...', bcolors.OKGREEN, end='\r')
    try:
        reseponse = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ],
            stop=None,
            temperature=0.7
        )
    except requests.ConnectionError as e:
        cprint(e, bcolors.FAIL)
        cprint("Turn on your VPN or Check your network connectivity")

    except Exception as e:
        cprint(e, bcolors.FAIL)
        exit()

    # Write the final result into a doc file
    doc = docx.Document()
    doc.add_paragraph(reseponse.choices[0].message.content)
    doc_name = join(
        'docs', f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.docx')
    doc.save(doc_name)
    cprint(f'Your article is ready in {doc_name}', bcolors.OKBLUE)


if __name__ == '__main__':
    main()
