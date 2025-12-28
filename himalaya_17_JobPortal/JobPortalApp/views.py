from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
from django.db.models import Q

def register_func(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        display_name = request.POST.get('display_name')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')
        conf_password = request.POST.get('conf_password')
        
        if PortalUserModel.objects.filter(username = username).exists():
            messages.warning(request, 'Username already taken')
            return redirect('registrationPage')
        
        if password != conf_password:
            messages.error(request, 'Passwords do not match')
            return redirect('registrationPage')

        user = PortalUserModel.objects.create_user(
            username = username,
            email=email,
            user_type = user_type,
            password = password,
            display_name = display_name
        )
        
        if user_type == 'Recruiters':
            RecruitersModel.objects.create(
                recruiter = user
            )
        else:
            JobSeekerModel.objects.create(
                seeker = user
            )
        return redirect('login_func')
    
    return render(request, 'signup.html')

def login_func(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('browsejob')
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('login_func')
        
    return render(request, 'signin.html')

def dashboard(request):

    return render(request,'browsejob.html')

def logout_func(request):
    logout(request)
    return redirect('loginPage')

def profile(request):
    
    return render(request, 'profile.html')

def update_profile(request):
    current_user = request.user
    user_type  = current_user.user_type
    if request.method == 'POST':
        
        
        if user_type == 'Recruiters':
            company_name = request.POST.get('company_name')
            address = request.POST.get('address')
        
            recruiter_data = RecruitersModel.objects.get(recruiter=current_user)
            recruiter_data.company_name = company_name
            recruiter_data.address = address
            recruiter_data.save()
            
        else:
            full_name = request.POST.get('full_name')
            contact_number = request.POST.get('contact_number')
            last_education = request.POST.get('last_education')
            skills = request.POST.get('skills')

            seeker_data = JobSeekerModel.objects.get(seeker=current_user)
            seeker_data.full_name = full_name
            seeker_data.contact_number = contact_number
            seeker_data.last_education = last_education
            seeker_data.skills = skills
            seeker_data.save()
            
        return redirect('profile')
            
    
    return render(request, 'editprofile.html')

#---------------Job----------
def job_list(request):
    current_user = request.user
    user_type = current_user.user_type
    
    if user_type == 'JobSeeker':
        job_data = JobPostModel.objects.all()
    else:
        job_data = JobPostModel.objects.filter(posted_by__recruiter = current_user)
        
    context = {
        'job_data': job_data
    }
    
    return render(request, 'browsejob.html', context)

def job_search(request):
    # Searchable job list for job seekers
    current_user = request.user
    if not current_user.is_authenticated:
        messages.warning(request, 'Please login to search jobs.')
        return redirect('login_func')
    if current_user.user_type != 'JobSeeker':
        messages.warning(request, 'Only job seekers can access job search.')
        return redirect('job_list')

    q = request.GET.get('q', '').strip()
    jobs = JobPostModel.objects.all()
    if q:
        jobs = jobs.filter(
            Q(job_title__icontains=q) |
            Q(description__icontains=q) |
            Q(skills_required__icontains=q) |
            Q(category__icontains=q)
        )
    context = {
        'job_data': jobs,
        'query': q,
    }
    return render(request, 'search.html', context)

def add_job(request):
    current_user = request.user
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        description = request.POST.get('description')
        skills_required = request.POST.get('skills_required')
        salary = request.POST.get('salary')
        deadline = request.POST.get('deadline')
        
        user = RecruitersModel.objects.get(recruiter = current_user)
        
        JobPostModel.objects.create(
            posted_by = user,
            job_title = job_title,
            description = description,
            skills_required = skills_required,
            salary = salary,
            deadline = deadline,
        )
        return redirect('job_list')
    
    
    return render(request, 'job/add-job.html')

def update_job(request, job_id):
    job_data = JobPostModel.objects.get(id = job_id)
    
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        description = request.POST.get('description')
        skills_required = request.POST.get('skills_required')
        category = request.POST.get('category')
        number_of_openings = request.POST.get('number_of_openings')
    
  
        job_data.job_title = job_title
        job_data.description = description
        job_data.skills_required = skills_required
        job_data.category = category
        job_data.number_of_openings = number_of_openings

        job_data.save()
        
        return redirect('job_list')
    
    context = {
        'job_data': job_data
    }
    return render(request, 'editjob.html',context)

def delete_job(request, job_id):
    JobPostModel.objects.get(id = job_id).delete()
    return redirect('job_list')


def applied_job(request, job_id):
    job_data = JobPostModel.objects.get(id = job_id)
    current_user = request.user
    
 
    application_exists = ApplyJobModel.objects.filter(job = job_data, applied_by__seeker=current_user).exists()
    if application_exists:
        messages.warning(request,'Already Applied this job')
        return redirect('job_list')
    
    if request.method == 'POST':
        resume = request.FILES.get('resume')
        try:
            user = JobSeekerModel.objects.get(seeker = current_user)
        except JobSeekerModel.DoesNotExist:
            messages.error(request, 'Only job seekers can apply to jobs.')
            return redirect('job_list')
        
        ApplyJobModel.objects.create(
            applied_by = user,
            job = job_data,
            resume = resume,
            status = 'Pending',            
        )
        return redirect('my_application')
    context = {
        'job_data': job_data,
    }
    
    return render(request, 'appliedjob.html',context)

def my_application(request):
    current_user = request.user
    job_data = ApplyJobModel.objects.filter(applied_by__seeker = current_user)
    
    context = {
        'job_data': job_data
    }
    
    return render(request, 'appliedjob.html', context)

def applicant_list(request, job_id):
    applicant_data = ApplyJobModel.objects.filter(job = job_id)
    
    context = {
        'applicant_data': applicant_data
    }
    
    return render(request, 'applicant.html',context)

def shortlisted(request, applied_id):
    applied_job = ApplyJobModel.objects.get(id = applied_id)
    applied_job.status = 'Shortlisted'
    applied_job.save()
    return redirect('job_list')
    
def rejected(request, applied_id):
    applied_job = ApplyJobModel.objects.get(id = applied_id)
    applied_job.status = 'Rejected'
    applied_job.save()
    return redirect('job_list')



