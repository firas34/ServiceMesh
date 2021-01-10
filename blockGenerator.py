import os, requests
ch = str(input("Please give the concerned host IP...\n"))
#target = str(input("Please give the concerned application...\n"))
#l = str(input("Please give the IP address that you want to block...\n"))

#JSONFILE= { "appName": target, "ExceptionIp": l , "rule": "DENY" }


# os.system('kubectl apply -f rule.yaml') when you are in the same machine
#print(requests.post(ch+'/addRule' , json=JSONFILE).text)
#ad1b2639-7e8f-40e4-a41d-27e3bffc531d
print(requests.delete(ch+'/deleteRule/ad1b2639-7e8f-40e4-a41d-27e3bffc531d' ).text)
