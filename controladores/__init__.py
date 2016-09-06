import os
import json

asd = ""
try:
    asd = open(os.getcwd()[:-13] + r"storage\trayectos.json", "w")
    dsa = {"qwer" : 123, "asdf" : 321}
    par = json.dumps(dsa)
    print (dsa)
    print (par)
    asd.write(par)
    asd.close()
    asd = open(os.getcwd()[:-13] + r"storage\trayectos.json", "r")
    qwe = json.load(asd)
    print(qwe)
    print(par)
    if qwe == par:
        print ("asd")
finally:
    asd.close()
