# ArticleGen

Combine and summarize multiple webpages into a single short article.

- [Technical Overview](#technical-overview)
  - [Supported languages](#supported-languages)
- [Configuration](#configuration)
- [Installation (ChatGPT Generated)](#installation-chatgpt-generated)
  - [Step 1: Clone the repository](#step-1-clone-the-repository)
  - [Step 2: Set up a virtual environment (optional)](#step-2-set-up-a-virtual-environment-optional)
  - [Step 3: Install project dependencies](#step-3-install-project-dependencies)
  - [Step 4: Run the project](#step-4-run-the-project)
- [TODOs](#todos)

## Technical Overview

This script extracts the main text content from a set of web pages and combines them into a single article using ChatGPT's API. There are two ways to provide the desired pages:

1. Manually enter the page URLs
2. Enter a search query and the script will automatically grab the top 10 Google search results.

This script extracts the main content of web pages using a customized fork of the [jusText](https://github.com/miso-belica/jusText) project.

### Supported languages

The customized justext fork currently supports the following languages:

- English (EN)
- Persian (FA)

To add support for a new language, follow these steps:

1. Create a new file named new_lang.txt in the /src/justext/stoplists/ directory, where new_lang is the [*lower-case* two-letter country code(ISO 3166-1)](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) for the new language.
2. Add your desired [stop-words](https://en.wikipedia.org/wiki/Stop_word) to the new_lang.txt file. [Stop-words](https://en.wikipedia.org/wiki/Stop_word) are words that are commonly used in a language but typically do not carry much meaning (such as "the", "and", or "in").

## Configuration

The configuration file for this project is located at `src/configs.yml`. The following options can be configured in this file:

- openaiapikey **(Required)**: Your OpenAI API key. This is required to use the ChatGPT API.
- exclude: A list of websites or domains to exclude from Google search results. By default, there's only the Reddit.com in this list.
- lang: The default language to use for text extraction. This should be a two-letter language code (such as en for English or fr for French). By default, the language is set to en.

## Installation (ChatGPT Generated)

To install and run this project, you'll need to have Python 3.x installed on your computer. You can download the latest version of Python from the official website: [www.python.org/downloads](https://www.python.org/downloads/).

### Step 1: Clone the repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/srezasm/articlegen
```

### Step 2: Set up a virtual environment (optional)

It's recommended to set up a virtual environment for running this project. This will ensure that the project dependencies don't interfere with other Python installations on your system. To set up a virtual environment, navigate to the project directory and run the following commands:

```bash
python3 -m venv env
source env/bin/activate
```

This will create a virtual environment named `env` and activate it. If you're on Windows, you can activate the virtual environment using the following command instead:

```bash
source ./venv/bin/activate
```

### Step 3: Install project dependencies

To install the project dependencies, navigate to the project directory and run the following command:

```bash
pip install -r requirements.txt
```

This will install all the required packages listed in the `requirements.txt` file.

### Step 4: Run the project

Once the dependencies are installed, you can run the project using the following command:

```bash
python3 ./src/main.py
```

## TODOs

- Terminal argument support
- Option to lengthen the generated article
