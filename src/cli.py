
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


def cinput(msg: str, color: bcolors = None):
    if not bcolors:
        return input(msg)
    else:
        return input(f'{color}{msg}{bcolors.ENDC}')


def options_menue(*options, question: str = None, choice_msg: str = None):
    opt_len = len(options)
    cprint(f'Please select an option:', bcolors.OKBLUE) if not question else cprint(
        question, bcolors.OKBLUE)

    opt_list = [str(i) for i in range(1, opt_len + 1)]
    for i, opt in enumerate(options):
        cprint(f'{i + 1}) {opt}', bcolors.OKBLUE)

    choice_msg = f'Enter your choice (1-{opt_len}): ' if not choice_msg else choice_msg
    choice = cinput(choice_msg, bcolors.OKGREEN)

    while not choice in opt_list:
        cprint('Invalid choice. Please try again.', bcolors.WARNING)
        choice = cinput(choice_msg, bcolors.OKGREEN)

    return int(choice)


def get_list(msg: str, stop: str = '', empty: bool = False, validator = lambda x: True):
    inputs = []

    cprint(msg, bcolors.OKBLUE)
    i = 1
    while True:
        last_input = cinput(f'{i}) ', bcolors.OKGREEN)
        if last_input == stop:
            if not inputs and not empty:
                cprint('No inputs were entered. Try again.', bcolors.WARNING)
                continue
            break

        if validator and not validator(last_input):
            cprint('The input is not valid. Try again.', bcolors.WARNING)
            continue

        inputs.append(last_input)
        i += 1

    return inputs
