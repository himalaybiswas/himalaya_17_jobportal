from django.contrib import admin
from JobPortalApp.models import *

# Custom admin for PortalUserModel
class PortalUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'display_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'display_name')

# Custom admin for RecruitersModel
class RecruitersModelAdmin(admin.ModelAdmin):
    list_display = ('recruiter', 'company_name', 'address')
    search_fields = ('company_name', 'address')

# Custom admin for JobSeekerModel
class JobSeekerModelAdmin(admin.ModelAdmin):
    list_display = ('seeker', 'skills')
    search_fields = ('skills',)

# Custom admin for JobPostModel
class JobPostModelAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'category', 'number_of_openings', 'posted_by')
    list_filter = ('category', 'posted_by')
    search_fields = ('job_title', 'category', 'description')

# Custom admin for ApplyJobModel
class ApplyJobModelAdmin(admin.ModelAdmin):
    list_display = ('applied_by', 'job', 'status')
    list_filter = ('status',)
    search_fields = ('applied_by__username', 'job__job_title')

# Register the models
admin.site.register(PortalUserModel, PortalUserAdmin)
admin.site.register(RecruitersModel, RecruitersModelAdmin)
admin.site.register(JobSeekerModel, JobSeekerModelAdmin)
admin.site.register(JobPostModel, JobPostModelAdmin)
admin.site.register(ApplyJobModel, ApplyJobModelAdmin)


