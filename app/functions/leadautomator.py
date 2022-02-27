from pymongo import MongoClient
from datetime import datetime
from app.functions.site_base import SiteAutomator
MONGO_DB="REDACTED"
class LeadAutomator:
    def __init__(self,lead_data) -> None:
        self.lead_data = lead_data
        self.CONN = MongoClient(MONGO_DB)
        self.DB = self.CONN['lead_automation']
        self.LEADS = self.DB['leads']
        self.SITE=self.DB['Site']
    
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
    
    def generate_lead(self, by):
        
        if by=="enquired" :
            self.project_name = self.lead_data.get("project_enquired_for")
    
            if self.project_name is not None:
                site = self.SITE.find_one( {"key_words": {"$in": [self.project_name]}})

                if site is not None:
                    browser_automation = SiteAutomator( self.lead_data[ "phone" ] , self.lead_data[ "email" ],self.lead_data)
                    browser_automation.projectCheck( site ['name'], self.project_name,keyword_search=True)
                    browser_automation.automated_flow()
                    browser_automation.upload_data()
                    browser_automation.teardown()

        
        if by=="interested":
            self.interested_properties=self.lead_data.get("interested_properties").split(";")
            if self.interested_properties :
                for properties in self.interested_properties:
                    site=self.SITE.find({"key_words":{"$in":[properties]}})
                    if site is not None:
                        browser_automation = SiteAutomator( self.lead_data[ "phone" ] , self.lead_data[ "email" ],self.lead_data)
                        browser_automation.projectCheck( site ['name'], self.project_name,keyword_search=True)
                        browser_automation.automated_flow()
                        browser_automation.upload_data()
                        browser_automation.teardown()
        
        if by=="location":
            self.location = self.lead_data.get("location")
            if self.location :
                browser_automation = SiteAutomator( self.lead_data[ "phone" ] , self.lead_data[ "email" ],self.lead_data)
                browser_automation.projectCheck( site ['name'], self.project_name,keyword_search=False)
                browser_automation.automated_flow()
                browser_automation.upload_data()
                browser_automation.teardown()
                # for properties in self.interested_properties:
                    # site=self.SITE.find({"key_words":{"$in":[properties]}})







        
    
