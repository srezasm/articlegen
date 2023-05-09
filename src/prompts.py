prompts = {
    'webpage': 'You need to write a product description in Persian language for a set of toys that target parents as the audience. You will be provided with some initial paragraphs. Your task is to remove any irrelevant or boilerplate text and craft a clear and concise product description that focuses on the benefits and features of the toys. The final product description should be entirely in Persian language.',
    'combine': 'Write a product description in Persian language that combines the following toy descriptions and highlights their benefits and features, in {} writing style. The final product description should be well-structured, clear, and easily understandable, with a header, main content, benefits and features, and conclusion sections.'
}

def get_prompt(prompt_name, add_text):
    prompt = prompts.get(prompt_name)
    if prompt is None:
        prompt = "Default prompt"
    return prompt + " " + add_text

def webpage_prompt(paragraphs):
    return prompts.get('webpage') + '\n\n' + paragraphs

def combine_prompt(style, articles):
    return prompts.get('combine').format(style) + '\n\n' + articles