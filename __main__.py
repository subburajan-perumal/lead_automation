from flask import Flask, request, abort, json
from flask_sqlalchemy import SQLAlchemy
from data import all_sites
from functions_ import *
from data import constants
from function import alliance


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = constants.db_path
db = SQLAlchemy(app)


### CLASS DECLARATION
class Lead(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String,  nullable=False)
    props = db.Column(db.String)
    email = db.Column(db.String)
    status = db.Column(db.String)

    
    def __repr__(self):
        return f"{self.name} - {self.props}- {self.status}"


### POST NEW LEADS FOR REGISTRATION
@app.route('/',methods=['POST'])
def webhook():
    if request.method == 'POST':

        print("webhook is working")
        
        print(request.headers)
        
        first_name = request.headers['first_name']
        last_name = request.headers['last_name']
        name = str(first_name) + ' ' + str(last_name)
        if request.headers['Mobile']:
            phone=request.headers['Mobile']
        else:
            phone = request.headers['Phone']
        email = request.headers['Email']
        list_project_names = request.headers['Interested_Properties'].split(',')
        
        #interested_in = request.json['Interested in']

        for project_name in list_project_names:
            for site in all_sites.sites:
                for sub_project_name in site["key_words"]:
                    print(sub_project_name + ' present!')
                    if project_name in sub_project_name:
                        site["function"].fin_function(sub_project_name, name, phone, email)
            
        
        return 'completed',200


### DISPLAY ALL LEADS
@app.route('/leads')
def get_requests():
    leads = Lead.query.all()
    output = []
    
    for data in leads:
        lead_data = {'name':data.name, 'props':data.props, 'phone': data.phone, 'email': data.email, 'status': data.status}
        output.append(lead_data)
    
    return {'leads' : output}


### GET STATUS FOR SPECIFIC LEADS
@app.route('/output', methods=['GET'])
def get_lead_status():
    mobile = request.args.get('Mobile')
    phone = request.args.get('Phone')
    
    if mobile:
        phone = mobile
    
    print(phone)
    
    lead = Lead.query.get(phone)
    if lead is None:
        return {'error': 'Not found!'}
    leads = Lead.query.all()
    print(leads)
    for data in leads[::-1]:
        output = data.status
        print(output)
        break
    
    return output        

if __name__ == '__main__':
    app.run(debug=True, port = 443, ssl_context=("cert.pem", "key.pem"))
