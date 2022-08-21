from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pymongo
from flask_mail import Mail,Message
app = Flask(__name__)

model = pickle.load(open('modelA.pkl', 'rb'))
client = pymongo.MongoClient("mongodb+srv://agrawalutkarsh:vjur09052628@cluster0.vritj4x.mongodb.net/?retryWrites=true&w=majority")
# mongodb+srv://agrawalutkarsh:vjur09052628@cluster0.vritj4x.mongodb.net/?retryWrites=true&w=majority

app.config['DEBUG']=True
app.config['TESTING']=False
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
app.config['MAIL_USERNAME']='ua8019@srmist.edu.in'
app.config['MAIL_PASSWORD']='@Ua470123'
app.config['MAIL_DEFAULT_SENDER']=('ua8019@srmist.edu.in')
app.config['MAIL_MAX_EMAILS']=None
app.config['MAIL_ASCII_ATTACHMENTS']= False

mail=Mail(app)

@app.route('/')
def home():
    return render_template('index.html')
@app.route("/practice")
def practice():
    """ return the rendered template """
    return render_template("practice.html")
@app.route("/practice1")
def practice1():
    """ return the rendered template """
    return render_template("practice1.html")

@app.route('/predict3',methods=['POST'])
def predict3():
   if request.method=='POST':
       name = request.form.get("name")
       text = request.form.get("Feed")
       # print(name)
       # print(text)
       data = {
           'Name': name,
           'Feedback': text
       }
   with client:
        db = client.Anxiety
        db.CANX.insert_one(data)

   return render_template('index.html')

@app.route('/predict5',methods=['POST'])
def predict5():
    int_features = [x for x in request.form.values()]
    l = []
    #['S ADITYA', 's.aditya04042001@gmail.com', '21/07/2001', '9:00 to 10:00', ' Child psychiatrist', '']
    for i in range(len(int_features)-1):
        l.append(int_features[i])
    name=l[0]
    email=l[1]
    date=l[2]
    time=l[3]
    department=l[4]
    msg = Message('Anxiety Detection', recipients=[email])
    msg.html = 'MESSAGE FROM Anxiety Detection!'+'<br><br</br></br>'+"<br>Name : </br>"+name+'\n'+"<br>Department : </br>"+department+'\n'+"<br>Date : </br>"+date+'\n'+"<br>Time : </br>"+time+'\n'+'<br><br</br></br>'+"<br> join in this meet  at suitable slot</br>"+'<br>https://meet.google.com/cjo-raps-jwf</br>'
    mail.send(msg)
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    import random

    int_features = [ x for x in request.form.values()]
    l=[]
    int_features = int_features[1:-2]
    for i in range(len(int_features)-1):
        l.append(int_features[i+1])
    l = [int(i) for i in l]
    final_features = [np.array(l)]

    if random.randint(0, 1) == 0:
        output='YES'
    else:
        output = 'NO'

    return render_template('practice1.html', prediction_text='DO I HAVE ANXIETY ? {}'.format(output))


@app.route('/predict1_api',methods=['POST'])
def predict1_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model1.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == '__main__':
    app.run()
