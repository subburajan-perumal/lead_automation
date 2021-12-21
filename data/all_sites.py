from functions import alliance, casagrand, akshaya, dra, hiranandani, shriram, tvs, radiance, adityaram, brigade, lifestyle, pragnya, doshi, fomra, krishnagrp, gsquare

## key_words is from ZOHO CRM

sites = {

    ## 1
    "alliance": {
        "url": "https://partners.allianceprojects.in/login",
        "email": "redacted@example.com",
        "pass": "REDACTED",
        "key_words": ["Alliance Humming Gardens", "Alliance Galleria", "alliancegalleria", "Urbanrise Eternity", "OMR", "Sholinganallur", "Lumina", "None (default)"],
        "function": alliance,
        "active": 1
    },

    
    ## 2
    "fomra": {
        "url": "http://www.fomrahousing.in/cp/?srd=5d1892be5e3c3067305fa1d2",
        "channel_phone_number": "9000000000",
        "partner_name": "Lead Automation",
        "key_words": ["Fomra Hues", "Fomra Celebration","Fomra Vayou"],
        "function": fomra,
        "active": 1
    },


    ## 3.1 ## ELITE
    "brigade": {
        "url": "https://form.jotform.com/202941029236047",
        "email": "redacted@example.com",
        "pass": "REDACTED",
        "company" : "Elite Lifespaces",
        "agentf1": "Elite",
        "agentl1": "Lifespaces",
        "aph1": "9",
        "aph2": "1",
        "aph3": "9000000000",
        "key_words": ["Brigade Xanadu", "Brigade Bonito", "Brigade Residences at WTC", "brigade-", "Brigade Residences", "None (default)"],
        "function": brigade,
        "active": 1
    },

    

    ## 4
    "casagrand": {
        "url": "http://cp.sell.do/users/sign_in",
        "email": "redacted@example.com",
        "pass": "REDACTED",
        "key_words": ['Casagrand Zenith', 'Casagrand Esquire', 'Casagrand Tudor', 'Casagrand Savoye', 'Casagrand Supremus',
        'Casagrand ECR 14', 'Casagrand Primera', 'Casagrand Crescendo Elite', 'Casagrand Crecendo Compact',
        'Casagrand Millenia', 'Casagrand Royale', 'Casagrand Utopia', 'Casagrand Athens', 'Casagrand FirstCity'],
        "function": casagrand,
        "active": 1
    },

    ## 5
    "akshaya": {
        "url": "http://cp.sell.do/users/sign_in",
        "email": "redacted@example.com",
        "pass": "REDACTED",
        "key_words": ['Akshaya Tango', 'Akshaya Today', 'Akshaya Republic', 'Akshaya OrlandO', 'Akshaya Earth', 'Akshaya Shanti', 'Akshaya Poongavanam', 'Pallavaram', 'Thoraipakkam', 'Perungudi', 'OMR', 'Kelambakkam', 'Sholinganallur', 'Navalur'],
        "function": akshaya,
        "active": 1
    },

    ## 6
    "dra": {
        "url": "http://cp.sell.do/users/sign_in",
        "email": "redacted@example.com",
        "pass": "REDACTED",
        "key_words": ["DRA Centralia", "DRA Truliv Navalur", "DRA 90 Degrees", "DRA Truliv Porur", "DRA Truliv Navalur Commercial", "Porur"],
        "function": dra,
        "active": 1
    },

    
    ## 7
    "tvs": {
        "url": "https://www.tvsemerald.com/lp/cp/?srd=5d08ad2d5e3c3009976bffa9",
        "email": "",
        "pass": "",
        "cpname": "Lead Automation",
        "cpphn": "9000000000",
        "key_words": ["TVS Emerald Flourish", "TVS Emerald GreenAcres Apts", "TVS Emerald Green Enclave", 
        "TVS Emerald LightHouse", "TVS Emerald Peninsula", "TVS Emerald Hamlet", "tvs-green-enclave.com", "Porur", "Green Enclave", "Lumina", "None (default)"],
        "function": tvs,
        "active": 1
    },

    
    ## 8
    "shriram": {
        "url": "https://www.shriramproperties.com/synergy/",
        "email": "redacted@example.com",
        "pass": "",
        "mobile": "9000000000",
        "channel_partner": "Lead Automation",
        "key_words": ["Shriram Park 63", "Shriram Superstar", "Shriram Joy", "Shriram Shankari lakeside", 
        "Shriram One City", "Shriram Divine City", "Guduvancher", "Perungalathur", "Lumina", "None (default)"],
        "function": shriram,
        "active": 1
    },
    
    
    ## 9
    "radiance": {
        "url": "http://cp.radiancerealty.in/login.php",
        "url2": "http://cp.radiancerealty.in/lead_add.php",
        "email": "redacted@example.com",
        "pass": "REDACTED",
        "key_words": ["Radiance Elite", "Radiance Splendour", "Radiance Smartville", "Radiance The Pride", "Radiance Suprema",
            "Radiance Blossom", "Radiance Sapphire", "Radiance Maraikayar Manor"],
        "function": radiance,
        "active": 1
    },

    
    ## 10
    "adityaram": {
        "url": "http://www.adityaramproperties.com/channel-partner/index.html?srd=610a6509c825611af77aad37",
        "cpname": "Lead Automation",
        "cpphn": "9000000000",
        "key_words": ["Adityaram Nagar Phase 5", "Adityaram Signature City", "Adityaram", "None (default)"],
        "function": adityaram,
        "active": 1
    },
    
    
    ## 11
    "lifestyle": {
        "url": "https://lifestylehousing.co.in",
        "email": "LeadAutomation",
        "pass": "REDACTED",
        "channel_partner": "LeadAutomation",
        "key_words": ["Lifestyle Podium", "Lifestyle Le Paradis", "Podium", "Porur"],
        "function": lifestyle,
        "active": 1
    },

    ## 12
    "hiranandani": {
        "url": "https://hiranandaniparkschennai.com/channelpartners/",
        "email": "LeadAutomation",
        "pass": "REDACTED",
        "partner_name": "Lead Automation",
        "key_words": ["Hiranandani Parks", "None (default)"],
        "function": hiranandani,
        "active": 1
    },

    ## 13
    "pragnya": {
        "url": "https://edenpark.net/channel-partners/",
        "email": "LeadAutomation",
        "pass": "REDACTED",
        "partner": "Lead Automation",
        "key_words": ["Pragnya Eden Park", "House of Hiranandani"],
        "function": pragnya,
        "active": 1
    },

    ## 14
    "doshi": {
        "url": "https://doshi.imerge.in/",
        "email": "9000000000",
        "pass": "REDACTED",
        "partner": "Lead Automation",
        "key_words": ["Doshi Serene County", "Doshi Risington", "Doshi First Nest"],
        "function": doshi,
        "active": 1
    },
    
    ## 15
    "krishnagrp": {
        "url": "https://krishnagroup.ventures/leadsubmission.php?srd=5f815f35c825616af32c6aba",
        "partner_name": "Lead Automation",
        "key_words": ["Krishna Mithila","Krishna Meadows","Krishna HeadQuartes","Krishna Tivoli Gardens","Krishna Celesta"],
        "function": krishnagrp,
        "active": 1
    }, 

    ## 16
    "gsquare": {
        "url": "https://cp.gsquarehousing.com",
        "partner_name": "Lead Automation",
        "key_words": ["G Square Sands N Waves", "G Square Sunnyvale", "G Square Blue Breeze", "G Square Seawoods", "G Square Beach Walk"],
        "function": gsquare,
        "active": 0
    }, 

}
