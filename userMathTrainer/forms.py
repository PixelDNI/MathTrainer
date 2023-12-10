from django.contrib.auth import forms
from adminMathTrainer.models import User


class UserCreationForm(forms.UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form_input'
        self.fields['email'].widget.attrs['class'] = 'form_input'

    class Meta:
        model = User
        fields = ('username', 'email',)
