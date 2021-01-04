# importing all the modules---------------------
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
import pdfkit
# -------------------------------------------------------
# quiz link that we have to make active
quiz_link="2"
# -------------------------------------------------------
# Authentication part of the app----------------------------------------
def login(request):
    registration_details=list(Registration.objects.all())
    username_list=[]
    email_list=[]
    login_dict={}
    social_username=[]
    social_email=[]
    l=list(User.objects.all())
    for i in l:
        social_username.append(i.username)
        social_email.append(i.email)
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
            elif username in social_username:
                return render(request, "index.html", {'message': "Username Already Exist"})
            elif email in social_email:
                return render(request, "index.html", {"message": "Email Already registered"})
            elif email in email_list:
                return render(request,"index.hmtl",{"message":"Email Already registered"})
            else:
                Registration(name=name,email=email,username=username,password=password).save()
                u=User.objects.create_user(username,email,password)
                u.first_name=name
                u.save()
        if username_lgn!="default":
            try:
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
            except:
                return HttpResponse("I think the username and email id you are using is already registered and using it twice")
    return render(request,"index.html",{"message":""})
# --------------------------------------------------------------------------------
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
            "overall_cgpa":[0,0,0,0,0,0,0,0,0,0,0,0]
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


    #     creating the rank list
        rank_dict=json.load(open("/home/abhinav/PycharmProjects/QAT/QAT/json/rank_list.json"))
        rank_dictionary=rank_dict
        rank_dictionary[username]=[]
        writter=json.dumps(rank_dictionary,indent=5)
        with open("/home/abhinav/PycharmProjects/QAT/QAT/json/rank_list.json","w") as f:
            f.write(writter)
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
        cgpa=sum(cgpa_data_json["overall_cgpa"])/int(quiz_link)
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
    return render(request,"dash.html",{"username":str(request.user),"name":name,"cg":cgpa,"cgh":cgpa_highest,"accuracy":accuracy,"test":test,"l":listy})
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
    rank_path="/home/abhinav/PycharmProjects/QAT/QAT/json/rank_list.json"
    rank_data=json.load(open(rank_path))
    rank_dict=rank_data
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
        rank_dict[username].append((count/20)*10)
        rank_writter=json.dumps(rank_dict,indent=5)
        cgpa_dummy[quiz_link]=l_cgpa
        cgpa_dummy["overall_cgpa"][int(quiz_link)-1]=(sum(l_cgpa)/5)
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
        with open(rank_path,"w") as f:
            f.write(rank_writter)
        y="True"
    return render(request,"Subject1.html",{"username":str(request.user),"name":name,"y":y,"quiz":quiz_data_json})

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
    rank_path="/home/abhinav/PycharmProjects/QAT/QAT/json/rank_list.json"
    rank_data=json.load(open(rank_path))
    rank_dict=rank_data
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
        rank_dict[username].append((count / 20) * 10)
        rank_writter = json.dumps(rank_dict, indent=5)
        l_cgpa=cgpa_dummy[quiz_link]
        l_cgpa.append((count/20)*10)
        cgpa_dummy[quiz_link]=l_cgpa
        cgpa_dummy["overall_cgpa"][int(quiz_link)-1]=(sum(l_cgpa)/5)
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
        with open(rank_path,"w") as f:
            f.write(rank_writter)
        y="True"
    return render(request,"Subject2.html",{"username":str(request.user),"name":name,"y":y,"quiz":quiz_data_json})

