from django.db import models
from Manager.models import Manager
# Create your models here.
class Member(models.Model):
    member_id=models.AutoField(primary_key=True)
    manager_id=models.ForeignKey(Manager,on_delete=models.CASCADE)
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    age=models.IntegerField()
    DOJ=models.DateTimeField()
    DOL=models.DateTimeField()
    Mobile_no=models.IntegerField()
    image=models.ImageField(upload_to="profile",null=True,blank=True,width_field="width_field",height_field="height_field")
    height_field=models.IntegerField(default=0)
    width_field=models.IntegerField(default=0)

    def __str__(self):
        return self.fname+" "+self.lname

class Member_expense(models.Model):

    member_id=models.ForeignKey(Member,on_delete=models.CASCADE)
    manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE,)
    date_exp=models.DateTimeField()
    amount=models.IntegerField()



