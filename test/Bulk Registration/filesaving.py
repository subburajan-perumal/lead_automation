from flask import Flask, render_template, request,jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import pymongo
import json
from datetime import datetime
from json import loads

app = Flask (__name__)

@app.route('/upload')
def upload_file():
    return render_template("upload.html")


@app.route("/uploader", methods=["GET","POST"])
def uploader_file():
    if request.method == "POST":
        f = request.files['file']
        client = pymongo.MongoClient("mongodb://REDACTED_MONGO_URI")
        db = client["Bulk_Lead"]
        df = pd.read_csv(f)
        data = df.to_dict(orient="records")
        for val in data:
            val['created_time'] = datetime.now()
            val['source'] = 'bulk_upload'
            db.practice.insert_one(val)
    
        # db.practice.insert_many(data)
 
        return 'succesfully added to Mongodb'

@app.route('/list', methods=['GET','Post'])
def list():
        try:
            client = pymongo.MongoClient("mongodb://REDACTED_MONGO_URI")
            db = client["Bulk_Lead"]
            x=[]
            cur = db.practice.find()
            for i in cur:
                x.append(i)
            return render_template('list.html', x=x)
        except Exception as e:
            return jsonify({"Status": "Error", "Error": str(e)})

if __name__ == '__main__':
    app.run()
    