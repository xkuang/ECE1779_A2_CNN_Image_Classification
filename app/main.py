from flask import render_template,redirect,url_for,request
from app import webapp
import boto3

dynamodb = boto3.resource("dynamodb",region_name="us-east-1")

@webapp.route('/',methods=['GET'])
def main():
    return render_template("signin.html",error=None)

@webapp.route('/loading/<image>',methods=['GET'])
def load(image):
    return render_template("load.html",image=image)

@webapp.route('/signin',methods=['POST'])
def signin():
    username = request.form.get("inputUsername","")
    password = request.form.get("inputPassword","")
    
    table = dynamodb.Table("users")
    response = table.get_item(
        Key={
            "username": username
        },
        ProjectionExpression = "password"
    )
    if "Item" not in response:
        return render_template("signin.html",error="Username is not existed!")
    
    item = response["Item"] # type = dict
    if item["password"] != password:
        return render_template("signin.html",error="Wrong password!")
    
    return redirect(url_for('image_upload'))

@webapp.route('/signup',methods=['GET'])
def signup():
    return render_template("signup.html",error=None)

@webapp.route('/signup',methods=['POST'])
def signup_save():   
    username = request.form.get("inputUsername","")
    password = request.form.get("inputPassword","")
    
    table = dynamodb.Table("users")
    response = table.get_item(
        Key={
            "username": username
        }
    )
    if "Item" in response:
        return render_template("signup.html",error="Username is existed!")
    
    response = table.put_item(
        Item={
            "username": username,
            "password": password
        }
    )
    
    return render_template("signin.html",error=None)