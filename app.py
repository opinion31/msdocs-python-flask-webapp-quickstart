import os
from service.blob import *
from service.cosmos import *
from datetime import datetime
import time
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for,send_file)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

@app.route('/cosmos/get', methods=['GET'])
def getCosmosData():

    container = "nhbank-dev"
    resultlist = getCosmosList(container)
    return render_template('cosmosread.html',list = resultlist)

@app.route('/cosmos/write',methods=['POST'])
def setCosmosData():

    container = "cxp-list"
    writeDict = {}
    writeDict['name'] = request.form.get('name')
    writeDict['message'] = request.form.get('message')
    writeDict['Date'] = datetime.now().strftime("%Y-%m-%d")
    writeCosmos(container,writeDict)
    time.sleep(1)
    resultlist = getCosmosList(container)
    return render_template('cosmosread.html',list = resultlist)

@app.route('/blob/get',methods=['GET'])
def getblobData():
    container = "network"
    resultlist = getBlobList(container)
    return render_template('blobread.html',list = resultlist)

@app.route('/blob/upload',methods=['POST'])
def uploadBlob():
    fileList = request.files.getlist('File')
    container = "network"
    for file in fileList :
        upload_file_to_blob(file,container,file.filename)
    time.sleep(2)
    resultlist = getBlobList(container)
    return render_template('blobread.html',list = resultlist)

@app.route('/blob/download',methods=['POST'])
def downloadBlob():
    container = "network"
    blobname = request.form.get('blobname')
    file_stream = download_blob(container,blobname)
    return send_file(file_stream, as_attachment=True, download_name=blobname)

@app.route('/blob/sas',methods=['GET'])
def getSASUrl():
    return "Y"

if __name__ == '__main__':
   app.run()
