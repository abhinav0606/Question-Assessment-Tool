# import os
# import json
# list_of_subjects=["Python.json","C++.json","Django.json","HTML.json","JavaScript.json"]
# for i in range(1,13):
#     d={}
#     for j in range(1,21):
#         d[f"Q{str(j)}"]={
#         "Heading":"",
#         "o1":"",
#             "o2":"",
#             "o3":"",
#             "o4":"",
#             "correct_answer":""
#         }
#     data_dump=json.dumps(d,indent=5)
#     for k in list_of_subjects:
#         with open("/home/abhinav/PycharmProjects/QAT/QAT/json/"+str(i)+"/"+k,"w") as f:
#             f.write(data_dump)

text="<h1 style='text-align:center;color:red;background-color:black'>QAT Result<br>Project Report Test Series 2 <br>Name:Abhinav Gangrade<br>Username:abhinav0606</h1>" \
     "<div style='text-align:center;background-color:grey'><br><h1>Marks</h1><p>Python:</p><p>C++:</p>" \
     "<p>Django:</p><p>HTML:</p><p>JavaScript:</p><br></div>" \
     "<div style='text-align:center;background-color:red'><h1>Overall CGPA:</h1><h1>Rank:</h1><br><br><h1>Signature</h1></div>"
import pdfkit
pdfkit.from_string(text,'shaurya.pdf')
