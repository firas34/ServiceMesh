from flask import Flask , request
import os
app = Flask(__name__)
#global ruleId = 1111
import uuid

def generateRuleFile(JSONFILE, ruleId):
    target = JSONFILE["appName"]
    l = JSONFILE["ExceptionIp"]
    rule = JSONFILE["rule"].upper()
    List = '["'+l+'" ]'
    first = "apiVersion: security.istio.io/v1beta1\nkind: AuthorizationPolicy\nmetadata:\n  name: "+ruleId +"\n  namespace: default\nspec:\n  selector:\n    matchLabels:\n"
    target = "      app: " + target + "\n"
    second = "  action: "+ rule +"\n  rules:\n  - from:\n    - source:\n"
    List = "        ipBlocks: " + List + "\n"
    final = first + target + second + List
    f = open("rule.yaml", "w")
    f.write(final)
    f.close()

@app.route('/addRule', methods=["POST"])
def addRule():
    JSONFILE = request.get_json()
    ruleId  = str(uuid.uuid4()) 
    generateRuleFile(JSONFILE, ruleId)
    # save in db
    stream = os.popen('kubectl apply -f rule.yaml')
    return { "response": stream.read() , "ruleId": ruleId }

@app.route('/deleteRule/<ruleId>', methods=["DELETE"])
def deleteRule(ruleId):
    stream = os.popen('kubectl delete AuthorizationPolicy '+ ruleId)
    return stream.read()


@app.route('/updateRule/<ruleId>', methods=["PUT"])
def updateRule(ruleId):
    JSONFILE = request.get_json()
    generateRuleFile(JSONFILE, ruleId)
    # save in db
    stream = os.popen('kubectl apply -f rule.yaml')
    return { "response": stream.read() , "ruleId": ruleId }

@app.route('/showRule/<ruleId>', methods=["GET"])
def showRule(ruleId):
    return "next version maybe!"

if __name__ == "__main__":
	app.run(port=9090)
