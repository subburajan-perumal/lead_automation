import glob
import os
import time
import schedule

def removing_older_img():
    
    path = r"./storage/**/*.png"
    now = time.time()
    days = 200

    for filename in glob.iglob(path, recursive=True):

        if os.path.getmtime(os.path.join(path, filename)) < now - days * 86400:
            if os.path.isfile(os.path.join(path, filename)):
                print(filename)
                os.remove(os.path.join(path, filename))

schedule.every().seconds.do(removing_older_img)

while True:
    schedule.run_pending()
    time.sleep(1)