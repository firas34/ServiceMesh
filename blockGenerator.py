import os, requests
ch = str(input("Please give the concerned host IP...\n"))
target = str(input("Please give the concerned application...\n"))
l = str(input("Please give the IP address that you want to block...\n"))
List = '["'+l+'" ]'
first = "apiVersion: security.istio.io/v1beta1\nkind: AuthorizationPolicy\nmetadata:\n  name: ingress-policy\n  namespace: default\nspec:\n  selector:\n    matchLabels:\n"
target = "      app: " + target + "\n"
second = "  action: DENY\n  rules:\n  - from:\n    - source:\n"
List = "        ipBlocks: " + List + "\n"
final = first + target + second + List
f = open("rule.yaml", "w")
f.write(final)
f.close()
# os.system('kubectl apply -f rule.yaml') when you are in the same machine
print(requests.get(ch+'/applyRule').text)

