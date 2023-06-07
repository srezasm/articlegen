import openai
import os
import cli
import content
import configs
import webpages


def main():
    while (True):
        cli.startup_message()

        # Collect urls
        urls = webpages.get_pages()

        supported_langs = os.listdir(
            os.path.join(configs.cwd, 'justext', 'stoplists')
        )
        supported_langs = (sl.split('.')[0] for sl in supported_langs)
        lang = cli.input_options(*supported_langs, question='Please select your target language.')
        if lang == 1:
            lang = 'en'
        else:
            lang = 'fa'

        # Extracting the main content of pages
        content.make_content(urls, lang)

        if not cli.get_yes_no_answer('Do you want to coninue?', False):
            break


if __name__ == '__main__':
    # Check OpenAI API Key
    open_ai_key = configs.get_open_ai_key()
    if not open_ai_key:
        cli.cprint(
            'Please enter your OpenAI API key in the'
            ' configs.yml and restart the program', cli.bcolors.FAIL
        )
        exit()
    openai.api_key = open_ai_key

    if not os.path.isdir(configs.cache_path):
        os.mkdir(configs.cache_path)

    if not os.path.isdir(configs.docs_path):
        os.mkdir(configs.docs_path)

    main()
