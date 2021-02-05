from flask import Flask
from flask import request,render_template,redirect
import json
app=Flask(__name__)
# Home page routing and functionality
@app.route("/",methods=["POST","GET"])
def index():
    name=request.form.get("name")
    email=request.form.get("email")
    subject=request.form.get("subject")
    message=request.form.get("message")
    d={}
    if name=="" or name==None:
        d={}
    else:
        data=open("messages.json")
        data_json=json.load(data)
        d=data_json
        l=list(reversed(list(data_json.keys())))
        if len(l)>0:
            if (data_json[l[0]]["Name"]==name and data_json[l[0]]["Subject"]==subject
            and data_json[l[0]]["Message"]==message
            ):
                pass
            else:
                d[f"{len(l)+1}"]={"Name":name,"Email":email,"Subject":subject,"Message":message}
        else:
            d["1"]={"Name":name,"Email":email,"Subject":subject,"Message":message}
        writer=json.dumps(d,indent=5)
        with open("messages.json","w") as out:
            out.write(writer)
    post_add=json.load(open("post.json"))
    art={}
    paint={}
    wall={}
    mehndi={}
    for i in (reversed(list((post_add["Art_Craft"].keys())))):
        art[i]=post_add["Art_Craft"][i]
    for i in (reversed(list((post_add["Painting"].keys())))):
        paint[i]=post_add["Painting"][i]
    for i in reversed((list((post_add["Mehndi"].keys())))):
        mehndi[i]=post_add["Mehndi"][i]
    for i in reversed((list((post_add["Wall_Decor"].keys())))):
        wall[i]=post_add["Wall_Decor"][i]
    print(art)
    return render_template("index.html",art=art,paint=paint,wall=wall,mehndi=mehndi)
# Messages page routing and functionaliy
@app.route("/m")
def message():
    d=open("messages.json")
    d_json=json.load(d)
    l=list(reversed(list(d_json.keys())))
    x={}
    for i in l:
        x[i]=d_json[i]
    print(x)
    return render_template("message.html",x=x)
@app.route("/update",methods=["POST","GET"])
def update():
    if request.method=="POST":
        title=request.form.get("title")
        link=request.form.get("link")
        type=request.form.get("type")
        data_json=json.load(open('post.json'))
        data_json[type][len(list(data_json[type].keys()))+1]={'title':title,'link':link}
        writer=json.dumps(data_json,indent=6)
        with open("post.json","w") as opt:
            opt.write(writer)
        return "Hello<br><a href='/update'>Add One More Post</a><br><a href='/'>Home Page</a>"
    else:
        return render_template("update.html")
app.run(debug=True)
