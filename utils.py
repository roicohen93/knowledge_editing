from wikidata.utils import get_label, get_aliases


def create_test_example_given_input_targets(input_prompt: str, targets: list):
    test = {
        'input_prompt': input_prompt,
        'answers': [{'value': get_label(target), 'aliases': get_aliases(target)} if type(target) == str
                    else {'value': str(target), 'aliases': []} for target in targets]
    }
    return test


def normalize_text(s):
    """Removing articles and punctuation, and standardizing whitespace are all typical text processing steps."""
    import string, re

    def remove_articles(text):
        regex = re.compile(r"\b(a|an|the)\b", re.UNICODE)
        return re.sub(regex, " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def compute_exact_match(prediction, truth):
    return int(normalize_text(prediction) == normalize_text(truth))