@login_required(login_url="/login")
def subject3(request):
    global quiz_link
    username = str(request.user)
    # commenting for the path(All the paths will be here)
    path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/Django.json"
    quiz_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/{quiz_link}/Django.json"
    cgpa_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/cgpa.json"
    accuracy_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/accuracy.json"
    test_given_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/test_given.json"
    rank_path="/home/abhinav/PycharmProjects/QAT/QAT/json/rank_list.json"
    rank_data=json.load(open(rank_path))
    rank_dict=rank_data
    # Processing the paths here
    quiz_data = open(quiz_path)
    quiz_data_json = json.load(quiz_data)
    subject_data = open(path)
    subject_data_json = json.load(subject_data)
    subject_dummy = subject_data_json
    cgpa_json = open(cgpa_path)
    cgpa_json_data = json.load(cgpa_json)
    cgpa_dummy = cgpa_json_data
    accuracy_json = open(accuracy_path)
    accuracy_json_data = json.load(accuracy_json)
    accuracy_dummy = accuracy_json_data
    test_given_json = open(test_given_path)
    test_given_json_data = json.load(test_given_json)
    test_given_dummy = test_given_json_data
    y = ""
    if subject_data_json[quiz_link]["submitted"] == True:
        y = "True"
    name = str(request.user.get_full_name())
    if str(request.user) == "QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    if request.method == "POST" and y == "":
        print("Yes")
        count = 0
        for i in range(1, 21):
            option_selected = request.POST.get(f"Q{str(i)}", "")
            if option_selected.lower() == quiz_data_json[f"Q{str(i)}"]["correct_answer"]:
                count = count + 1
            else:
                pass
        subject_dummy[quiz_link]["correct"] = count
        subject_dummy[quiz_link]["wrong"] = 20 - count
        subject_dummy[quiz_link]["accuracy"] = (count / 20) * 100
        subject_dummy[quiz_link]["submitted"] = True
        subject_dummy[quiz_link]["cgpa"] = (count / 20) * 10
        accuracy_dummy["Django"].append((count / 20) * 100)
        accuracy_json_data["accuracy"].append((count / 20) * 100)
        test_given_dummy["Test_Given"] = test_given_dummy["Test_Given"] + 1
        l_cgpa = cgpa_dummy[quiz_link]
        l_cgpa.append((count / 20) * 10)
        rank_dict[username].append((count / 20) * 10)
        rank_writter = json.dumps(rank_dict, indent=5)
        cgpa_dummy[quiz_link] = l_cgpa
        cgpa_dummy["overall_cgpa"][int(quiz_link)-1]=(sum(l_cgpa)/5)
        cgpa_dummy["Django"].append((count / 20) * 10)
        cgpa_writer = json.dumps(cgpa_dummy, indent=6)
        subject_writer = json.dumps(subject_dummy, indent=6)
        accuracy_writer = json.dumps(accuracy_dummy, indent=6)
        test_given_writer = json.dumps(test_given_dummy, indent=4)
        with open(test_given_path, "w") as f:
            f.write(test_given_writer)
        with open(accuracy_path, "w") as f:
            f.write(accuracy_writer)
        with open(path, "w") as f:
            f.write(subject_writer)
        with open(cgpa_path, "w") as f:
            f.write(cgpa_writer)
        with open(rank_path,"w") as f:
            f.write(rank_writter)
        y = "True"
    return render(request, "Subject3.html", {"username":str(request.user),"name": name, "y": y, "quiz": quiz_data_json})
c=""
@login_required(login_url="/login")
def subject4(request):
    global quiz_link
    username = str(request.user)
    # commenting for the path(All the paths will be here)
    path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/HTML.json"
    quiz_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/{quiz_link}/HTML.json"
    cgpa_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/cgpa.json"
    accuracy_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/accuracy.json"
    test_given_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/test_given.json"
    rank_path="/home/abhinav/PycharmProjects/QAT/QAT/json/rank_list.json"
    rank_data=json.load(open(rank_path))
    rank_dict=rank_data
    # Processing the paths here
    quiz_data = open(quiz_path)
    quiz_data_json = json.load(quiz_data)
    subject_data = open(path)
    subject_data_json = json.load(subject_data)
    subject_dummy = subject_data_json
    cgpa_json = open(cgpa_path)
    cgpa_json_data = json.load(cgpa_json)
    cgpa_dummy = cgpa_json_data
    accuracy_json = open(accuracy_path)
    accuracy_json_data = json.load(accuracy_json)
    accuracy_dummy = accuracy_json_data
    test_given_json = open(test_given_path)
    test_given_json_data = json.load(test_given_json)
    test_given_dummy = test_given_json_data
    y = ""
    if subject_data_json[quiz_link]["submitted"] == True:
        y = "True"
    name = str(request.user.get_full_name())
    if str(request.user) == "QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    if request.method == "POST" and y == "":
        print("Yes")
        count = 0
        for i in range(1, 21):
            option_selected = request.POST.get(f"Q{str(i)}", "")
            if option_selected.lower() == quiz_data_json[f"Q{str(i)}"]["correct_answer"]:
                count = count + 1
            else:
                pass
        subject_dummy[quiz_link]["correct"] = count
        subject_dummy[quiz_link]["wrong"] = 20 - count
        subject_dummy[quiz_link]["accuracy"] = (count / 20) * 100
        subject_dummy[quiz_link]["submitted"] = True
        subject_dummy[quiz_link]["cgpa"] = (count / 20) * 10
        accuracy_dummy["HTML"].append((count / 20) * 100)
        accuracy_json_data["accuracy"].append((count / 20) * 100)
        test_given_dummy["Test_Given"] = test_given_dummy["Test_Given"] + 1
        l_cgpa = cgpa_dummy[quiz_link]
        l_cgpa.append((count / 20) * 10)
        rank_dict[username].append((count / 20) * 10)
        rank_writter = json.dumps(rank_dict, indent=5)
        cgpa_dummy[quiz_link] = l_cgpa
        cgpa_dummy["overall_cgpa"][int(quiz_link) - 1] = (sum(l_cgpa) / 5)
        cgpa_dummy["HTML"].append((count / 20) * 10)
        cgpa_writer = json.dumps(cgpa_dummy, indent=6)
        subject_writer = json.dumps(subject_dummy, indent=6)
        accuracy_writer = json.dumps(accuracy_dummy, indent=6)
        test_given_writer = json.dumps(test_given_dummy, indent=4)
        with open(test_given_path, "w") as f:
            f.write(test_given_writer)
        with open(accuracy_path, "w") as f:
            f.write(accuracy_writer)
        with open(path, "w") as f:
            f.write(subject_writer)
        with open(cgpa_path, "w") as f:
            f.write(cgpa_writer)
        with open(rank_path,"w") as f:
            f.write(rank_writter)
        y = "True"
    return render(request, "Subject4.html", {"username":str(request.user),"name": name, "y": y, "quiz": quiz_data_json})
