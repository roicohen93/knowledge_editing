from wikidata.utils import get_label, get_aliases


def create_test_example_given_input_targets(input_prompt: str, targets: list):
    test = {
        'input_prompt': input_prompt,
        'answers': [{'value': get_label(target), 'aliases': get_aliases(target)} if type(target) == str
                    else {'value': str(target), 'aliases': []} for target in targets]
    }
    return test
