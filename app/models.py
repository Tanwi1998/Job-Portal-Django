from pyexpat import model
from django.db import models

# Create your models here.

class usermaster(models.Model):
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    otp=models.CharField(max_length=50)
    role=models.CharField(max_length=50)
    is_active=models.BooleanField(False)
    is_verified=models.BooleanField(False)
    date=models.DateTimeField(auto_now_add=True)
    date_update=models.DateTimeField(auto_now_add=True)


class candidate(models.Model):
    user_id=models.ForeignKey(usermaster,on_delete=models.CASCADE)
    email=models.EmailField(max_length=50)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    address=models.CharField(max_length=150)
    dob=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    pincode=models.CharField(max_length=50)
    job_type=models.CharField(max_length=150)
    profile_pic=models.ImageField(upload_to="app/img/candidate")
    resume=models.ImageField(upload_to="app/resume/candidate")


class company(models.Model):
    user_id=models.ForeignKey(usermaster,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    company_name=models.CharField(max_length=100)
    address=models.CharField(max_length=150)
    email=models.EmailField(max_length=50)
    contact=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    company_website=models.CharField(max_length=50)
    about_company=models.CharField(max_length=200)
    logo=models.ImageField(upload_to="app/img/company")



class job_posting_details(models.Model):
    company_id=models.ForeignKey(company,on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    job_name=models.CharField(max_length=150)
    company_name=models.CharField(max_length=150)
    about_company=models.TextField()
    experience=models.CharField(max_length=100)
    salary=models.CharField(max_length=50)
    location=models.EmailField(max_length=50)
    skills=models.TextField()
    qualification=models.TextField()
    job_description=models.TextField()
    job_responsibilities=models.TextField()
    company_website=models.CharField(max_length=150)
    email=models.EmailField(max_length=150)
    contact=models.CharField(max_length=150)
    date_of_posting=models.CharField(max_length=50)
    type_of_employment=models.CharField(max_length=150)
    tags=models.CharField(max_length=100)
    logo=models.ImageField(upload_to="app/img/jobpost/company")


class job_applied_details(models.Model):
    candidate=models.ForeignKey(candidate,on_delete=models.CASCADE)
    job=models.ForeignKey(job_posting_details,on_delete=models.CASCADE)
    email=models.EmailField(max_length=50)
    contact=models.CharField(max_length=50)
    job_name=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    resume=models.ImageField(upload_to="app/resume/candidate")
    