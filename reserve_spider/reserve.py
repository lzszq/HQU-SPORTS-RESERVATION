from typing import Optional
import json
from httpx import Client, Cookies
from bs4 import BeautifulSoup
import time

USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
ACCEPT = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'


class ReserveUser:

    username: str
    password: str
    data: dict
    client: Optional[Client]

    def __init__(self,
                 data:     dict,
                 *args, **kwargs):
        self.username = data['username']
        self.password = data['password']
        self.data = data
        self.client = Client(verify=False)
        self.client.headers = {'User-Agent': USER_AGENT, 'Accept': ACCEPT}

    def add_cookies(self) -> bool:
        cookies = Cookies()
        cookies.set('imeiticket', self.data['imeiticket'],
                    domain='ecard-sh.hqu.edu.cn')
        cookies.set('sourcetypeticket',
                    self.data['sourcetypeticket'], domain='ecard-sh.hqu.edu.cn')
        cookies.set('insert_cookie',
                    self.data['insert_cookie'], domain='ecard-sh.hqu.edu.cn')
        cookies.set('ASP.NET_SessionId',
                    self.data['ASP.NET_SessionId'], domain='ecard-sh.hqu.edu.cn')
        cookies.set('hallticket', self.data['hallticket'],
                    domain='ecard-sh.hqu.edu.cn')
        self.client.cookies = self.client._merge_cookies(cookies)
        return True

    def gymrsapp(self):
        base_url = 'https://ecard-sh.hqu.edu.cn'
        base_gym_url = 'https://ecard-gymrsapp.hqu.edu.cn'
        query_params = {
            'flowID':  '251',
            'type':    '3',
            'apptype': '4',
            'Url': 'https%253a%252f%252fecard-gymrsapp.hqu.edu.cn',
            'comeapp': '0',
            'parm11': '',
            'parm22': '0',
            'sMenuName': '%E5%9C%BA%E9%A6%86%E9%A2%84%E8%AE%A2',
            'sEMenuName': '%E5%9C%BA%E9%A6%86%E9%A2%84%E5%AE%9A',
            'sourcetype': self.data['sourcetypeticket'],
            'IMEI': self.data['imeiticket'],
            'language': '0',
            'comeapp': '1'

        }
        res = self.client.post('https://ecard-sh.hqu.edu.cn//Page/Page', params=query_params, timeout=10)
        res = self.client.get(base_url+res.headers['Location'], timeout=10)
        res = self.client.get(base_gym_url+'/?'+res.headers['Location'].split('?')[1], timeout=10)



        res = self.client.get(f'''{base_gym_url}/product/getarea.html?{self.getarea(
            s_dates=time.strftime("%Y-%m-%d", time.localtime(time.time()+86400)),
            serviceid="144",
            coordinatedes="2_badminton_%25E5%259C%25BA%25E5%259C%25B01%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B02%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B03%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B04%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B05%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B06%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B07%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B08%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B09%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B010%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B011%252C2_badminton_%25E5%259C%25BA%25E5%259C%25B012"
        )}''', timeout=10)
        print(res.text)

        badminton_params = {}

        res = self.client.get(base_gym_url+'/product/show.html?id=144', timeout=10)
        print(res.text)



    def getarea(self, s_dates: str, serviceid: str, coordinatedes: str):
        return "s_dates=" + s_dates + "&serviceid=" + serviceid + "&coordinatedes=" + coordinatedes
