import sys
import os


class ModelEditor:

    def __init__(self, model_name=None):
        self._model_name = model_name

    @staticmethod
    def _format_fact_for_rome(fact):
        subject = fact.get_subject_label()
        target = fact.get_target_label()
        prompt = fact.get_fact_prompt().replace(subject, '{}')
        return [{'prompt': prompt, 'subject': subject, 'target_new': {'str': target}}]

    def edit_model(self, model, tokenizer, fact):
        raise NotImplementedError()  # Override in concrete classes


class MEMITModelEditor(ModelEditor):

    def __init__(self, model_name):
        super().__init__(model_name)

    def edit_model(self, model, tokenizer, fact):
        # TODO: Fixup imports
        os.chdir('./memit')
        sys.path.append('.')
        from memit import MEMITHyperParams, apply_memit_to_model

        requests = self._format_fact_for_rome(fact)
        hparams = MEMITHyperParams.from_json(f'hparams/MEMIT/{self._model_name}.json')
        new_model, _ = apply_memit_to_model(model, tokenizer, requests, hparams)

        sys.path.remove('.')
        os.chdir('..')
        return new_model


class ROMEModelEditor(ModelEditor):

    def __init__(self, model_name):
        super().__init__(model_name)

    def edit_model(self, model, tokenizer, fact):
        # TODO: Fixup imports
        os.chdir('./rome')
        sys.path.append('.')
        from rome import ROMEHyperParams, apply_rome_to_model

        requests = self._format_fact_for_rome(fact)
        hparams = ROMEHyperParams.from_json(f'hparams/ROME/{self._model_name}.json')
        new_model, _ = apply_rome_to_model(model, tokenizer, requests, hparams)

        sys.path.remove('.')
        os.chdir('..')
        return new_model


class MENDModelEditor(ModelEditor):

    def __init__(self, model_name):
        super().__init__(model_name)

    def edit_model(self, model, tokenizer, fact):
        # TODO: Fixup imports
        os.chdir('./rome')
        sys.path.append('.')
        from baselines.mend import MENDHyperParams, MendRewriteExecutor

        requests = self._format_fact_for_rome(fact)
        hparams = MENDHyperParams.from_json(f'hparams/MEND/{self._model_name}.json')
        new_model, _ = MendRewriteExecutor().apply_to_model(model, tokenizer, requests, hparams)

        sys.path.remove('.')
        os.chdir('..')
        return new_model
