#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author: github.com/imvast
@Date: 06/07/2023
"""

from requests  import Session
from time      import sleep
from emonkey   import MailGwApi
from terminut  import printf as print
from threading import Thread


class Monkey:
    def __init__(self) -> None:
        self.mailapi = MailGwApi()
        self.session = Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json;charset=utf-8',
            'version': '6.0.0',
            'device': 'Android',
            'lang': 'en-US',
            'app-type': '9',
            'Origin': 'https://www.monkey.app',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers',
        }

    def getIDs(self): # not needed but in the future when the version changes heres how you can get it :D
        payload = {
            "app_id":199577,
            "url":"https://www.monkey.app/",
            "user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0",
            "referer":"",
            "user_unique_id":""
        }

        response = self.session.post('https://mcs.tobsnssdk.com/v2/user/webid', json=payload)
        return response.json() # {"e":0,"ssid":"e1e0a5fb-052e-418f-8c21-902f5226da4a","web_id":"7241970282549790209"}
        
    def sendRegister(self, email):
        payload = {
            "email":email,
            "password":"7fd19c462b177450760aa1ac0b6c4349",
            "user_account_type":5,
            "pa_channel":None,
            "utm_source":None,
            "utm_medium":None,
            "utm_campaign":None,
            "utm_id":None,
            "web_id":7241970282549791000
        }

        response = self.session.post('https://api.monkey.cool/api/v5/auth/registerByEmail', json=payload)
        if "result" not in response.text:
            return print(f"err registering -- {response.text}")
        else: 
            return response.json() # {"result":1,"data":"845988d7-a73d-4c7b-a56f-c726b2900c83"}

    def getEmail(self):
        attempt = 0
        while attempt <= 10:
            sleep(3)
            attempt+=1
            for mail in self.mailapi.fetch_inbox():
                content = self.mailapi.get_message_content(mail['id'])
                # print(content)
                if "noreply@monkey.app" in mail["from"]["address"]:
                    id = content.split("https://www.monkey.app/#/redirectLogin?token=")[1].split("&email=")[0]
                    print(f"(*) Got ID: {id}")
                    return id
        print("(-) Failed to get id. Email never received.")
        return False

    def verifyEmail(self, email):
        code = self.getEmail()
        params = (
            ('code', code),
            ('email', email),
        )

        response = self.session.get('https://api.monkey.cool/api/v5/auth/activate', params=params)
        if "user_id" in response.text:
            print(f"(+) Successfully Created. [{email}]")
            return response.json()["data"]["token"]
        else:
            print("(!) Error Registering.")
            return False

    def updateProfile(self, auth):
        self.session.headers["Authorization"] = f"Bearer {auth}"

        payload = {
            "first_name":"MadeByVast",
            "gender":"male",
            "birth_date":"2000-06-07"
        }

        response = self.session.post('https://api.monkey.cool/api/v2/me/profile', json=payload)
        if "country" in response.text:
            print(f"(*) Profile Updated/Created. [{response.json()['id']}]")
            return True
        else:
            print(response.json())
            return False


def main():
    monk = Monkey()
    email = monk.mailapi.get_mail()
    print(f"(~) Using Email: {email}")
    monk.sendRegister(email)
    auth = monk.verifyEmail(email)
    monk.updateProfile(auth)
    
    
if __name__ == "__main__":
    for _ in range(3):
        Thread(target=main).start()