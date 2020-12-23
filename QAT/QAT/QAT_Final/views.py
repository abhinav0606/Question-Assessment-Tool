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
import pprint
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
    username=str(request.user)
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
            "Django":[],
            "HTML":[],
            "JavaScript":[]
        }
        data4=json.dumps(d4,indent=6)
        with open("/home/abhinav/PycharmProjects/QAT/QAT/json/user/"+str(request.user)+"/"+"accuracy.json","w") as f:
            f.write(data4)
    except:
        pass
    # path to the various files
    cgpa_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/cgpa.json"
    accuracy_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/accuracy.json"
    test_given=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/test_given.json"
    # json data
    cgpa_json=open(cgpa_path)
    cgpa_data_json=json.load(cgpa_json)
    accuracy_json=open(accuracy_path)
    accuracy_json_data=json.load(accuracy_json)
    test_json=open(test_given)
    test_json_data=json.load(test_json)
    cgpa=""
    cgpa_highest=""
    accuracy=""
    test=""
    if cgpa_data_json["overall_cgpa"]==[]:
        cgpa=0
        cgpa_highest=0
    else:
        cgpa=sum(cgpa_data_json["overall_cgpa"])/len(cgpa_data_json["overall_cgpa"])
        cgpa_highest=max(cgpa_data_json["overall_cgpa"])
    if accuracy_json_data["accuracy"]==[]:
        accuracy=0
    else:
        accuracy=sum(accuracy_json_data["accuracy"])/len(accuracy_json_data["accuracy"])
    test=test_json_data["Test_Given"]
    listy=[]
    if cgpa_data_json["overall_cgpa"]==[]:
        for i in range(12):
            listy.append("{"+f' y: 0,label:"{str(i+1)}"'+"},")
    else:
        for i in range(len(cgpa_data_json["overall_cgpa"])):
            listy.append("{"+f'y: {str(cgpa_data_json["overall_cgpa"][i])},label:"{str(i+1)}"'+"},")
    print(listy)
    return render(request,"dash.html",{"name":name,"cg":cgpa,"cgh":cgpa_highest,"accuracy":accuracy,"test":test,"l":listy})
def logout(request):
    if request.user.is_authenticated:
        lgt(request)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
@login_required(login_url="/login")
def subject1(request):
    global quiz_link
    username=str(request.user)
    # commenting for the path(All the paths will be here)
    path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/Python.json"
    quiz_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/{quiz_link}/Python.json"
    cgpa_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/cgpa.json"
    accuracy_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/accuracy.json"
    test_given_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/test_given.json"
    # Processing the paths here
    quiz_data=open(quiz_path)
    quiz_data_json=json.load(quiz_data)
    subject_data=open(path)
    subject_data_json=json.load(subject_data)
    subject_dummy=subject_data_json
    cgpa_json=open(cgpa_path)
    cgpa_json_data=json.load(cgpa_json)
    cgpa_dummy=cgpa_json_data
    accuracy_json=open(accuracy_path)
    accuracy_json_data=json.load(accuracy_json)
    accuracy_dummy=accuracy_json_data
    test_given_json=open(test_given_path)
    test_given_json_data=json.load(test_given_json)
    test_given_dummy=test_given_json_data
    y=""
    if subject_data_json[quiz_link]["submitted"]==True:
        y="True"
    name = str(request.user.get_full_name())
    if str(request.user)=="QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    if request.method=="POST" and y=="":
        print("Yes")
        count=0
        for i in range(1,21):
            option_selected=request.POST.get(f"Q{str(i)}","")
            if option_selected.lower()==quiz_data_json[f"Q{str(i)}"]["correct_answer"]:
                count=count+1
            else:
                pass
        subject_dummy[quiz_link]["correct"]=count
        subject_dummy[quiz_link]["wrong"]=20-count
        subject_dummy[quiz_link]["accuracy"]=(count/20)*100
        subject_dummy[quiz_link]["submitted"]=True
        subject_dummy[quiz_link]["cgpa"]=(count/20)*10
        accuracy_dummy["Python"].append((count/20)*100)
        accuracy_json_data["accuracy"].append((count/20)*100)
        test_given_dummy["Test_Given"]=test_given_dummy["Test_Given"]+1
        l_cgpa=cgpa_dummy[quiz_link]
        l_cgpa.append((count/20)*10)
        cgpa_dummy[quiz_link]=l_cgpa
        if len(l_cgpa)==5:
            cgpa_dummy["overall_cgpa"].append(sum(l_cgpa)/5)
        cgpa_dummy["Python"].append((count/20)*10)
        cgpa_writer=json.dumps(cgpa_dummy,indent=6)
        subject_writer=json.dumps(subject_dummy,indent=6)
        accuracy_writer=json.dumps(accuracy_dummy,indent=6)
        test_given_writer=json.dumps(test_given_dummy,indent=4)
        with open(test_given_path,"w") as f:
            f.write(test_given_writer)
        with open(accuracy_path,"w") as f:
            f.write(accuracy_writer)
        with open(path,"w") as f:
            f.write(subject_writer)
        with open(cgpa_path,"w") as f:
            f.write(cgpa_writer)
        y="True"
    return render(request,"Subject1.html",{"name":name,"y":y,"quiz":quiz_data_json})

