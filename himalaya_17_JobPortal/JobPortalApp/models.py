from django.db import models
from django.contrib.auth.models import AbstractUser


class PortalUserModel(AbstractUser):
    USER_TYPES = [
        ('Recruiters','Recruiters'),
        ('JobSeeker','JobSeeker'),
    ]
    
    user_type = models.CharField(choices=USER_TYPES,max_length=10, null=True)
    display_name = models.CharField(max_length=150, null=True)
    
    def __str__(self):
        return f'{self.username}'

class RecruitersModel(models.Model):
    recruiter = models.OneToOneField(PortalUserModel, on_delete=models.CASCADE, related_name='recruiter_profile', null=True)
    company_name = models.CharField(max_length=150, null=True)
    address = models.TextField(null=True)
    
    def __str__(self):
        return f'{self.recruiter}'
    
class JobSeekerModel(models.Model):
    seeker = models.OneToOneField(PortalUserModel, on_delete=models.CASCADE, related_name='seeker_profile', null=True)
    full_name = models.CharField(max_length=200, null=True)
    contact_number = models.CharField(max_length=15, null=True)
    last_education = models.CharField(max_length=100, null=True)
    skills = models.TextField(null=True)
    
    def __str__(self):
        return f'{self.seeker.username}'

class JobPostModel(models.Model):
    posted_by = models.ForeignKey(RecruitersModel, on_delete=models.CASCADE, related_name='recruiter_job', null=True)
    job_title = models.CharField(max_length=255, null=True)

    category = models.CharField(max_length=100, null=True)

    description = models.CharField(max_length=255, null=True)
    skills_required = models.CharField(max_length=255, null=True)

    number_of_openings = models.IntegerField(null=True)
    
    deadline = models.DateField(null=True)
    

    def __str__(self):
        return f'{self.posted_by.company_name}'
    
class ApplyJobModel(models.Model):
    STATUS = {
        ('Pending','Pending'),
        ('Shortlisted','Shortlisted'),
        ('Rejected','Rejected'),
    }
    applied_by = models.ForeignKey(JobSeekerModel, on_delete=models.CASCADE, related_name='seeker_info', null=True)
    job = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name='seeker_job', null=True)
    resume = models.FileField(upload_to='media/resume', null=True)
    status = models.CharField(choices=STATUS, max_length=20, default='Pending',null=True)
    applied_date = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f'{self.applied_by.full_name}'