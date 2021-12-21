## LIST OF ALL CONSTANTS

engine = './geckodriver'
db_path = 'sqlite:///leads.db'


mailgun = {

    "MAILGUN_DOMAIN": "REDACTED_MAILGUN_DOMAIN",
    "MAILGUN_URL": "https://api.mailgun.net/v3/REDACTED_MAILGUN_DOMAIN/messages",
    "MAILGUN_KEY": "REDACTED_SECRET_8",
    "from_mail": "mailgun@REDACTED_MAILGUN_DOMAIN",
    "to_mail": ["redacted@example.com", "redacted@example.com"],
    "pass": "REDACTED"

}

'''
zoho = {

    'url' : 'https://www.zohoapis.com/crm/v2/Leads/',
    'client_id': 'REDACTED',
    'client_secret': 'REDACTED',
    'refresh_token': "REDACTED",
    'redirect_URI': 'https://example.com',

}
'''


zoho = {

    'url' : 'https://www.zohoapis.com/crm/v2/Leads/',
    'client_id': 'REDACTED',
    'client_secret': 'REDACTED',
    'refresh_token': "REDACTED",
    'redirect_URI': 'https://www.google.com/',

}
