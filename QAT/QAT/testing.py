import os
import json
list_of_subjects=["Python.json","C++.json","Django.json","HTML.json","JavaScript.json"]
for i in range(1,13):
    d={}
    for j in range(1,21):
        d[f"Q{str(j)}"]={
        "Heading":"",
        "o1":"",
            "o2":"",
            "o3":"",
            "o4":"",
            "correct_answer":""
        }
    data_dump=json.dumps(d,indent=5)
    for k in list_of_subjects:
        with open("/home/abhinav/PycharmProjects/QAT/QAT/json/"+str(i)+"/"+k,"w") as f:
            f.write(data_dump)
