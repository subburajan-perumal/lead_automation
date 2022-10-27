from datetime import datetime
from pymongo import MongoClient
from app.functions.site_base import SiteAutomator
import logging

logging.basicConfig(
    # filename= Config.LOG_PATH+"lead_automation.log",
    level=logging.INFO,
    # format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    encoding='utf-8'
    )

MONGO_DB = "REDACTED"

def common_member(a, b):   
    a_set = set(a)
    b_set = set(b)
     
    # check length
    if len(a_set.intersection(b_set)) > 0:
        return list(a_set.intersection(b_set))
    else:
        return None
     

def function_finder(lead_data: dict):
    """This function process the request data and generate into lead

    Args:
        lead_data (dict):  it have lead details from the request

    Returns:
        string :  return the success and failed message of the execution
    """
    try:
        CONN = MongoClient(MONGO_DB)
        DB = CONN['lead_automation']
        LEADS = DB['leads']

    except Exception:
        logging.exception(msg="db connection failure")

    try:
        logging.info(msg="check for existing user in db")
        user_detail = LEADS.find_one(
            {"email": lead_data["email"], "phone": lead_data["phone"]})
        print(user_detail)
        fullname = lead_data['first_name'] + lead_data['last_name']
        if user_detail is None:
            lead_creation = {"name": fullname,
                             "phone": lead_data["phone"],
                             "email": lead_data["email"],
                             "created_at": datetime.now(),
                             "modified_time": datetime.now()
                             }
            LEADS.insert_one(lead_creation)
            logging.info(msg="new user created")
        # Enquired site
        site_keywords = []
        project_enquired = lead_data.get("project_enquired_for", "").split(";")
        interested_project = lead_data.get("interested_properties", "").split(";")
        interested_localities = lead_data.get("interested_localities", "").split(";")
        site_keywords.extend(project_enquired)
        site_keywords.extend(interested_project)
        site_keywords.extend(interested_localities)
        logging.debug(msg=str(site_keywords))
        logging.info(msg="search for the keywords in db")
        site_list = DB.Site.aggregate(
            [
                {
                    "$match":
                    {
                        "$or":
                            [
                                {
                                    "project_list.keywords":
                                    {
                                        "$in": site_keywords
                                    },
                                    "status": 1
                                }
                            ]
                    }
                },
                {
                    "$unwind":
                    {
                        "path": "$project_list",
                        "preserveNullAndEmptyArrays": False
                    }
                },
                {
                    "$match":
                    {
                        "$or":
                        [
                            {
                                "project_list.keywords":
                                {
                                    "$in": site_keywords
                                },
                                # "project_list.projectStatus":1,
                                "status": 1
                            }
                        ]
                    }
                },
                # {
                #     "$project":
                #     {"project_list.project_name":1}
                # },
                # {
                #     # "$sort":{
                #     #     "project_list.project_name":1
                #     # }
                # }
            ]
        )
        for _site in site_list:
            project_list = _site['project_list']
            logging.debug(msg=str(project_list))
            match_keywords = common_member(site_keywords,project_list['keywords'])
            logging.info('Match keywords in finder.py')
            logging.info(match_keywords)
            print('Matched keywords .. ' + str(match_keywords))
            logging.info(msg=f"Site: {_site['name']}; Project: {_site['project_list']['project_name']}; Matched keywords: {match_keywords}")
            logging.debug(msg="Matched_Keywords")
            logging.debug(msg=str(match_keywords))
            site_name = _site['name']
            site_projectname = _site['project_list']['project_name']
            browserAutomation = SiteAutomator(  
                                            phone = lead_data["phone"],
                                            email= lead_data["email"],
                                            lead_data= lead_data,
                                            match_keywords= match_keywords,
                                            site_data=_site
                                            )
            browserAutomation.projectCheck(site_name, site_projectname)
            browserAutomation.automated_flow()
            browserAutomation.upload_data()
            browserAutomation.teardown()
        logging.info(msg="task completed")
        return "success"

    except Exception:
        logging.exception(msg="exception occured")
        # print("error occured in function_finder", str(e))
        # print(os.getcwd())
        return "failed"
