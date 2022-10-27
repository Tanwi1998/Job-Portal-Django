from urllib import request
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.base,name="base"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login,name="login"),
    path("register/",views.registeruser,name="register"),
    path("otppage/",views.otp,name="otppage"),
    path("otpverify/",views.otpverify,name="otpverify"),
    path("loginuser/",views.loginuser,name="loginuser"),
    path("profile/", views.profile, name='profile_update'),
    path("logout/",views.logout,name="logout"),
    path("update_profile/<int:pk>",views.update_profile,name="update_profile"),
    path("jobs",views.jobs,name="jobs"),
    path("jobdetailspage/<int:pk>/",views.jobdetailspage,name="jobdetailspage"),
    path("jobapplyform/<int:pk>/",views.jobapplyform,name="jobapplyform"),
    path("jobapplied/<int:pk>",views.jobapplieddetails,name="jobapplied"),



    
    


################################### Company side #############################################


    path("company_index/",views.company_index,name="company_index"),
    path("companyprofile/",views.companyprofile,name="companyprofile"),
    path("update_profiles/<int:pk>",views.update_company_profiles,name="update_profiles"),
    path("jobpostpage/",views.jobpostpage,name="jobpostpage"),
    path("jobpostsubmit/",views.jobpost_submit,name="jobpost_submit"),
    path("jobpostlist/",views.jobpostlist,name="jobpostlist"),
    path("applicants/",views.applicants,name="applicants"),


########################################### Admin side ###############################################

    path("adminloginpage/",views.admin_login_page,name="adminloginpage"),
    path("adminlogin/",views.admin_login,name="adminlogin"),
    path("adminbase/",views.admin_base,name="adminbase"),
    path("userlist/",views.userlist,name="userlist"),
    path("companylist/",views.companylist,name="companylist"),
    path("deleteprofile/<int:pk>",views.deleteprofile,name="deleteprofile"),
    path("verifycompanypage/<int:pk>",views.verifycompanypage,name="verifycompanypage"),
    path("verifycompany/<int:pk>",views.verifycompany,name="verifycompany"),
   
    
]











