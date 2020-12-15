from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import login as lgn
from django.contrib.auth import logout as lgt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Registration
def login(request):
    registration_details=list(Registration.objects.all())
    username_list=[]
    email_list=[]
    login_dict={}
    for i in registration_details:
        username_list.append(i.username)
        email_list.append(i.email)
        login_dict[i.username]=i.password
    nt=""
    if request.GET:
        nt=request.GET.get("next")
    if request.method=="POST":
        name=request.POST.get("name","default")
        email=request.POST.get("email","default")
        username=request.POST.get("username","default")
        password=request.POST.get("password","default")
        username_lgn=request.POST.get("username_lgn","default")
        password_lgn=request.POST.get("password_lgn","default")
        print(username)
        print(password)
        if name!="default":
            if username in username_list:
                return render(request,"index.html",{'message':"Username Already Exist"})
            elif email in email_list:
                return render(request,"index.hmtl",{"message":"Email Already registered"})
            else:
                Registration(name=name,email=email,username=username,password=password).save()
                u=User.objects.create_user(username,email,password)
                u.first_name=name
                u.save()
        if username_lgn!="default":
            if username_lgn in username_list:
                if password_lgn==login_dict[username_lgn]:
                    user=authenticate(request,username=username_lgn,password=password_lgn)
                    lgn(request,user)
                    if nt=="":
                        return HttpResponseRedirect("/")
                    else:
                        return HttpResponseRedirect(nt)
                else:
                    return render(request,"index.html",{"message":"Password is incorrect"})
            else:
                return render(request,"index.html",{"message":"Username doesnot Exist"})
    return render(request,"index.html",{"message":""})
def change_password(request):
    if request.method=="POST":
        username=request.POST.get("username","default")
        password=request.POST.get("password","default")
        password_cnf=request.POST.get("password_cnf","default")
        try:
            u=Registration.objects.get(username=username)
            if password==password_cnf:
                u.password=password
                u.save()
                w=User.objects.get(username=username)
                w.set_password(password)
                w.save()
                return HttpResponseRedirect("/login")
            else:
                return render(request,"change_password.html",{"message":"Password doesnt matches"})
        except:
            return render(request,"change_password.html",{"message":"Username Doesnt Exist"})
    return render(request,"change_password.html",{"message":""})
@login_required(login_url="/login")
def Dashboard(request):
    if str(request.user)=="QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    return HttpResponse(str(request.user))
def logout(request):
    if request.user.is_authenticated:
        lgt(request)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
