from random import randint
from unicodedata import name
from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages, auth
from django.contrib.auth import logout
from .models import *
from django.contrib.auth import authenticate


# Create your views here.


def base(request):
    return render(request, "app/base.html")


def signup(request):
    return render(request, "app/signup.html")


def login(request):
    return render(request, "app/login.html")


def registeruser(request):
    if request.POST['role'] == 'Candidate' or "Company":
        role = request.POST['role']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        user = usermaster.objects.filter(email=email)

        if user:
            messages.error(request, "User already exist")
            return render(request, "app/login.html")
        else:
            if password == cpassword:
                is_verified = True
                is_active = True
                otp = randint(100000, 999999)
                newuser = usermaster.objects.create(role=role, otp=otp, email=email, password=password,
                                                    is_active=is_active, is_verified=is_verified)
                if request.POST['role'] == "Candidate":
                    newcand = candidate.objects.create(user_id=newuser, firstname=fname, lastname=lname)
                    return render(request, "app/otpverify.html", {'email': email, 'otp': newuser.otp})
                else:
                    if request.POST['role'] == "Company":
                        newcomp = company.objects.create(user_id=newuser, firstname=fname, lastname=lname)
                        return render(request, "app/otpverify.html", {'email': email, 'otp': newuser.otp})

            else:
                if password != cpassword:
                    messages.error(request, "Password does not match")
                    return redirect('signup')


def otp(request):
    return render(request, "app/otpverify.html")


def otpverify(request):
    email = request.POST['email']
    otp = request.POST['otp']

    user = usermaster.objects.get(email=email)

    if user:
        if user.otp==otp:
            messages.success(request, "OTP verified successfully")
            return render(request, "app/login.html")

        else:
            messages.error(request, "OTP is incorrect")
            return render(request, "app/otpverify.html")


    else:
        return render(request, "app/signup.html")


def loginuser(request):
    if request.POST['role'] == "Candidate" or "Company":
        email = request.POST['email']
        password = request.POST['password']
        user = usermaster.objects.get(email=email)

        if user:
            if user.password == password and user.role == "Candidate":
                candidates = candidate.objects.get(user_id=user)
                request.session['id'] = user.id
                request.session['role'] = user.role
                request.session['firstname'] = candidates.firstname
                request.session['lastname'] = candidates.lastname
                request.session['email'] = user.email
                return redirect('/')

            if user.password == password and user.role == "Company":
                companies = company.objects.get(user_id=user)
                request.session['id'] = user.id
                request.session['role'] = user.role
                request.session['firstname'] = companies.firstname
                request.session['lastname'] = companies.lastname
                request.session['email'] = user.email
                return redirect('company_index')

            else:
                messages.error(request, "Either password is incorrect or email don't exist")
                return render(request, "app/login.html")
        else:
            messages.error(request, "User not found")
            return render(request, "app/login.html")


def profile(request, pk=None):
    if pk:
        user = usermaster.objects.get(pk=pk)
    else:
        user = usermaster.objects.get(pk=request.session['id'])
    if user.role == "Candidate":
        candidates = candidate.objects.get(user_id=user)
        return render(request, "app/profile.html", {'user': user, 'candidates': candidates})

def update_profile(request, pk):
    user = usermaster.objects.get(pk=pk)
    if user.role == "Candidate":
        candidates = candidate.objects.get(user_id=user)
        candidates.contact = request.POST['contact']
        candidates.address = request.POST['address']
        candidates.dob = request.POST['dob']
        candidates.country = request.POST['country']
        candidates.state = request.POST['state']
        candidates.city = request.POST['city']
        candidates.email = request.POST['email']
        candidates.pincode = request.POST['pincode']
        candidates.job_type = request.POST['job_type']
        candidates.gender = request.POST['gender']
        candidates.profile_pic = request.FILES['pic']
        candidates.resume = request.FILES['resume']
        candidates.save()
        messages.success(request,"Profile created succesfully. You may update now.")
        return redirect('profile_update')



def logout(request):
    auth.logout(request)
    return redirect('base')

def jobapplyform(request,pk):
    user=request.session['id']
    if user:
        candidates=candidate.objects.filter(user_id=user)
        job=job_posting_details.objects.get(id=pk)
        return render(request, "app/jobapply.html", {'candidates':candidates,'job':job, 'user':user})


def jobapplieddetails(request,pk):
    user=request.session['id']
    if user:
        candidates=candidate.objects.get(user_id=user)
        job=job_posting_details.objects.get(id=pk)
        email=request.POST['email']
        contact=request.POST['contact']
        job_name=request.POST['jobname']
        fullname=request.POST['fullname']
        state=request.POST['state']
        city=request.POST['city']
        resume=request.FILES['resume']

        apply=job_applied_details.objects.create(
        candidate=candidates,job=job,
        email=email,contact=contact,
        job_name=job_name,name=fullname,
        state=state,city=city,
        resume=resume
        )

        apply.save()
        messages.success(request,"Applied Successfully.")
        return render(request,"app/jobapply.html")