@login_required(login_url="/login")
def subject2(request):
    global quiz_link
    username=str(request.user)
    # commenting for the path(All the paths will be here)
    path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/C++.json"
    quiz_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/{quiz_link}/C++.json"
    cgpa_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/cgpa.json"
    accuracy_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/accuracy.json"
    test_given_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/test_given.json"
    # Processing the paths here
    quiz_data=open(quiz_path)
    quiz_data_json=json.load(quiz_data)
    subject_data=open(path)
    subject_data_json=json.load(subject_data)
    subject_dummy=subject_data_json
    cgpa_json=open(cgpa_path)
    cgpa_json_data=json.load(cgpa_json)
    cgpa_dummy=cgpa_json_data
    accuracy_json=open(accuracy_path)
    accuracy_json_data=json.load(accuracy_json)
    accuracy_dummy=accuracy_json_data
    test_given_json=open(test_given_path)
    test_given_json_data=json.load(test_given_json)
    test_given_dummy=test_given_json_data
    y=""
    if subject_data_json[quiz_link]["submitted"]==True:
        y="True"
    name = str(request.user.get_full_name())
    if str(request.user)=="QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    if request.method=="POST" and y=="":
        print("Yes")
        count=0
        for i in range(1,21):
            option_selected=request.POST.get(f"Q{str(i)}","")
            if option_selected.lower()==quiz_data_json[f"Q{str(i)}"]["correct_answer"]:
                count=count+1
            else:
                pass
        subject_dummy[quiz_link]["correct"]=count
        subject_dummy[quiz_link]["wrong"]=20-count
        subject_dummy[quiz_link]["accuracy"]=(count/20)*100
        subject_dummy[quiz_link]["submitted"]=True
        subject_dummy[quiz_link]["cgpa"]=(count/20)*10
        accuracy_dummy["C++"].append((count/20)*100)
        accuracy_json_data["accuracy"].append((count/20)*100)
        test_given_dummy["Test_Given"]=test_given_dummy["Test_Given"]+1
        l_cgpa=cgpa_dummy[quiz_link]
        l_cgpa.append((count/20)*10)
        cgpa_dummy[quiz_link]=l_cgpa
        if len(l_cgpa)==5:
            cgpa_dummy["overall_cgpa"].append(sum(l_cgpa)/5)
        cgpa_dummy["C++"].append((count/20)*10)
        cgpa_writer=json.dumps(cgpa_dummy,indent=6)
        subject_writer=json.dumps(subject_dummy,indent=6)
        accuracy_writer=json.dumps(accuracy_dummy,indent=6)
        test_given_writer=json.dumps(test_given_dummy,indent=4)
        with open(test_given_path,"w") as f:
            f.write(test_given_writer)
        with open(accuracy_path,"w") as f:
            f.write(accuracy_writer)
        with open(path,"w") as f:
            f.write(subject_writer)
        with open(cgpa_path,"w") as f:
            f.write(cgpa_writer)
        y="True"
    return render(request,"Subject2.html",{"name":name,"y":y,"quiz":quiz_data_json})
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


