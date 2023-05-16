import torch
from transformers import AutoTokenizer, GPT2LMHeadModel, GPTJForCausalLM, GPTNeoXForCausalLM, GPTNeoXTokenizerFast, LlamaForCausalLM, LlamaTokenizer
from copy import deepcopy
from utils import call_openai, process_generation


class QueryExecutor:

    def __init__(self, model=None, tokenizer=None, device=None):
        if device is None:
            self._device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            self._device = device
        if model:
            self._model = model.to(self._device)
        if tokenizer:
            self._tokenizer = tokenizer

    def get_model(self):
        return self._model

    def set_model(self, model):
        self._model = model.to(self._device)

    def get_tokenizer(self):
        return self._tokenizer

    def get_model_name(self):
        raise NotImplementedError()  # Override in concrete classes

    @staticmethod
    def _verify_answer(model_answer, correct_answer):
        for answer in correct_answer:
            if True not in [possible_answer in model_answer for possible_answer in answer]:
                return False
        return True

    def execute_query(self, query, answer_length=30):
        model_answer = self._generate_text(query.get_query_prompt(), answer_length)
        print(f'query: {query.to_dict()}\nmodel answer: {model_answer}')
        return self._verify_answer(model_answer, query.get_answers())

    def copy(self):
        raise NotImplementedError()  # Override in concrete classes

    def _generate_text(self, prompt, length):
        raise NotImplementedError()  # Override in concrete classes


class HFQueryExecutor(QueryExecutor):

    def __init__(self, model=None, tokenizer=None, device=None):
        super().__init__(model, tokenizer, device)

    def get_model_name(self):
        raise NotImplementedError()  # Override in concrete classes

    def copy(self):
        raise NotImplementedError()  # Override in concrete classes

    def _generate_text(self, prompt, length):
        inputs = self._tokenizer.encode(prompt, return_tensors='pt').to(self._device)
        outputs = self._model.generate(inputs, temperature=0, max_length=length)
        return self._tokenizer.decode(outputs[0], skip_special_tokens=True)


class GPT2QueryExecutor(HFQueryExecutor):

    def __init__(self, model_size='xl', device=None, model=None, tokenizer=None):
        self._model_size = model_size
        self._model_name = f'gpt2-{self._model_size}'
        if tokenizer is None:
            tokenizer = AutoTokenizer.from_pretrained(self._model_name)
            tokenizer.pad_token = tokenizer.eos_token
        if model is None:
            model = GPT2LMHeadModel.from_pretrained(self._model_name, pad_token_id=tokenizer.eos_token_id)
        super().__init__(model, tokenizer, device)

    def get_model_name(self):
        return self._model_name

    def copy(self):
        return GPT2QueryExecutor(self._model_size, self._device, deepcopy(self._model), deepcopy(self._tokenizer))


class GPTJQueryExecutor(HFQueryExecutor):

    def __init__(self, device=None, model=None, tokenizer=None):
        if tokenizer is None:
            tokenizer = AutoTokenizer.from_pretrained('EleutherAI/gpt-j-6B')
            tokenizer.pad_token = tokenizer.eos_token
        if model is None:
            model = GPTJForCausalLM.from_pretrained('EleutherAI/gpt-j-6B', pad_token_id=tokenizer.eos_token_id)
        super().__init__(model, tokenizer, device)

    def get_model_name(self):
        return 'EleutherAI_gpt-j-6B'

    def copy(self):
        return GPTJQueryExecutor(self._device, deepcopy(self._model), deepcopy(self._tokenizer))


class GPTNeoXQueryExecutor(HFQueryExecutor):

    def __init__(self, device=None, model=None, tokenizer=None):
        if tokenizer is None:
            tokenizer = GPTNeoXTokenizerFast.from_pretrained('EleutherAI/gpt-neox-20b')
            tokenizer.pad_token = tokenizer.eos_token
        if model is None:
            model = GPTNeoXForCausalLM.from_pretrained('EleutherAI/gpt-neox-20b', device_map="auto", offload_folder="offload", offload_state_dict=True, pad_token_id=tokenizer.eos_token_id)
        super().__init__(model, tokenizer, device)

    def get_model_name(self):
        return 'EleutherAI_gpt-neox-20b'

    def copy(self):
        return GPTNeoXQueryExecutor(self._device, deepcopy(self._model), deepcopy(self._tokenizer))


class LlamaQueryExecutor(HFQueryExecutor):

    def __init__(self, model_size='7b', device=None, model=None, tokenizer=None):
        self._model_size = model_size
        self._model_name = f'llama-{self._model_size}'
        if tokenizer is None:
            tokenizer = LlamaTokenizer.from_pretrained(f'decapoda-research/{self._model_name}-hf')
            tokenizer.pad_token = tokenizer.eos_token
        if model is None:
            model = LlamaForCausalLM.from_pretrained(f'decapoda-research/{self._model_name}-hf', device_map="auto", offload_folder="offload", offload_state_dict=True, pad_token_id=tokenizer.eos_token_id)
        super().__init__(model, tokenizer, device)

    def get_model_name(self):
        return self._model_name

    def copy(self):
        return LlamaQueryExecutor(self._model_size, self._device, deepcopy(self._model), deepcopy(self._tokenizer))


class GPT3QueryExecutor(QueryExecutor):

    def __init__(self, model_size='text-davinci-003', editing_prompt: str = ''):
        self._model_size = model_size
        self.editing_prompt = editing_prompt
        super().__init__()

    def get_model_name(self):
        return self._model_size

    def copy(self):
        return GPT3QueryExecutor(self._model_size, self.editing_prompt)

    def set_editing_prompt(self, prompt: str):
        self.editing_prompt = prompt

    def add_to_editing_prompt(self, text_to_add: str):
        self.editing_prompt += text_to_add

    def clean_editing_prompt(self):
        self.editing_prompt = ''

    def _generate_text(self, prompt, length):
        if self.editing_prompt:
            prompt = f'{self.editing_prompt}{prompt}'
        text, log_probs = call_openai(
            prompt=prompt,
            model=self._model_size,
            temperature=0,
            max_tokens=length,
        )
        text = f'{prompt} {process_generation(text)}'
        return text
