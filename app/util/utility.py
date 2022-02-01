def cmpstring(string1,string2):
    str1="".join([i for i in string1 if i.isalpha()])
    str2="".join([i for i in string2 if i.isalpha()])
    return str1==str2