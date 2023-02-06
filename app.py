from flask import Flask,render_template,url_for,request
import csv
import pandas as pd
app=Flask(__name__)

storage_list=[]
def csv_to_list():
    with open("people.csv","r") as file :
        global storage_list
        reader=csv.DictReader(file)
        for row in reader:
            storage_list.append(row)
    return storage_list
storage_list=csv_to_list()
print(storage_list)
#Dispalying all the pictures whose salary is lessthan 99000
@app.route('/salary',methods=["GET","POST"])
def salary_less_pictures():
    if request.method == "GET":
        return render_template("salary.html")
    elif request.method=="POST":
        salary=float(request.form.get("input_value"))
        #print(salary)
        #print(salaries)
        temp=[] 
        temp_user=[]
        for i in range(0,len(storage_list)):
            print(storage_list[i]['Salary'])
            if(storage_list[i]['Salary']=='' or storage_list[i]['Salary']==' '):
                continue
            elif(float(storage_list[i]['Salary'])<salary):
                        temp.append(storage_list[i]['Picture'])
                        
        print(temp)
        result_picture=[]
        for x in range(0,len(temp)):
            if(temp[x]==' ' or temp[x]==''):
                continue
            else:
                for i in range(0,len(storage_list)):
                    if(storage_list[i]['Picture']==temp[x]):
                        temp_user.append(storage_list[i]['Name'])
                result_picture.append("/static/pictures/"+temp[x])
    return render_template("get_picture_by_salary.html",get_picture_salary=result_picture,amount=salary,user_list=temp_user,zip=zip)
@app.route('/name',methods=["GET","POST"])
def get_picture_using_name():
     if request.method == "GET":
        return render_template("name.html")
     elif request.method == "POST":
        name = request.form.get("input_value")
        print(name)
        for i in range(0,len(storage_list)):
            temp=storage_list[i]['Name']
            if(temp==name.capitalize()):
                picture_result=storage_list[i]['Picture']
                print(picture_result)
                if(picture_result!=' '):
                    picture_path="/static/pictures/"+picture_result
                    print(picture_path)
                    return render_template("get_picture_by_name.html",picture_by_name=name,picture_path=picture_path);
                else:
                    print("no picture found")
                    return render_template("get_picture_by_name.html",picture_by_name=name,picture_path=None)
        return "user Not Found" 
#######################################
@app.route('/remove/user',methods=["GET","POST"])
def remove_user():
    global storage_list
    storage_list=storage_list
    
    if request.method == "GET":
            list_all_names=[]
            for i in range(0,len(storage_list)):
                list_all_names.append(storage_list[i]['Name'])
            return render_template("deleteuser.html",current_list=list_all_names)
    elif request.method == "POST":
        name = request.form.get("delete_user")
       
        index_to_remove=None
        
        for i,user in enumerate(storage_list):
            if user['Name']==name.capitalize():
                index_to_remove=i
                break
        
        if index_to_remove is not None:
            del storage_list[index_to_remove]
            with open("people.csv","w",newline='')as file:
                writer=csv.DictWriter(file,fieldnames=['Name','State','Salary','Grade','Room','Telnum','Picture','Keywords'])
                writer.writeheader()
                writer.writerows(storage_list)
                print("user deleted and csv file updated")
                storage_list=csv_to_list()
            print(storage_list)
            list_all_names=[]
            for i in range(0,len(storage_list)):
                    list_all_names.append(storage_list[i]['Name'])
            return render_template('deleteusersuccess.html',name=name,current_list=list_all_names)
        
        return "User Not Found"
@app.route('/modify/keyword',methods=["GET","POST"])
def modify_keywords():
    if request.method=="GET":
        temp_user_list=[]
        temp_keywords_list=[]
        for i in range(0,len(storage_list)):
            temp_user_list.append(storage_list[i]['Name'])
            temp_keywords_list.append(storage_list[i]['Keywords'])
        return render_template('modifykeywords.html',user_list=temp_user_list,keywords_list=temp_keywords_list,zip=zip)
    elif request.method=="POST":
        user_name=request.form.get("user_name")
        user_keyword_entry=request.form.get("user_keyword")
        print(user_name)
        print(user_keyword_entry)
        for i in range(0,len(storage_list)):
            if(storage_list[i]['Name']==user_name.capitalize()):
                storage_list[i]['Keywords']=user_keyword_entry
        temp_user_list=[]
        temp_keywords_list=[]
        for i in range(0,len(storage_list)):
            temp_user_list.append(storage_list[i]['Name'])
            temp_keywords_list.append(storage_list[i]['Keywords'])
        return render_template("modifykeywordsuccess.html",user_list=temp_user_list,keywords_list=temp_keywords_list,zip=zip)
    return "keyword Not Updated!!! Try Again!!"
@app.route('/modify/salary',methods=["GET","POST"])
def modify_salary():
    if request.method=="GET":
        temp_user_list=[]
        temp_salary_list=[]
        for i in range(0,len(storage_list)):
            temp_user_list.append(storage_list[i]['Name'])
            temp_salary_list.append(storage_list[i]['Salary'])
        return render_template('modifysalary.html',user_list=temp_user_list,salary_list=temp_salary_list,zip=zip)
    elif request.method=="POST":
        user_name=request.form.get("user_name")
        user_salary_entry=request.form.get("user_salary")
        print(user_name)
        print(user_salary_entry)
        for i in range(0,len(storage_list)):
            if(storage_list[i]['Name']==user_name.capitalize() and pd.isna(float(user_salary_entry))==False):
                storage_list[i]['Salary']=user_salary_entry
        temp_user_list=[]
        temp_salary_list=[]
        for i in range(0,len(storage_list)):
            temp_user_list.append(storage_list[i]['Name'])
            temp_salary_list.append(storage_list[i]['Salary'])
        return render_template("modifysalarysuccess.html",user_list=temp_user_list,salary_list=temp_salary_list,zip=zip)
    return "Salary Not Updated!!! Try Again!!"
# @app.route('add/picture',methods=["GET","POST"])
# def add_picture():
#     if request.method=="GET":
#         temp_user_list=[]
#         for i in range(0,len(storage_list)):
#             temp_user_list.append(storage_list[i]['Name'])
#         return render_template("image.html",list_names=temp_user_list)
#     elif request.method=="POST":
#         user_name=request.form.get("user_name")
#         user_image=request.files["image"]
#         image_dict={}
#         picture_names=[];
#         for x in range(0,len(storage_list)):
#             picture_names.append("/static/pictures/"+storage_list[x]['Picture'])
#         for image_file in picture_names:
#             with open(image_file, "rb") as f:
#                 binary_data = f.read()
#         image_dict[image_file] = binary_data
#         with open("image.jpg", "rb") as image_file:
#             binary_image = image_file.read()
#             if(binary_image==[])
#         binary_img=user_image.rea

# def get_picture_list():
#     picture_list=[];
#     return
@app.route('/')
def home():
    return render_template("home.html")

if __name__=="__main__":
    app.run(debug=True)