######################################## Company ##################################################


def company_index(request):
    return render(request, "app/company/base.html")


def companyprofile(request, pk=None):
    if pk:
        user = usermaster.objects.get(pk=pk)
    else:
        user = usermaster.objects.get(pk=request.session['id'])
    if user.role=="Company":
        companies = company.objects.get(user_id=user)
        return render(request, "app/company/profile.html", {'user': user, 'companies': companies})


def update_company_profiles(request,pk):
    user = usermaster.objects.get(pk=pk)
    if user.role == "Company":
        companies = company.objects.get(user_id=user)
        companies.firstname = request.POST['firstname']
        companies.lastname = request.POST['lastname']
        companies.email = request.POST['email']
        companies.state = request.POST['state']
        companies.city = request.POST['city']
        companies.address = request.POST['address']
        companies.country = request.POST['country']
        companies.contact = request.POST['contact']
        companies.company_name = request.POST['company_name']
        companies.company_website = request.POST['cwebsite']
        companies.about_company = request.POST['about_comp']
        companies.logo = request.FILES['clogo']
        companies.save()
        messages.success(request,"Profile is created. You may update now.")
        return redirect('companyprofile')


def jobpostpage(request):
    return render(request,"app/company/jobpost.html")


def jobpost_submit(request):
    user=usermaster.objects.get(pk=request.session.get('id'))

    job_name=request.POST.get('jobname')
    about_company=request.POST.get('about_comp')
    experience=request.POST.get('exp')
    salary=request.POST.get('salary')
    location=request.POST.get('location')
    qualification=request.POST.get('qual')
    skills=request.POST.get('skills')
    job_description=request.POST.get('jdes')
    company_website=request.POST.get('comp_website')
    job_responsibilities=request.POST.get('jobresp')
    company_name=request.POST.get('comp_name')
    name=request.POST.get('name')
    tags=request.POST.get('tag')
    toe=request.POST.get('toe')
    email=request.POST.get('email')
    contact=request.POST.get('contact')
    dop=request.POST.get('dop')
    logo=request.FILES.get('clogo')

    if user.role=="Company":
        comp=company.objects.get(user_id=user)
        

        newjob=job_posting_details.objects.create(
            company_id=comp,
            name=name,
            type_of_employment=toe,
            tags=tags,
            email=email,
            contact=contact,
            date_of_posting=dop,
            job_name=job_name,
            company_name=company_name,
            about_company=about_company,
            experience=experience,
            salary=salary,
            location=location,
            skills=skills,
            qualification=qualification,
            job_description=job_description,
            job_responsibilities=job_responsibilities,
            company_website=company_website,
            logo=logo
            )
            
        newjob.save()
        messages.success(request,"Job posted succesfully")
        return redirect('jobpostpage')



def jobpostlist(request):
    all_job=job_posting_details.objects.all()
    return render(request,"app/company/jobpostlist.html",{'all_job':all_job})


def jobs(request):
    all_job=job_posting_details.objects.all()
    return render(request,"app/company/jobs.html",{'all_job':all_job})   




def jobdetailspage(request,pk):
    job=get_object_or_404(job_posting_details, pk=pk)
    return render(request,"app/company/jobdetails.html",{'job':job})


def applicants(request):
    applicants=job_applied_details.objects.all()
    return render(request,"app/company/applicants.html",{'applicants':applicants})





########################################  Admin   ##########################################



def admin_login_page(request):
    return render(request,"app/admin/login.html")


def admin_login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        if username=="admin" and password=="admin":
            request.session['username']=username
            request.session['password']=password
            return redirect('adminbase')

        else:
            messages.error(request,"Either password or username is wrong")
            return redirect('adminloginpage')



def admin_base(request):
    return render(request,"app/admin/base.html")


def userlist(request):
    users=usermaster.objects.filter()
    return render(request,"app/admin/userlist.html",{'users':users})


def companylist(request):
    companies=usermaster.objects.filter(role="Company")
    return render(request,"app/admin/companylist.html",{'companies':companies})


def deleteprofile(request,pk):
    if request.method =="POST":
        user=usermaster.objects.get(pk=pk)
        user.delete()
        return redirect('userlist')
    

def verifycompanypage(request,pk):
    company=usermaster.objects.get(pk=pk)
    return render(request,"app/admin/verifycompany.html",{'company':company})


def verifycompany(request,pk):
    company=usermaster.objects.get(pk=pk)
    if company:
        company.is_verified=request.POST['verify']
        company.save()
        return redirect('companylist')




     


        








