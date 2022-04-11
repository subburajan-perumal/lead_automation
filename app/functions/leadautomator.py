from pymongo import MongoClient
from datetime import datetime
# from app.functions.site_base import SiteAutomator
from config import Config
MONGO_DB = Config.MONGO_URI
class LeadAutomator:
    def __init__(self,lead_data) :
        self.lead_data = lead_data
        self.CONN = MongoClient(MONGO_DB)
        self.DB = self.CONN['lead_automation']
        self.LEADS = self.DB['leads']
        self.SITE=self.DB['Site']
        self.keywords=[]
        self.site_list={}
    
    def create_lead(self):
        self.user_detail = self.LEADS.find_one( {"email": self.lead_data["email"], "phone": self.lead_data["phone"]} )
        # print(user_detail)
        fullname=self.lead_data['name']
        if self.user_detail is None:
            lead_creation={"name":fullname,
                    "phone":self.lead_data["phone"],
                    "email":self.lead_data["email"], 
                    "created_at":datetime.now(),
                    "modified_time":datetime.now()
                    }
            self.LEADS.insert_one(lead_creation)
    
    def get_keywords(self,field:str,splitBy:str):
        print("get by keyword")
        try:
            temp=field.split(splitBy)
            self.keywords.extend(temp)
        except Exception as e:
            print(str(e))

    
    def search_by_keyword(self):
        print("search by keyword")
        print(self.keywords)
        self.site_list = self.DB.Site.aggregate(
            [
                {
                    "$match":
                    {
                        "$or":
                            [
                                {
                                    "project_list.keywords":
                                    {
                                        "$in": self.keywords
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
                                    "$in": self.keywords
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
        print("searched bykeyword")
        # for _site in list(self.site_list):
        #     # logger.info(f"Site: {_site['name']}; Project: {_site['project_list']['project_name']}")
        #     site_name = _site['name']
        #     print(site_name)
        #     print(_site) 
        # result=list(self.site_list)
        return list(self.site_list)
    
    # def generate_lead(self, by):
    #     for site in self.site_list:
    #         browser_automation = SiteAutomator( self.lead_data[ "phone" ] , self.lead_data[ "email" ],self.lead_data)
    #         browser_automation.projectCheck( site ['name'], self.project_name,keyword_search=True)
    #         browser_automation.automated_flow()
    #         browser_automation.upload_data()
    #         browser_automation.teardown()

        
        # if by=="interested":
        #     self.interested_properties=self.lead_data.get("interested_properties").split(";")
        #     if self.interested_properties :
        #         for properties in self.interested_properties:
        #             site=self.SITE.find({"key_words":{"$in":[properties]}})
        #             if site is not None:
        #                 browser_automation = SiteAutomator( self.lead_data[ "phone" ] , self.lead_data[ "email" ],self.lead_data)
        #                 browser_automation.projectCheck( site ['name'], self.project_name,keyword_search=True)
        #                 browser_automation.automated_flow()
        #                 browser_automation.upload_data()
        #                 browser_automation.teardown()
        
        # if by=="location":
        #     self.location = self.lead_data.get("location")
        #     if self.location :
        #         browser_automation = SiteAutomator( self.lead_data[ "phone" ] , self.lead_data[ "email" ],self.lead_data)
        #         browser_automation.projectCheck( site ['name'], self.project_name,keyword_search=False)
        #         browser_automation.automated_flow()
        #         browser_automation.upload_data()
        #         browser_automation.teardown()
        #         # for properties in self.interested_properties:
                    # site=self.SITE.find({"key_words":{"$in":[properties]}})







        
    
