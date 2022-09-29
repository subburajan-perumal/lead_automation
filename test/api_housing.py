{
    'lead_date': 1664425620, 
    'apartment_names': '3 BHK', 
    'country_code': '+91', 
    'service_type': 'resale', 
    'category_type': 'residential', 
    'locality_name': 'Guindy', 
    'city_name': 'Chennai', 
    'lead_name': 'Raghavan ', 
    'lead_email': 'redacted@example.com', 
    'lead_phone': '9000000000', 
    'flat_id': 5665228, 
    'project_name': 'Puravankara Somerset House', 
    'property_field': ['Apartment'], 
    'max_area': 1925, 
    'min_area': 1925, 
    'min_price': 22470525, 
    'max_price': 22470525
}


{
    'lead_date': 1664505720, 
    'apartment_names': '2 BHK', 
    'country_code': '+33', 
    'service_type': 'new-projects', 
    'category_type': 'residential', 
    'locality_name': 'Porur', 
    'city_name': 'Chennai', 
    'lead_name': 'Rafi Ahamed', 
    'lead_email': 'redacted@example.com', 
    'lead_phone': '649388392', 
    'project_id': 128170, 
    'project_name': 'Smart Homes At Green Enclave', 
    'property_field': ['Apartment'], 
    'max_area': None, 'min_area': None, 
    'min_price': 6200000, 'max_price': 6200000
}

if 'lead_email' not in input or input['lead_email'] == None:
    input['lead_email'] = input['lead_phone'] + '@example.com'
if 'lead_name' not in input or input['lead_name'] == None:
    input['lead_name'] = 'Housing User'
if 'property_field' not in input or input['property_field'] == None:
    input['property_field'] = ['Apartment']
if 'category_type' not in input or input['category_type'] == None:
    input['category_type'] = 'residential'
apartment_names = '2 BHK'
if '4 BHK' in input['apartment_names']:
    apartment_names = '4 BHK'
elif '3 BHK' in input['apartment_names']:
    apartment_names = '3 BHK'


data = {
    'Configuration1': str(input['apartment_names']),
    'Country_Code': str(input['country_code']),
    # 'Zoning': input['category_type'],
    'City': input['city_name'],
    'Email': input['lead_email'],
    'Phone': input['lead_phone'],
    'Project_Enquired_for': dict({'id': project_id}),
    # 'Property_Type1': input['property_field'],
    # 'Minimum_Price': input['min_price'],
    # 'Maximum_Price': input['max_price'],
    'Full_Name': input['lead_name'],
    'Last_Name': input['lead_name'],
    'Lead_Source': str(type),
    'Initial_Enquiry_Particulars_Automation': str(input)[:200]
}

if not input['locality']:
    data['Interested_Localities'] = None
elif type(input['locality_name']) == str:
    data['Interested_Localities'] = [input['locality_name']]
else:
    data['Interested_Localities'] = list(input['locality_name'])

if input['service_type'] == 'new-projects':
    data['Interested_in_wf'] = 'New'