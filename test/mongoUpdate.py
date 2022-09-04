from pymongo import MongoClient


MONGO_DB="REDACTED"

CONN = MongoClient(MONGO_DB)
DB = CONN['lead_automation']
Sites = DB['Site']

Sites.update_many(
    {

    },
    {
        "$set": {
            "days": 30
        }
    }
)