d=""
@login_required(login_url="/login")
def subject5(request):
    global quiz_link
    username = str(request.user)
    # commenting for the path(All the paths will be here)
    path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/JavaScript.json"
    quiz_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/{quiz_link}/JavaScript.json"
    cgpa_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/cgpa.json"
    accuracy_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/accuracy.json"
    test_given_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/test_given.json"
    rank_path="/home/abhinav/PycharmProjects/QAT/QAT/json/rank_list.json"
    rank_data=json.load(open(rank_path))
    rank_dict=rank_data
    # Processing the paths here
    quiz_data = open(quiz_path)
    quiz_data_json = json.load(quiz_data)
    subject_data = open(path)
    subject_data_json = json.load(subject_data)
    subject_dummy = subject_data_json
    cgpa_json = open(cgpa_path)
    cgpa_json_data = json.load(cgpa_json)
    cgpa_dummy = cgpa_json_data
    accuracy_json = open(accuracy_path)
    accuracy_json_data = json.load(accuracy_json)
    accuracy_dummy = accuracy_json_data
    test_given_json = open(test_given_path)
    test_given_json_data = json.load(test_given_json)
    test_given_dummy = test_given_json_data
    y = ""
    if subject_data_json[quiz_link]["submitted"] == True:
        y = "True"
    name = str(request.user.get_full_name())
    if str(request.user) == "QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    if request.method == "POST" and y == "":
        print("Yes")
        count = 0
        for i in range(1, 21):
            option_selected = request.POST.get(f"Q{str(i)}", "")
            if option_selected.lower() == quiz_data_json[f"Q{str(i)}"]["correct_answer"]:
                count = count + 1
            else:
                pass
        subject_dummy[quiz_link]["correct"] = count
        subject_dummy[quiz_link]["wrong"] = 20 - count
        subject_dummy[quiz_link]["accuracy"] = (count / 20) * 100
        subject_dummy[quiz_link]["submitted"] = True
        subject_dummy[quiz_link]["cgpa"] = (count / 20) * 10
        accuracy_dummy["JavaScript"].append((count / 20) * 100)
        accuracy_json_data["accuracy"].append((count / 20) * 100)
        test_given_dummy["Test_Given"] = test_given_dummy["Test_Given"] + 1
        rank_dict[username].append((count / 20) * 10)
        rank_writter = json.dumps(rank_dict, indent=5)
        l_cgpa = cgpa_dummy[quiz_link]
        l_cgpa.append((count / 20) * 10)
        cgpa_dummy[quiz_link] = l_cgpa
        cgpa_dummy["overall_cgpa"][int(quiz_link) - 1] = (sum(l_cgpa) / 5)
        cgpa_dummy["JavaScript"].append((count / 20) * 10)
        cgpa_writer = json.dumps(cgpa_dummy, indent=6)
        subject_writer = json.dumps(subject_dummy, indent=6)
        accuracy_writer = json.dumps(accuracy_dummy, indent=6)
        test_given_writer = json.dumps(test_given_dummy, indent=4)
        with open(test_given_path, "w") as f:
            f.write(test_given_writer)
        with open(accuracy_path, "w") as f:
            f.write(accuracy_writer)
        with open(path, "w") as f:
            f.write(subject_writer)
        with open(cgpa_path, "w") as f:
            f.write(cgpa_writer)
        with open(rank_path,"w") as f:
            f.write(rank_writter)
        y = "True"
    return render(request, "Subject5.html", {"username":str(request.user),"name": name, "y": y, "quiz": quiz_data_json})
