from flask import Flask , request
import os
from utils.dbEngine import *
import uuid
import json
# For SWAGGER
from flasgger import Swagger
from flasgger.utils import swag_from
from flasgger import LazyString, LazyJSONEncoder



app = Flask(__name__)
app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 2}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True, 
            "model_filter": lambda tag: True, 
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/swagger/",
}
template = dict(
    swaggerUiPrefix=LazyString(lambda: request.environ.get("HTTP_X_SCRIPT_NAME", ""))
)

app.json_encoder = LazyJSONEncoder
swagger = Swagger(app, config=swagger_config, template=template)



def generateRuleFile(JSONFILE, ruleId):
    target = JSONFILE["appName"]
    l = JSONFILE["ipRange"]
    rule = JSONFILE["rule"].upper()
    List = '["'+l+'"]'
    print(List)
    first = "apiVersion: security.istio.io/v1beta1\nkind: AuthorizationPolicy\nmetadata:\n  name: "+ruleId +"\n  namespace: default\nspec:\n  selector:\n    matchLabels:\n"
    target = "      app: " + target + "\n"
    second = "  action: "+ rule +"\n  rules:\n  - from:\n    - source:\n"
    List = "        ipBlocks: " + List + "\n"
    final = first + target + second + List
    f = open("rule.yaml", "w")
    f.write(final)
    f.close()

@app.route('/addRule', methods=["POST"])
@swag_from("swagger/add.yml")
def addRule():
    JSONFILE = request.get_json()
    ruleId  = str(uuid.uuid4()) 
    generateRuleFile(JSONFILE, ruleId)
    # save in db
    addRuleData("db/Rules","RULES",ruleId, json.dumps(JSONFILE))
    stream = os.popen('kubectl apply -f rule.yaml')
    # LAZMNA NA3MLOU TRY 3LA RESPONCE MTA3 STREAM, if not completed successfuly => no ruleId !!!!!!!!!!!!!!!!!!!!!!!!!!
    return { "response": stream.read() , "ruleId": ruleId }

@app.route('/deleteRule/<ruleId>', methods=["DELETE"])
@swag_from("swagger/delete.yml")
def deleteRule(ruleId):
    stream = os.popen('kubectl delete AuthorizationPolicy '+ ruleId)
    return stream.read()


@app.route('/updateRule/<ruleId>', methods=["PUT"])
@swag_from("swagger/update.yml")
def updateRule(ruleId):
    JSONFILE = request.get_json()
    generateRuleFile(JSONFILE, ruleId)
    # update data in db
    print(json.dumps(JSONFILE))
    updateRuleData("db/Rules","RULES",ruleId, json.dumps(JSONFILE))
    stream = os.popen('kubectl apply -f rule.yaml')
    return { "response": stream.read() , "ruleId": ruleId }

@app.route('/showRule/<ruleId>', methods=["GET"])
@swag_from("swagger/show.yml")
def showRule(ruleId):
    return getRuleData("db/Rules","RULES",ruleId)
    

if __name__ == "__main__":
	app.run(port=9090)
