import pymysql
import requests

import time

import requests
import random
from bs4 import BeautifulSoup

url = 'https://www.spark.co.nz/online/shop/products/oppo_find_n2_flip_group/?offerId=oppo127374spo&planId=mbundle051026&ifpId=interest_free_payment_over_12_months'

def get_content(url):
    # 设置headers是为了模拟浏览器访问 否则的话可能会被拒绝 可通过浏览器获取
    header = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate , br',
        'Accept-Language': 'en-NZ,en;q=0.9,zh-NZ;q=0.8,zh;q=0.7,en-GB;q=0.6,en-US;q=0.5,zh-CN;q=0.4',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
    }

    # 设置一个超时时间 取随机数 是为了防止网站被认定为爬虫
    timeout = random.choice(range(80, 180))

    while True:
        try:
            res = requests.get(url=url, headers=header, timeout=timeout)
            #print(res.text)
            break
        except Exception as e:
            print('3', e)
            time.sleep(random.choice(range(8, 15)))
    return res.text

html = get_content(url)
# html5lib,html.parser
bf = BeautifulSoup(html, 'html5lib')
#texts = bf.find_all('script', {'id': '__NEXT_DATA__'})
print(bf)

url = 'https://www.spark.co.nz/online/shop/static/product-manifest.json'
res=requests.get(url=url)
data = res.json()
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='my_database')
cursor = conn.cursor()
def device(brand):
    n2 = 'https://www.spark.co.nz/online/shop/_next/data/4077434/products/'+brand +'.json'
    res = requests.get(n2)
    data = res.json()
    pageProps = data['pageProps']
    product = pageProps['product']
    productData = product['productData']
    offerDetails = productData['offerDetails']
    return offerDetails

def write_in_phones(brand):
    #id = offerDetails[0]['id']
    offerDetails = device(brand)
    groupName = offerDetails[0]['groupName']
    basePrice= offerDetails[0]['basePrice']
    data_to_insert = {
        'Brand': device,
        'Model': groupName,
        'OneOffPrice': basePrice,
        # 其他字段数据可以继续添加
    }
    # SQL插入语句
    insert_query = '''
    INSERT INTO Phones (Brand, Model, OneOffPrice)
    VALUES (%(Brand)s, %(Model)s, %(OneOffPrice)s)
    '''
    try:
        # 执行插入语句
        cursor.execute(insert_query, data_to_insert)

        # 提交更改到数据库
        conn.commit()
        print("数据插入成功！")
    except Exception as e:
        # 发生错误时回滚
        conn.rollback()
        print(f"数据插入失败：{e}")
    print(groupName)
    print(basePrice)


def write_in_plans(brand):
    offerDetails = device(brand)
    associatedPrices = offerDetails[0]['associatedPrices']
    #print(len(associatedPrices))
    #print(associatedPrices[3])
    for i in range(len(associatedPrices)):
        info = associatedPrices[i]
        #print(info)
        try:
            with conn.cursor() as cursor:
                # 查询Phones表，找到对应Model的PhoneID
                groupName = offerDetails[0]['groupName']
                model = groupName  # 替换为要查询的手机型号
                sql = "SELECT * FROM Phones WHERE Model = %s"
                cursor.execute(sql, (model,))
                result = cursor.fetchone()
                #print(result)

                if result:
                    phone_id = result[0]
                    print(result[2])
                    basePrice = float(result[3])
                    month = int(info["priceLength"])
                    every = float(info["basePrice"])
                    if info["minimumDownPaymentAmount"] != None:
                        minp = float(info["minimumDownPaymentAmount"])
                    else:
                        minp = 0
                    plan_name = 'spark'+str(info["priceLength"])  # 替换为购买方案的名称
                    savings_amount = month*every+ minp-basePrice # 替换为对应的省钱金额
                    # 插入数据到PurchasePlans表
                    insert_sql = "INSERT INTO PurchasePlans (PhoneID, PlanName, SavingsAmount) VALUES (%s, %s, %s)"
                    cursor.execute(insert_sql, (phone_id, plan_name, savings_amount))
                    conn.commit()
                    print("数据插入成功！")

                else:
                    print(f"找不到型号为 '{result[2]}' 的手机。")
        except Exception as e:
            # 发生错误时回滚
            conn.rollback()
            print(f"数据插入失败：{e}")

def brand(brand):
    for item in data:
        if brand in item and 'group' in item:
            write_in_phones(brand)
            #device(item)
            #write_in_plans(item)
            #print(item)
    #print(data)

brand('oppo')
# 关闭游标和连接
cursor.close()
conn.close()



