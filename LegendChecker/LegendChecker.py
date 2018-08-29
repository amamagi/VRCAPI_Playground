import requests
import getpass

def end():
    input("enterで終了")
    exit()

def check_legend(response, target):
    if response.status_code != 200:
        print("データ取得に失敗")
        
    elif "system_trust_legend" in response.json()["tags"]:
        print("{}はレジェンド".format(target))
        
    else:
        print("{}はレジェンドではない".format(target))

def get_response(target, data, username, password):
    try:
        return requests.get("https://api.vrchat.cloud/api/1/users/{}/name".format(target), data=data, auth=(username.encode(), password))
    except Exception as e:
        print(e.args)
        end()

apiKey = "JlE5Jldo5Jibnk5O5hTx6XVqsJu4WJ26"
data = {"apiKey":apiKey}

username = input("Your VRChatID:")
password = getpass.getpass()

while(1):
    target = input("Target VRChatID:")
    response = get_response(target, data, username, password)
    check_legend(response, target)
    is_continue = input("続けますか？(y/n)")
    if is_continue != "y" and is_continue != "Y":
        exit()