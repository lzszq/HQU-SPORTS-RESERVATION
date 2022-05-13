import reserve_spider
import json


def get_data():
    with open('.env.json', mode='r', encoding='utf-8') as f:
        data = json.loads(f.readline())
        f.close()
    return data


def generate_data():
    print('按照提示输入信息：')
    arr = ["pay_password", "stunum", "imeiticket", "sourcetypeticket",
           "insert_cookie", "ASP.NET_SessionId", "hallticket"]
    data = {}
    for i in arr:
        a = input(f"请输入{i}：")
        data[i] = a
    with open('.env.json', mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data))
        f.close()


if __name__ == '__main__':
    a = 'n'
    a = input('是否需要生成数据（y or n, default n)：')
    if a == 'y':
        generate_data()
    data = get_data()
    user = reserve_spider.ReserveUser(get_data())
    user.add_cookies()


    # print("badminton_weekday:")
    # for i in user.get_badminton_weekday_info(s_date='2022-05-18'):
    #     print(i)
    # print()

    # print("badminton_weekend:")
    # for i in user.get_badminton_weekend_info(s_date='2022-05-15'):
    #     print(i)
    # print()

    # print("fitness:")
    # for i in user.get_fitness_info(s_date='2022-05-15'):
    #     print(i)
    # print()

    # user.book_fitness(s_date='2022-05-15', time_no='19:31-20:30')

    # user.book_badminton_weekend(s_date='2022-05-15', time_no='16:31-17:30')

    # user.book_badminton_weekday(s_date='2022-05-18', time_no='16:31-17:30')

    # user.get_stunum(stu_name='', use_stu_num=False)
