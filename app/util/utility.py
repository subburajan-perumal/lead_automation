def cmpstring(string1,string2):
    str1="".join([i for i in string1 if i.isalpha()])
    str2="".join([i for i in string2 if i.isalpha()])
    return str1==str2

def getTime():
            from datetime import datetime
            import pytz
            now = datetime.now(pytz.timezone('Asia/Kolkata')) 
            #print("now =", now)
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            return dt_string
            
def getsavePath(path,sub_project_name):
    from datetime import date
    today = date.today()
# ddmmYY
    formateddate = today.strftime("%d%m%y")
    # print("d1 =", d1)

    return [str(str(path) + '/' + formateddate+"_"+str(sub_project_name) + "_pre.png"), 
    str(str(path) + '/' +formateddate+"_"+ str(sub_project_name)   + "_post.png"),
    str(str(path) + '/' +formateddate+"_" + str(sub_project_name)  + "_error.png")
    ]
# print(getsavePath("akshaya","Tango"))