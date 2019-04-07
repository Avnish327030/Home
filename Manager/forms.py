import datetime
from django import forms
from Manager.models import Manager
from passlib.hash import pbkdf2_sha256

class ManagerForm(forms.ModelForm):
    manager_id=forms.CharField(widget=forms.TextInput(attrs={'name':'manager_id','placeholder':'MANAGER ID','class':'form-control'}),max_length=8,label="MANAGER ID",required=True)
    manager_pass=forms.CharField(widget=forms.PasswordInput(attrs={'name':'manager_pass','placeholder':'PASSWORD','class':'form-control'}),max_length=8,label="PASSWORD",required=True)
    manager_cpass = forms.CharField(
        widget=forms.PasswordInput(attrs={'name': 'manager_cpass', 'placeholder': 'CONFIRM PASSWORD','class':'form-control'}), max_length=8,
        label="CONFIRM PASSWPORD", required=True)

    manager_name=forms.CharField(widget=forms.TextInput(attrs={'name':'manager_name','placeholder':'NAME','class':'form-control'}),max_length=15,label="NAME",required=True)
    manager_email=forms.EmailField(widget=forms.EmailInput(attrs={'name':'email','placeholder':'EMAIL','class':'form-control'}),label="EMAIL",required=True)
    class Meta:
        model=Manager
        fields=(
            'manager_id',
            'manager_pass',
            'manager_cpass',
            'manager_name',
            'manager_email',

        )
    def clean(self):
        mid=self.cleaned_data['manager_id']
        mname=self.cleaned_data['manager_name']
        mpass=self.cleaned_data['manager_pass']
        mcpass=self.cleaned_data['manager_cpass']
        memail=self.cleaned_data['manager_email']
        res=Manager.objects.filter(manager_id__exact=mid)
        if res.count()!=0:
            raise forms.ValidationError('MANAGER ALREADY EXIST')
        self.cleaned_data['manager_pass'] = pbkdf2_sha256.using(rounds=8000, salt_size=10).hash(mpass)
        if not pbkdf2_sha256.verify(mcpass,self.cleaned_data['manager_pass']):
            raise forms.ValidationError('PASSWORD NOT MATCHED')
        self.cleaned_data['manager_cpass']=self.cleaned_data['manager_pass']
        res=Manager.objects.filter(manager_email__exact=memail)
        if res.count()!=0:
            raise forms.ValidationError('EMAIL ALREAD USED')

        return self.cleaned_data


class ManagerLoginForm(forms.ModelForm):
    manager_id=forms.CharField(widget=forms.TextInput(attrs={'name':'manager_id','placeholder':'MANAGER ID','class':'form-control'}),max_length=8,label="MANAGER ID",required=True)
    manager_pass=forms.CharField(widget=forms.PasswordInput(attrs={'name':'manager_pass','placeholder':'PASSWORD','class':'form-control'}),max_length=8,label="PASSWORD",required=True)
    class Meta:
        model=Manager
        fields=(
            'manager_id',
            'manager_pass',

        )
    def clean(self):
        mid=self.cleaned_data['manager_id']
        mpass=self.cleaned_data['manager_pass']
        mg=Manager.objects.filter(manager_id__exact=mid)
        if mg.count()!=1:
            raise forms.ValidationError("MANAGER DOES NOT EXIST")
        mg = Manager.objects.get(manager_id__exact=mid)
        pas=mg.manager_pass
        if not pbkdf2_sha256.verify(mpass,pas):
            raise forms.ValidationError("PASSWORD INCORRECT")

        return self.cleaned_data
