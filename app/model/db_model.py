from mongoengine import Document
from mongoengine import  StringField, ReferenceField, ListField ,IntField,DictField

MONGO_DB="REDACTED"

#future use not implemented
class ProjectList(Document):
    project_name=StringField(max_length=60)
    project_status=IntField(min_value=0,max_value=1)

class Site(Document):
    name=StringField(max_length=60, required=True, unique=True)
    url=StringField(max_length=60)
    site_data=DictField()
    status=IntField(min_value=0,max_value=1)
    projectlist=ListField(ReferenceField(ProjectList))
    
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

# conn=connect('lead_automation',MONGO_DB)
# t1=Site()
# t1.name=("subburajan")
# t1.url="https://testing.com"
# t1.save()
# # t1.save()
# print(t1)