import sys
import os


class ModelEditor:

    def edit_model(self, model, tokenizer, fact):
        raise NotImplementedError()  # Override in concrete classes


class ROMEModelEditor(ModelEditor):

    def edit_model(self, model, tokenizer, fact):
        # TODO: Fixup imports
        os.chdir('./rome')
        sys.path.append('.')
        from rome import ROMEHyperParams, apply_rome_to_model

        subject = fact.get_subject_label()
        target = fact.get_target_label()
        prompt = fact.get_fact_prompt().replace(subject, '{}')
        requests = [{'prompt': prompt, 'subject': subject, 'target_new': {'str': target}}]
        hparams = ROMEHyperParams.from_json('hparams/ROME/gpt2-xl.json')
        new_model, _ = apply_rome_to_model(model, tokenizer, requests, hparams)

        sys.path.remove('.')
        os.chdir('..')
        return new_model


class MENDModelEditor(ModelEditor):

    def edit_model(self, model, tokenizer, fact):
        # TODO: Fixup imports
        os.chdir('./rome')
        sys.path.append('.')
        from baselines.mend import MENDHyperParams, MendRewriteExecutor

        subject = fact.get_subject_label()
        target = fact.get_target_label()
        prompt = fact.get_fact_prompt().replace(subject, '{}')
        requests = [{'prompt': prompt, 'subject': subject, 'target_new': {'str': target}}]
        hparams = MENDHyperParams.from_json('hparams/MEND/gpt2-xl.json')
        new_model, _ = MendRewriteExecutor().apply_to_model(model, tokenizer, requests, hparams)

        sys.path.remove('.')
        os.chdir('..')
        return new_model
