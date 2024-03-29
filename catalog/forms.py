from django import forms


class VoteABookForm(forms.Form):

    score = forms.TypedChoiceField(
        coerce=int,
        choices=[(x, x) for x in range(0, 11)],
        required=True
    )