import data
from flask import Flask, request
from flask import Response
from flask_sqlalchemy import SQLAlchemy
from data import constants, all_sites, exclude
import warnings
warnings.filterwarnings("ignore") 


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
    created_at = db.Column(db.String,  nullable=False)
    attachments = db.Column(db.String,  nullable=False)
    
    def __repr__(self):
        return f"{self.name} - {self.props}- {self.status}"


### POST NEW LEADS FOR REGISTRATION
### Webhook from Zoho is sends the POST request of required information
@app.route('/',methods=['POST'])
def webhook():
    if request.method == 'POST':       
        lead_id = request.headers['lead_id']
        first_name = request.headers['first_name']
        last_name = request.headers['last_name']
        if request.headers['Mobile']:
            phone=request.headers['Mobile']
        else:
            phone = request.headers['Phone']
        email = request.headers['Email']
        
        list_project_names = request.headers['Interested_Properties']
        
        Initial_Enquiry_Particulars_Automation = request.headers['Initial_Enquiry_Particulars_Automation']

        project_enquired_for = request.headers['project_enquired_for']

        for short, site in all_sites.sites.items():
            for sub_project_name in site["key_words"]:
                print("Checking for..." + str(sub_project_name))
                if sub_project_name in list_project_names and site["active"] and sub_project_name not in exclude.list_:
                    print(str(sub_project_name) + ' present!')
                    site["function"].fin_function(lead_id, sub_project_name, first_name, last_name, phone, email)
                if sub_project_name in Initial_Enquiry_Particulars_Automation and site["active"] and sub_project_name not in exclude.list_:
                    print(str(sub_project_name) + ' present!')
                    site["function"].fin_function(lead_id, sub_project_name, first_name, last_name, phone, email)
                if sub_project_name in project_enquired_for  and site["active"] and sub_project_name not in exclude.list_:
                    print(str(sub_project_name) + ' present!')
                    site["function"].fin_function(lead_id, sub_project_name, first_name, last_name, phone, email)

        return {'leads': 200 }


@app.route('/post')
def webhook_salesiq():
    if request.method == 'POST':
        try:        
            lead_id = request.headers['lead_id']
            first_name = request.headers['first_name']
            last_name = request.headers['last_name']
            if request.headers['Mobile']:
                phone=request.headers['Mobile']
            else:
                phone = request.headers['Phone']
            email = request.headers['Email']
            
            list_project_names = []
            
            list_project_names.extend(request.headers['Interested_Properties'].split(';'))
            
            Initial_Enquiry_Particulars_Automation = request.headers['Initial_Enquiry_Particulars_Automation']

            project_enquired_for = request.headers['project_enquired_for']

            print("Project enquired for ... " + str(project_enquired_for))

            for project_name in list_project_names:
                for short, site in all_sites.sites.items():
                    for sub_project_name in site["key_words"]:
                        if project_name in sub_project_name and len(project_name) > 1 and site["active"]:
                            print(str(sub_project_name) + ' present!')
                            site["function"].fin_function(lead_id, sub_project_name, first_name, last_name, phone, email)
                        if sub_project_name in Initial_Enquiry_Particulars_Automation:
                            print(str(sub_project_name) + ' present!')
                            site["function"].fin_function(lead_id, sub_project_name, first_name, last_name, phone, email)
                        if sub_project_name in project_enquired_for:
                            print(str(sub_project_name) + ' present!')
                            site["function"].fin_function(lead_id, sub_project_name, first_name, last_name, phone, email)
        except:
            print("Unknown exception.")

        return Response("{'a':'b'}", status=200, mimetype='application/json')

    if request.method == 'HEAD':
        return Response("{'a':'b'}", status=200, mimetype='application/json')


### DISPLAY ALL LEADS
@app.route('/leads')
def get_requests():
    leads = Lead.query.all()
    output = []

    for data in leads[::-1]:
        lead_data = {'name':data.name, 'props':data.props, 'phone': data.phone, 'email': data.email, 'status': data.status, 'created_at': data.created_at, 'attachments': data.attachments}
        output.append(lead_data)

    return {'leads' : output}


### DISPLAY 10k LEADS
@app.route('/10kleads')
def get_10krequests():
    leads = Lead.query.all()
    output = []
    
    i = 0
    for data in leads[::-1]:
        if i < 10000:
            lead_data = {'name':data.name, 'props':data.props, 'phone': data.phone, 'email': data.email, 'status': data.status, 'created_at': data.created_at, 'attachments': data.attachments}
            output.append(lead_data)
        else:
            break
        i += 1
    
    return {'leads' : output}


if __name__ == '__main__':
    app.run(debug=True, port = 443, ssl_context=("cert.pem", "key.pem"), threaded=True)
