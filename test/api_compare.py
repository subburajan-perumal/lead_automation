{
    'pgname': None, 
    'pid': None, 
    'loginid': '3788146', 
    'dt': '20220929', 
    'tranType': None, 
    'project': None, 
    'email': 'redacted@example.com', 
    'mobile': '9000000000', 
    'ph': None, 
    'vdate': '20220929', 
    'vtime': '092027', 
    'pgcity': None, 
    'msg': 'i am  looking for property in Chennai and has viewed your contact details from the company profile.', 
    'city': 'Chennai', 
    'isd': '91', 
    'subject': 'Subject', 
    'locality': None, 
    'address': None, 
    'name': 'Magicbricks User', 
    'id': '864256911', 
    'time': '092027'
}

apartment_names = '2 BHK'
if '4 BHK' in input['msg']:
    apartment_names = '4 BHK'
elif '3 BHK' in input['msg']:
    apartment_names = '3 BHK'
if 'name' not in input or input['name'] == None:
    input['name'] = 'Magicbricks User'
if 'email' not in input or input['email'] == None:
    input['email'] = str(input['mobile']) + '@example.com'
details = str(input['msg']) + str('\n\n') + str(input)
details = details[:200]
data = {
    'Configuration1': apartment_names,
    'Country_Code': '+' + str(input['isd']),
    'City': input['city'],
    'Email': input['email'],
    'Phone': input['mobile'],
    'Project_Enquired_for': dict({'id': project_id}),
    'Full_Name': input['name'],
    'Lead_Source': 'Magicbricks',
    'Last_Name': input['name'],
    'Initial_Enquiry_Particulars_Automation': details
}
if not input['locality']:
    data['Interested_Localities'] = None
elif type(input['locality']) == str:
    data['Interested_Localities'] = [input['locality']]
else:
    data['Interested_Localities'] = list(input['locality'])