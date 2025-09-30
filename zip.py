import requests
# get server icon
def get_icon():
    with open("pack.png", "wb") as f:
        f.write(requests.get("https://api.mcstatus.io/v2/icon/akoot.co").content)

get_icon()
