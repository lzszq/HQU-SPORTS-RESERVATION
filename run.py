import reserve_spider
import json


def get_data():
    with open('.env.json', mode='r', encoding='utf-8') as f:
        data = json.loads(f.readline())
        f.close()
    return data


def generate_data():
    print('按照提示输入信息：')
    arr = ["username", "password", "imeiticket", "sourcetypeticket",
           "insert_cookie", "ASP.NET_SessionId", "hallticket"]
    data = {}
    for i in arr:
        a = input(f"请输入{i}：")
        data[i] = a
    with open('.env.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data))
        f.close()


if __name__ == '__main__':
    # a = input('是否需要生成数据（y or n)：')
    # if a == 'y':
    #     generate_data()
    data = get_data()
    user = reserve_spider.ReserveUser(get_data())
    user.add_cookies()
    user.book_fitness(s_date='2022-04-29', time_no='19:31-20:30')
    # user.book_badminton()
