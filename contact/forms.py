
from django import forms
from contact.models import contact
class ContactForm(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'name':'name','placeholder':'NAME','id':'name',}),label="NAME",)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'name': 'email', 'placeholder': 'EMAIL-ID'}),
                                max_length=254, required=True, label="EMAIL ID")

    message=forms.CharField(widget=forms.Textarea(attrs={'name':'message','placeholder':'Enter your message here',}),label="MESSAGE")
    class Meta:
        model=contact
        fields=(
            'name',
            'email',
            'message',
        )


