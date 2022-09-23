import logging


logging.basicConfig(
    # filename= Config.LOG_PATH+"lead_automation.log",
    level=logging.INFO,
    # format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    encoding='utf-8'
    )


def housing():
    from app.util.utility import housing_api
    logging.info(msg='Housing API running ...')
    housing_api()
    return {'status': 'success'}

def magicbricks():
    from app.util.utility import magicbricks_api
    logging.info(msg='Magicbricks API running ...')
    magicbricks_api()
    return {'status': 'success'}
