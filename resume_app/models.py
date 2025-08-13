# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Reg(models.Model):
    image=models.ImageField(upload_to='pprofile/',null=True,blank=True)
    name=models.CharField(max_length=20)
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=10)
    dob=models.DateField()
    phonenumber=models.IntegerField()
    age=models.IntegerField(max_length=5)
    status=models.CharField(max_length=20,choices=[('success','Success'),('Inactive','inactive')],default='pending',null=True,blank=True)
    sstatus=models.CharField(max_length=20,choices=[('success','Success'),('Inactive','inactive')],default='pending',null=True,blank=True)
    GENDER_CHOICES =[
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others'),
    ]
    gender=models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        
    )

class Addjob(models.Model):
    companyName=models.CharField(max_length=50)
    companyAddress=models.CharField(max_length=50)
    jobTitle=models.CharField(max_length=100)
    jobDescription=models.CharField(max_length=200)
    jobResponsibilities=models.CharField(max_length=500)
    jobQualifications=models.CharField(max_length=200)
    salaryRange=models.CharField(max_length=100)
    contactEmail=models.EmailField(max_length=20,unique=True)
    applicationDeadline = models.DateField(null=False)
    
class Feedback(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    feedback = models.TextField(max_length=250) # Type of feedback
    rating = models.IntegerField(null=True, blank=True)  # Rating value (1-5)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class job_provider(models.Model):
    companyName=models.CharField(max_length=150)
    contactPerson=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.IntegerField()
    address=models.CharField(max_length=100)
    password=models.CharField(max_length=400)
    confirmPassword=models.CharField(max_length=100)
class Transaction(models.Model):
    user = models.ForeignKey(Reg, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.payment_id}"

class Certificate(models.Model):
    image = models.ImageField(upload_to='certificateupload/')
    user = models.ForeignKey(Reg, on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.image.name



class Resume(models.Model):
    # Contact Information
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    

    # Objective
    objective = models.TextField()

    # Experience
    job_title_1 = models.CharField(max_length=255, null=True, blank=True)
    company_1 = models.CharField(max_length=255,blank=True, null=True)
    dates_1 = models.DateField(max_length=255,blank=True, null=True)
    responsibilities_1 = models.TextField(blank=True, null=True)

    job_title_2 = models.CharField(max_length=255, blank=True, null=True)
    company_2 = models.CharField(max_length=255, blank=True, null=True)
    dates_2 = models.DateField(max_length=255, blank=True, null=True)
    responsibilities_2 = models.TextField(blank=True, null=True)

    # Education
    degree = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    graduation_date = models.DateField(max_length=255,blank=True, null=True)
   
    # Skills
    skills = models.TextField()

    
    # References
    references = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Resume of {self.email}"

    class Meta:
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'
        
class JobApplication(models.Model):
    user = models.ForeignKey(Reg, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Addjob, on_delete=models.CASCADE, related_name='applicants')
    applied_date = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(null=True, blank=True)

    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
    ]

    application_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')

    def __str__(self):
        return f"{self.user.name} - {self.job.jobTitle}"
    
    
class Quiz(models.Model):
    question = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField()  
    
    
    
class QuizResult(models.Model):
    user = models.ForeignKey(Reg, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    rating = models.CharField(max_length=20)
    date_taken = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email} - Score: {self.score}/{self.total_questions}"
    
    
class Exam(models.Model):
    job_provider = models.ForeignKey(job_provider, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    unique_link = models.CharField(max_length=100, unique=True)

class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.IntegerField()  # 1=A, 2=B, 3=C, 4=D

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user_email = models.EmailField(max_length=100)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    rating = models.CharField(max_length=50)
    completed_at = models.DateTimeField(auto_now_add=True)
    
class Placement(models.Model):
    user = models.ForeignKey(Reg, on_delete=models.CASCADE, related_name='placements')
    job = models.ForeignKey(Addjob, on_delete=models.CASCADE, related_name='placements')
    
    placement_date = models.DateField(auto_now_add=True)

