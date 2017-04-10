from flask import render_template,redirect,url_for,request,g
from app import webapp
import boto3
import os
import vgg16
from vgg16 import vgg16_run
import numpy as np

def compare(x,y):
    if x[0] < y[0]:
        return -1
    elif x[0] > y[0]:
        return 1
    else:
        fil_x = x[2:-4]
        fil_y = y[2:-4]
        if int(fil_x) < int(fil_y):
            return -1
        else:
            return 1

@webapp.route('/image_upload',methods=['GET'])
def image_upload():
    filelist = [f for f in os.listdir("app/static/input")]
    for f in filelist:
        os.remove("app/static/input/"+f)
    filelist = [f for f in os.listdir("app/static/output")]
    for f in filelist:
        os.remove("app/static/output/"+f)    

    return render_template("image/upload.html",title="Upload Image for Testing",image=None,test=0)

@webapp.route('/image_upload',methods=['POST'])
def image_upload_save():
    if 'uploadedfile' not in request.files:
        return redirect(url_for('image_upload'))
    
    new_image = request.files['uploadedfile']
    
    if new_image.filename == "":
        return redirect(url_for('image_upload'))
    
    fname = os.path.join('app/static/input',new_image.filename)
    new_image.save(fname)
    
    return render_template("image/upload.html",title="Image Uploaded",image=fname[17:],test=0)

@webapp.route('/<input>/<needToTest>',methods=['GET'])
def image_test(input,needToTest):
    if needToTest == "1":
        #print("\n\n\nniuniuniu\n\n\n")
        vgg16_run(input)
    
    data = np.load("result.npy") #type: numpy.ndarray
    result = data.tolist() #type: dict
    
    li = os.listdir("app/static/output")
    li.sort(compare)
    
    level1 = []
    for i in [0,1,2,3,4]:
        level1.append(li[i])
    level2 = []
    for i in [5,6,7,8,9]:
        level2.append(li[i])    
    level3 = []
    for i in [10,11,12,13,14]:
        level3.append(li[i])       
    level4 = []
    for i in [15,16,17,18,19]:
        level4.append(li[i])       
    level5 = []
    for i in [20,21,22,23,24]:
        level5.append(li[i])    
    
    return render_template("image/upload.html",title="Test",image=input,test=1,result=result,
                           level1=level1,level2=level2,level3=level3,level4=level4,level5=level5)

@webapp.route('/<input>/<output>/view',methods=['GET'])
def result_view(input,output):
    return render_template("image/view.html",title="Level-" + output[0] + " Filter-" + output[2:-4],image=input,result=output)

@webapp.route('/train',methods=['GET'])
def train():
    return render_template("image/train.html",title="Custom CNN")

#@webapp.route('/network',methods=['GET'])
#def network_view():
    #path = os.path.join(os.getcwd(),"app/static/output")
    #images = os.listdir(path)
    #return render_template("image/network.html",title="Network View",images=images)

#@webapp.route('/<image>',methods=['GET'])
#def image_view(image):
    #return render_template("image/view.html",title="Image View",image=image)