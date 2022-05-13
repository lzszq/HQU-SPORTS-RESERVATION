from typing import Optional
import json
from httpx import Client, Cookies
import time

USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
ACCEPT_XML = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
ACCEPT_JSON = 'application/json, text/javascript, */*; q=0.01'
BASE_URL = 'https://ecard-sh.hqu.edu.cn'
BASE_GYM_URL = 'https://ecard-gymrsapp.hqu.edu.cn'


class ReserveUser:

    data: dict
    client: Optional[Client]

    def __init__(self,
                 data:     dict,
                 *args, **kwargs):
        self.data = data
        self.client = Client(verify=False)
        self.client.headers = {'User-Agent': USER_AGENT, 'Accept': ACCEPT_XML}

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
        res = self.client.post(BASE_URL+'//Page/Page',
                               params=query_params, timeout=10)
        res = self.client.get(BASE_URL+res.headers['Location'], timeout=10)
        res = self.client.get(
            BASE_GYM_URL+'/?'+res.headers['Location'].split('?')[1], timeout=10)

        return True

    def book_fitness(self, s_date: str, time_no: str, try_cnt: int = 10):
        return self.book(service_id=143, s_date=s_date, time_no=time_no, try_cnt=10)

    def book_badminton_weekend(self, s_date: str, time_no: str, try_cnt: int = 10):
        return self.book(service_id=144, s_date=s_date, time_no=time_no, try_cnt=10)

    def book_badminton_weekday(self, s_date: str, time_no: str, try_cnt: int = 10):
        return self.book(service_id=141, s_date=s_date, time_no=time_no, try_cnt=10)

    def get_fitness_info(self, s_date: str):
        return self.get_info(s_date=s_date, service_id=143)

    def get_badminton_weekend_info(self, s_date: str):
        return self.get_info(s_date=s_date, service_id=144)

    def get_badminton_weekday_info(self, s_date: str):
        return self.get_info(s_date=s_date, service_id=141)

    def get_info(self, s_date: str, service_id: str):
        res = self.client.get(
            BASE_GYM_URL + f'/product/findOkArea.html?s_date={s_date}&serviceid={service_id}', timeout=10)
        data_json = json.loads(res.text)
        arr = []
        for i in data_json['object']:
            if i['status'] == 1:
                arr.append({"service_id": str(i['stock']['serviceid']), "id": str(i['id']), "stock_id": str(
                    i['stockid']), "s_date": str(i['stock']['s_date']), "time_no": str(i['stock']['time_no'])})
        return arr

    def book(self, service_id: int, s_date: str, time_no: str, try_cnt: int = 10):
        '''
        service_id: like 141, 143, 144
        s_date: like 2022-04-29
        time_no: like 18:30-19:30
        '''
        arr = get_info(s_date, service_id)
        
        headers = self.client._headers
        headers['Host'] = 'ecard-gymrsapp.hqu.edu.cn'
        headers['Accept'] = ACCEPT_JSON
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Content-Type'] = 'application/x-www-formurl-urlencoded; charset=UTF-8'
        headers[
            'Referer'] = f'https://ecard-gymrsapp.hqu.edu.cn/product/show.html?id={service_id}'
        headers['Origin'] = BASE_GYM_URL
        headers['Connection'] = 'keep-alive'

        t = {}
        for i in arr:
            if i['s_date'] == s_date and i['time_no'] == time_no:
                t = i
                break

        if service_id == 144 or service_id == 141:
            book_params = {
                "param": '{"stockdetail":{"'+str(t["stock_id"])+'":"'+str(t['id'])+'"},"serviceid":"'+str(t['service_id'])+'","stockid":"'+str(t['stock_id'])+',","password":"'+self.data['pay_password']+'","users":"'+self.get_stunum(stu_num=self.data['stunum'])+'"}',
                "num": "1",
                "json": "true"
            }
        else:
            book_params = {
                "param": '{"stockdetail":{"'+str(t["stock_id"])+'":"'+str(t['id'])+'"},"serviceid":"'+str(t['service_id'])+'","stockid":"'+str(t['stock_id'])+',","password":"'+self.data['pay_password']+'"}',
                "num": "1",
                "json": "true"
            }

        while try_cnt != 0:
            res = self.client.post(BASE_GYM_URL + '/order/tobook.html',
                                   params=book_params, headers=headers, timeout=100)
            print(try_cnt+1, res.text)
            try_cnt -= 1
            # time.sleep(1)
        return True

    def get_stunum(self, stu_num: str = '', stu_name: str = '', use_stu_num: bool = True):
        if use_stu_num:
            res = self.client.get(f'https://ecard-gymrsapp.hqu.edu.cn/userInfo/select_user.html?sno={stu_num}&remark=0')
        else:
            res = self.client.get(f'https://ecard-gymrsapp.hqu.edu.cn/userInfo/select_user.html?name={stu_name}&remark=1')
        data = json.loads(res.text)
        if use_stu_num:
            return data[0]['name']
