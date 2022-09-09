import time
import schedule

def housing():
    from app.util.utility import housing_api
    print('Housing API running ...')
    housing_api()
    return {'status': 'success'}

def magicbricks():
    from app.util.utility import magicbricks_api
    print('Magicbricks API running ...')
    magicbricks_api()
    return {'status': 'success'}

schedule.every(60).seconds.do(housing)
schedule.every(60).seconds.do(magicbricks)

while True:
    schedule.run_pending()
    time.sleep(6)