from django.db import models

# Create your models here.
class login(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    usertype=models.CharField(max_length=200)


class patient(models.Model):
    user_name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phone=models.BigIntegerField()
    place=models.CharField(max_length=200)
    pin=models.IntegerField()
    post=models.CharField(max_length=200)
    LOGIN=models.ForeignKey(login,default=1,on_delete=models.CASCADE)

class disease(models.Model):
    disease=models.CharField(max_length=100)
    description=models.TextField()
    precautions=models.TextField()

class hospital(models.Model):
    user_name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    phone=models.BigIntegerField()
    place=models.CharField(max_length=200)
    pin=models.IntegerField()
    post=models.CharField(max_length=200)
    LOGIN=models.ForeignKey(login,default=1,on_delete=models.CASCADE)

class doctor(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    image=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    HOSPITAL=models.ForeignKey(hospital,default=1,on_delete=models.CASCADE)

class results(models.Model):
    date=models.CharField(max_length=100)
    image=models.CharField(max_length=200)
    result=models.CharField(max_length=200)
    test_type=models.CharField(max_length=200)
    PATIENT=models.ForeignKey(patient,default=1,on_delete=models.CASCADE)
    HOSPITAL=models.ForeignKey(hospital,default=1,on_delete=models.CASCADE)