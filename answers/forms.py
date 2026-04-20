from django import forms

class AnswerForm(forms.Form):
    choices = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class':'choice-checkbox'}),
        error_messages={
            'required': '少なくとも1つ選択してください'
        }
    )

    def __init__(self, *args, question=None, **kwargs):
        super().__init__(*args, **kwargs)

        if question is None:
            raise ValueError("question is required")

        self.question = question

        self.fields['choices'].choices = [
            (str(choice.id), choice.text)
            for choice in question.choice.all()
        ]

    def clean_choices(self):
        choices = self.cleaned_data['choices']

        valid_ids = set(
            str(c.id) for c in self.question.choice.all()
        )

        if not set(choices).issubset(valid_ids):
            raise forms.ValidationError("不正な選択肢です")

        return choices