@login_required(login_url="/login")
def result(request):
    global quiz_link
    username=str(request.user)
    name = str(request.user.get_full_name())
    if str(request.user)=="QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    cgpa_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/cgpa.json"
    python_score=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/Python.json"
    c_score=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/C++.json"
    django_score=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/Django.json"
    html_score=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/HTML.json"
    js_score=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/JavaScript.json"
    cgpa_data=json.load(open(cgpa_path))
    python_data=json.load(open(python_score))
    c_data=json.load(open(c_score))
    django_data=json.load(open(django_score))
    html_data=json.load(open(html_score))
    js_data=json.load(open(js_score))
    cgpa={}
    python={}
    c={}
    django={}
    html={}
    js={}
    if cgpa_data["overall_cgpa"]==[]:
        for i in range(1,13):
            cgpa[i]="--"
    else:
        for i in range(1,13):
            if i<=int(quiz_link):
                try:
                    cgpa[i]=cgpa_data["overall_cgpa"][i-1]
                except:
                    cgpa[i]="--"
            else:
                cgpa[i]="--"
    for i in range(1,13):
        if i<=int(quiz_link):
            python[i]=python_data[str(i)]["correct"]
            c[i]=c_data[str(i)]["correct"]
            django[i]=django_data[str(i)]["correct"]
            html[i]=html_data[str(i)]["correct"]
            js[i]=js_data[str(i)]["correct"]
        else:
            python[i]="--"
            c[i]="--"
            django[i]="--"
            html[i]="--"
            js[i]="--"
    return render(request,"Result.html",{"username":username,"name":name,"cgpa":cgpa,"python":python,"c":c,"django":django,"html":html,"js":js})
# added
@login_required(login_url="/login")
def analysis(request):
    global quiz_link
    username=str(request.user)
    name = str(request.user.get_full_name())
    if str(request.user)=="QAT":
        lgt(request)
        return HttpResponseRedirect("/")
    # path to files
    cgpa_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/cgpa.json"
    python_score=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/Python.json"
    c_score=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/C++.json"
    django_score=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/Django.json"
    html_score=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/HTML.json"
    js_score=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/JavaScript.json"
    accuracy_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/accuracy.json"
    # loading the data
    python_data=json.load(open(python_score))
    c_data=json.load(open(c_score))
    django_data=json.load(open(django_score))
    html_data=json.load(open(html_score))
    js_data=json.load(open(js_score))
    cgpa_data=json.load(open(cgpa_path))
    accuracy_data=json.load(open(accuracy_path))
    python_cgpa=0
    c_cgpa=0
    django_cgpa=0
    html_cgpa=0
    js_cgpa=0
    if cgpa_data["Python"]==[]:
        python_cgpa=0
    else:
        python_cgpa=sum(cgpa_data["Python"])/(len(cgpa_data["Python"]))
    if cgpa_data["C++"] == []:
        c_cgpa = 0
    else:
        c_cgpa = sum(cgpa_data["C++"]) / (len(cgpa_data["C++"]))
    if cgpa_data["Django"] == []:
        django_cgpa = 0
    else:
        django_cgpa = sum(cgpa_data["Django"]) / (len(cgpa_data["Django"]))
    if cgpa_data["HTML"] == []:
        html_cgpa = 0
    else:
        html_cgpa = sum(cgpa_data["HTML"]) / (len(cgpa_data["HTML"]))
    if cgpa_data["JavaScript"] == []:
        js_cgpa = 0
    else:
        js_cgpa = sum(cgpa_data["JavaScript"]) / (len(cgpa_data["JavaScript"]))
    python_list=[]
    c_list=[]
    django_list=[]
    html_list=[]
    js_list=[]
    for i in range(1,13):
        python_list.append("{"+f'y: {str(python_data[str(i)]["correct"])},label:"{str(i)}"'+"},")
        c_list.append("{ y:" + f'{c_data[str(i)]["correct"]},label:"{str(i)}"' + "},")
        django_list.append("{ y:" + f'{django_data[str(i)]["correct"]},label:"{str(i)}"' + "},")
        html_list.append("{ y:" + f'{html_data[str(i)]["correct"]},label:"{str(i)}"' + "},")
        js_list.append("{ y:" + f'{js_data[str(i)]["correct"]},label:"{str(i)}"' + "},")
    py_acc=0
    c_acc=0
    django_acc=0
    html_acc=0
    js_acc=0
    if len(accuracy_data["Python"])==[]:
        py_acc=0
    else:
        try:
            py_acc=sum(accuracy_data["Python"])/(len(accuracy_data["Python"]))
        except:
            py_acc=0
    if len(accuracy_data["C++"]) == []:
        c_acc=0
    else:
        try:
            c_acc = sum(accuracy_data["C++"]) / (len(accuracy_data["C++"]))
        except:
            c_acc=0
    if len(accuracy_data["Django"])==[]:
        django_acc=0
    else:
        try:
            django_acc = sum(accuracy_data["Django"]) / (len(accuracy_data["Django"]))
        except:
            django_acc=0
    if len(accuracy_data["HTML"]) == []:
        html_acc=0
    else:
        try:
            html_acc = sum(accuracy_data["HTML"]) / (len(accuracy_data["HTML"]))
        except:
            html_acc=0
    if len(accuracy_data["JavaScript"]) == []:
        js_acc=0
    else:
        try:
            js_acc = sum(accuracy_data["JavaScript"]) / (len(accuracy_data["JavaScript"]))
        except:
            js_acc=0
    rank_path="/home/abhinav/PycharmProjects/QAT/QAT/json/rank_list.json"
    rank_data=json.load(open(rank_path))
    l=sorted(rank_data,key=lambda x:sum(rank_data[x]),reverse=True)
    index=l.index(username)+1
    return render(request,"Analysis.html",{"username":str(request.user),"name":name,"python_gp":python_cgpa,"c_gp":c_cgpa,"django_gp":django_cgpa,"html_gp":html_cgpa,"js_gp":js_cgpa,"python_list":python_list,"c_list":c_list,
                                           "django_list":django_list,"html_list":html_list,"js_list":js_list,
                                           "py_acc":py_acc,"c_acc":c_acc,"django_acc":django_acc,"html_acc":html_acc,"js_acc":js_acc,"index":index
                                           })
