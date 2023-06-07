import httpx
import random
import string

class MailGwApi:
    def __init__(self, proxy: str= None, timeout: int=15) -> None:
        self.session = httpx.Client(headers={'content-type': 'application/json'}, timeout=timeout, proxies=proxy)
        self.base_url = 'https://api.mail.gw'
    
    def get_domains(self) -> list:
        domains: list = []
        
        for item in self.session.get(f'{self.base_url}/domains').json()['hydra:member']:
            domains.append(item['domain'])

        return domains

    def get_mail(self, name: str = None, password: str = None, domain: str = None) -> str:
        if not name: name = ''.join(random.choice(string.ascii_lowercase) for _ in range(15)) 
        mail: str =  f'{name}@{domain if domain != None else self.get_domains()[0]}'
        response = self.session.post(f'{self.base_url}/accounts', json={'address': mail, 'password': mail})
        
        try:
            if response.status_code == 201:
                token = self.session.post(f'{self.base_url}/token', json={'address': mail, 'password': mail if password == None else password}).json()['token']
                self.session.headers['authorization'] = f'Bearer {token}'
                return mail
            else:
                print(response.text)
        except:
            return 'Email creation error.'
    
    def fetch_inbox(self):
        response = self.session.get(f'{self.base_url}/messages').json()['hydra:member']
        return response
    
    def get_message(self, message_id: str):
        response = self.session.get(f'{self.base_url}/messages/{message_id}').json()
        return response
    
    def get_message_content(self, message_id: str):
        response = self.get_message(message_id)['text']
        return response