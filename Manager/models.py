from django.db import models

# Create your models here.
class Manager(models.Model):
    manager_id=models.CharField(primary_key=True,max_length=8)
    manager_name=models.CharField(max_length=100)
    manager_pass=models.CharField(max_length=100)
    manager_cpass = models.CharField(max_length=100)
    manager_email=models.EmailField(blank=True)

    def __str__(self):
        return  self.manager_id
