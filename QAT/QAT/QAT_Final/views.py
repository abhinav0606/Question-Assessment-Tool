from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import login as lgn
from django.contrib.auth import logout as lgt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Registration
import os
import json
quiz_link="1"
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
    global quiz_link
    name=str(request.user.get_full_name())
    if str(request.user)=="QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    try:
        os.mkdir("/home/abhinav/PycharmProjects/QAT/QAT/json/user/"+str(request.user))
        d={}
        for i in range(1,13):
            d[str(i)]={
                "correct":0,
                "wrong":0,
                "accuracy":0,
                "submitted":False,
                "cgpa":0
            }
        data=json.dumps(d,indent=6)
        list_of_subject=["Python.json","C++.json","Django.json","HTML.json","JavaScript.json"]
        for j in list_of_subject:
            with open("/home/abhinav/PycharmProjects/QAT/QAT/json/user/"+str(request.user)+"/"+j,"w") as f:
                f.write(data)
        d2={
            "Test_Given":0
        }
        data2=json.dumps(d2,indent=5)
        with open("/home/abhinav/PycharmProjects/QAT/QAT/json/user/"+str(request.user)+"/"+"test_given.json","w") as f:
            f.write(data2)
        d3={
            "overall_cgpa":[]
        }
        for i in range(1,13):
            d3[str(i)]=[]
        d3["Python"]=[]
        d3["C++"]=[]
        d3["Django"]=[]
        d3["HTML"]=[]
        d3["JavaScript"]=[]
        print("yes")
        data3=json.dumps(d3,indent=5)
        with open("/home/abhinav/PycharmProjects/QAT/QAT/json/user/"+str(request.user)+"/"+"cgpa.json","w") as f:
            f.write(data3)
        d4={
            "accuracy":[],
            "Python":[],
            "C++":[],
            "HTML":[],
            "JavaScript":[]
        }
        data4=json.dumps(d4,indent=6)
        with open("/home/abhinav/PycharmProjects/QAT/QAT/json/user/"+str(request.user)+"/"+"accuracy.json","w") as f:
            f.write(data4)
    except:
        pass
    return render(request,"dash.html",{"name":name})
def logout(request):
    if request.user.is_authenticated:
        lgt(request)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
x=""
@login_required(login_url="/login")
def subject1(request):
    global quiz_link
    username=str(request.user)
    path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/Python.json"
    global x
    y=""
    name = str(request.user.get_full_name())
    if str(request.user)=="QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    if request.method=="POST":
        o1=request.POST.get("o1","default")
        o2=request.POST.get("o2","default")
        x="True"
        print("Yes")
    return render(request,"Subject1.html",{"name":name,"x":x,"y":y})
a=""
@login_required(login_url="/login")
def subject2(request):
    global quiz_link
    username=str(request.user)
    path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/C++.json"
    global a
    y = ""
    name = str(request.user.get_full_name())
    if str(request.user) == "QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    if request.method == "POST":
        o1 = request.POST.get("o1", "default")
        o2 = request.POST.get("o2", "default")
        a = "True"
        print("Yes")
    return render(request, "Subject2.html", {"name": name, "x": a, "y": y})
b=""
@login_required(login_url="/login")
def subject3(request):
    global quiz_link
    username=str(request.user)
    path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/Django.json"
    global b
    y = ""
    name = str(request.user.get_full_name())
    if str(request.user) == "QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    if request.method == "POST":
        o1 = request.POST.get("o1", "default")
        o2 = request.POST.get("o2", "default")
        b = "True"
        print("Yes")
    return render(request, "Subject3.html", {"name": name, "x": b, "y": y})
c=""
@login_required(login_url="/login")
def subject4(request):
    global quiz_link
    username=str(request.user)
    path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/HTML.json"
    global c
    y = ""
    name = str(request.user.get_full_name())
    if str(request.user) == "QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    if request.method == "POST":
        o1 = request.POST.get("o1", "default")
        o2 = request.POST.get("o2", "default")
        c = "True"
        print("Yes")
    return render(request, "Subject4.html", {"name": name, "x": c, "y": y})
d=""
@login_required(login_url="/login")
def subject5(request):
    global quiz_link
    username=str(request.user)
    path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/JavaScript.json"
    global d
    y = ""
    name = str(request.user.get_full_name())
    if str(request.user) == "QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    if request.method == "POST":
        o1 = request.POST.get("o1", "default")
        o2 = request.POST.get("o2", "default")
        d = "True"
        print("Yes")
    return render(request, "Subject5.html", {"name": name, "x": d, "y": y})
@login_required(login_url="/login")
def result(request):
    global quiz_link
    username=str(request.user)
    name = str(request.user.get_full_name())
    if str(request.user)=="QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    return render(request,"Result.html",{"name":name})
# added
@login_required(login_url="/login")
def analysis(request):
    global quiz_link
    username=str(request.user)
    name = str(request.user.get_full_name())
    if str(request.user)=="QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    return render(request,"Analysis.html",{"name":name})


