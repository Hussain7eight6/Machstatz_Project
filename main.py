from flask import Flask,jsonify,render_template,request,redirect,url_for
import traceback
import requests
import json
app=Flask(__name__)
name_list=[]

response_fetch=requests.get('http://3.6.93.159:7883/machstatz/get_all_users')
dict={"name":"","email":""}
for items in response_fetch.json():
    dict["name"]=items["fist_name"]+" "+items["last_name"]
    dict["email"]=items["email"]
    name_list.append(dict)
length=len(name_list)

@app.route("/")
def home():
    return render_template('screen_1.html')


@app.route("/machstatz")
def existing_user():
    return render_template('delete_existing_user.html',length=length,name_list=name_list)


@app.route("/machstatz/add_new_user",methods=['GET','POST'])
def add_new_user():
    resp={"email":"","fist_name":"","last_name":"","pwd":"","username":""}
    response={"message":"Created the new user successfully.","status":"Success"}
    if request.method=="POST":
        resp["email"]=request.form["email"]
        resp["fist_name"]=request.form["fname"]
        resp["last_name"]=request.form["lname"]
        resp["pwd"]=request.form["pwd"]
        resp["username"]=request.form["username"]
        for items in response_fetch.json():
            if items["email"]==resp["email"]:
                response["message"]="User with provided email or username is already exist."
                response["status"]="Error"
    return response


@app.route("/machstatz/delete_existing_user")
def delete_existing_user():
    response={"message":"Unable to delete the user or user may not exist.","status":"Error"}
    if request.method=="POST":
        enterd_email=request.form["email"]   #(This email needs to be used to delete the user from database which we dont have access to)
        for item in name_list():
            if enterd_email==item["email"]:
                name_list.remove(item)
                response["message"]="User deleted successfully."
                response["status"]="Deleted"
                
    return response
    


if __name__=='__main__':
    app.run(debug=False,host='0.0.0.0')


