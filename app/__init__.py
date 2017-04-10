from flask import Flask

webapp = Flask(__name__)

#import os
#os.system("pip install tensorflow")
#os.system("pip install scipy")
#os.system("pip install matplotlib")

from app import vgg16
from app import image
from app import main

