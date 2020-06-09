

import numpy as np
import os
from keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
global graph
graph = tf.get_default_graph()
from flask import Flask , request,url_for, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
model = load_model("rock.h5")

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/frm')
def frm():
    return render_template('base.html')


@app.route('/predict',methods = ['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']
        print("current path")
        basepath = os.path.dirname(__file__)
        print("current path", basepath)
        filepath = os.path.join(basepath,'uploads',f.filename)
        print("upload folder is ", filepath)
        f.save(filepath)
        
        img = image.load_img(filepath,target_size = (64,64))
        x = image.img_to_array(img)
        x = np.expand_dims(x,axis =0)
        
        with graph.as_default():
            preds = model.predict_classes(x)
            4
            
            print("prediction",preds)
            
        index=['Basalt(Igneous)   Uses- Basalt is used in construction, making cobblestones and in making statues', 
               'Marble(Metapher)   Uses- Marble is used in Buildings and Sculptures,Brightener, Filler, Pigment etc..',
               'Slate (Metapher)   Uses- Slate is used in  roofing, flooring, and flagging because of its durability and attractive appearance.',
               'liginite(Sedimentary)   Uses- Liginite is used in Electricity Generation,Synthetic Natural Gas Generation,Home Heating, Fertilizer and Oil Well Drilling Mud',
               'nephline(Igneous)   Uses- Nephline is used in  geological clues to environment of formation,refractories, glass making, ceramics and, in pigments and fillers.']
        
        text = "The Predicted Rock is : " + str(index[preds[0]])
        
    return text
if __name__ == '__main__':
    app.run(debug = True, threaded = False)
        
        
        
    
    
