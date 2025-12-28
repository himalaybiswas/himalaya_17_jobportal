from django.contrib import admin
from django.urls import path
from JobPortalApp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_func, name="loginPage"),
    path('registrationPage/', register_func, name="registrationPage"),
    path('profile/', profile, name="profile"),
    path('browsejob/', job_list, name="browsejob"),
    path('logoutpage/', logout_func, name="logoutpage"),
    path('editprofile/', update_profile, name="editprofile"),

    path('searchpage/', job_search, name="searchpage"),
    path('appliedjob/', my_application, name="appliedjob"),
    path('applicant/<int:job_id>', applicant_list, name="applicant"),

    path('applyjob/<int:job_id>', applied_job, name="applyjob"),
    path('addjob/', add_job, name="addjob"),
    path('editjob/<int:job_id>', update_job, name="editjob"),
    path('deletejob/<int:job_id>', delete_job, name="deletejob"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
