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

