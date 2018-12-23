import requests
import getpass

def end():
    input("enterで終了")
    exit()

def check_trust(response):
    target = response["username"]
    if "system_trust_legend" in response["tags"]:
        print("{} [Legend]".format(target))

def get_response(endpoint,data, username, password, params={}):
    try:
        return requests.get(endpoint, data=data, auth=(username.encode(), password), params=params)
    except Exception as e:
        print(e.args)
        end()

def check_status_code(response):
    if response.status_code == 401:
        print("ログインに失敗") 
        end()
    elif response.status_code != 200:
        print("データ取得に失敗")
        end()

apiKey = "JlE5Jldo5Jibnk5O5hTx6XVqsJu4WJ26"
data = {"apiKey":apiKey}
username = input("Your VRChatID:")
password = getpass.getpass()

# 本人のトラスト値
user = get_response("https://api.vrchat.cloud/api/1/auth/user", data, username, password)
check_status_code(user)
check_trust(user.json())

# フレンドの人数
friends_num = len(user.json()["friends"])

# フレンドのトラスト値
offset = 0
while(friends_num > 0):
    payload = {'offset':offset, 'n':100, 'offline':"true"}
    friends = get_response("https://api.vrchat.cloud/api/1/auth/user/friends", data, username, password, params=payload)
    check_status_code(friends)
    for friend in friends.json():
        check_trust(friend)
    offset += 100
    friends_num-=100

exit()