@login_required(login_url="/login")
def report(request):
    username=str(request.user)
    Python_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/Python.json"
    c_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/C++.json"
    django_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/Django.json"
    html_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/HTML.json"
    js_path = f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/JavaScript.json"
    cgpa_path=f"/home/abhinav/PycharmProjects/QAT/QAT/json/user/{username}/cgpa.json"
    python_data=json.load(open(Python_path))
    c_data=json.load(open(c_path))
    django_data=json.load(open(django_path))
    html_data=json.load(open(html_path))
    js_data=json.load(open(js_path))
    cgpa_data=json.load(open(cgpa_path))
    cgpa_series=cgpa_data["overall_cgpa"][int(quiz_link)-1]
    ovcgpa=sum(cgpa_data["overall_cgpa"][:int(quiz_link)])/int(quiz_link)
    rank_path="/home/abhinav/PycharmProjects/QAT/QAT/json/rank_list.json"
    rank_data=json.load(open(rank_path))
    l=sorted(rank_data,key=lambda x:sum(rank_data[x]),reverse=True)
    index=l.index(username)+1
    text = f"<div style='text-align:center'><img src='/home/abhinav/PycharmProjects/QAT/QAT/static/logo.png'></div><h1 style='text-align:center;color:red;background-color:black'>QAT Result<br>Project Report Test Series {quiz_link} <br>Name:{str(request.user.get_full_name())}<br>Username:{username}</h1>" \
           f"<div style='text-align:center;background-color:grey'><br><h1>Marks</h1><p>Python:{python_data[quiz_link]['correct']}/20 with accuracy {python_data[quiz_link]['accuracy']}</p><p>C++:{c_data[quiz_link]['correct']}/20 with accuracy {c_data[quiz_link]['accuracy']}</p>" \
           f"<p>Django:{django_data[quiz_link]['correct']}/20 with accuracy {django_data[quiz_link]['accuracy']}</p><p>HTML:{html_data[quiz_link]['correct']}/20 with accuracy {html_data[quiz_link]['accuracy']}</p><p>JavaScript:{js_data[quiz_link]['correct']}/20 with accuracy {js_data[quiz_link]['accuracy']}</p><br></div>" \
           f"<div style='text-align:center;background-color:red'><h1>CGPA of series link {quiz_link}: {cgpa_series}</h1><h1>Overall Cgpa : {ovcgpa} </h1><h1>Rank:{index}</h1><br><br><h1>Signature</h1></div>"
    pdfkit.from_string(text,f"/home/abhinav/PycharmProjects/QAT/QAT/static/{username}.pdf")
    link="{% static '"+username+".pdf' %}"
    print(link)
    return render(request,"report.html",{"username":f"{username}.pdf","link":str(link)})

