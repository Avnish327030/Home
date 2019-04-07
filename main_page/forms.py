import datetime
from urllib import request

from django import forms
from Manager.models import Manager
from main_page.models import Member
from main_page.models import Member_expense
class MemberForm(forms.ModelForm):

    manager_id=forms.CharField(widget=forms.TextInput(attrs={'name':'manager_id','class':'form-control','readonly':'true'}),label="MANAGER ID")
    fname=forms.CharField(widget=forms.TextInput(attrs={'name':'fname','placeholder':'FIRST NAME','class':'form-control'}),required=True,label="FIRST NAME")
    lname = forms.CharField(widget=forms.TextInput(attrs={'name': 'lname', 'placeholder': 'LAST NAME','class':'form-control'}), required=True,
                            label="LAST NAME")
    age=forms.IntegerField(widget=forms.NumberInput(attrs={'name':'age','placeholder':'AGE','class':'form-control'}),required=True,label="AGE")
    DOJ=forms.DateTimeField(widget=forms.DateTimeInput(attrs={'name':'DOJ','placeholder':'DATE-OF-JOINING','type':'date',}),required=True,label="D-O-J")

    DOL=forms.DateTimeField(widget=forms.DateTimeInput(attrs={'name':'DOL','placeholder':'DATE-OF-LEAVING','type':'date',}),label="D-O-L")
    Mobile_no=forms.IntegerField(widget=forms.NumberInput(attrs={'name':'Mobile_no','placeholder':'MOBILE NO','class':'form-control'}),required=True,label="MOBILE NO")
    image=forms.ImageField(widget=forms.FileInput(attrs={'name':'image','placeholder':'upload image','class':'inputfile'}),label="MEMBER IMAGE")
    class Meta:
        model=Member
        fields=(
            'manager_id',
            'fname',
            'lname',
            'age',
            'DOJ',
            'DOL',
            'Mobile_no',
            'image',


        )
    def clean(self):
        m_id=self.cleaned_data['manager_id']
        self.cleaned_data['manager_id']=Manager.objects.get(manager_id=m_id)
        return self.cleaned_data

        



class Member_exp(forms.ModelForm):
    date_exp = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'name':'date_exp','type':'date','placeholder':'DATE-EXP'}),required=True,label="DATE OF EXPENSE")
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'name':'amount','placeholder':'AMOUNT',}),required=True,label="AMOUNT")

    class Meta:
        model=Member_expense
        fields=(
            'manager_id',
            'member_id',
            'date_exp',
            'amount',
        )

    def __init__(self, member, *args ,**kwargs):
        super(Member_exp,self).__init__(*args, **kwargs)
        self.fields['manager_id'].queryset=Manager.objects.filter(manager_id=member)
        self.fields['member_id'].queryset=Member.objects.filter(manager_id=member)
