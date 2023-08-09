import os
import pymysql
import xlrd
import xlwt
from xlutils.copy import copy
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

device_list=[]
# 配置 SMTP 服务器和端口
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
# Gmail 邮箱的登录凭据
EMAIL_ADDRESS = 'sehunni1130@gmail.com'
PASSWORD = 'guphphezefccffcc'

# 获取当前日期
current_date = datetime.now().date()
name = 'OPPOdevices-%s.xls' % (str(current_date))

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='oppo')
cursor = conn.cursor()
#current_date = '2023-08-07'


# 获取当前Python文件所在的路径
current_directory = os.path.dirname(os.path.abspath(__file__))
# 构建完整的文件路径
save = 0
file_path = os.path.join(current_directory, name)
# 检查文件是否存在
if os.path.exists(file_path):
    save = 1
    print(f"文件 '{name}' 存在于当前路径下。")
else:
    # 创建Chrome WebDriver选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 设置为headless模式，不显示浏览器窗口
    chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速，可避免一些兼容性问题
    # chromedriver_path ='C:\\ProgramData\\\Jenkins\\.jenkins\\workspace\\oppoandspark\\venv\\Lib\\site-packages\\selenium\\webdriver\\chrome\\webdriver'
    # 创建Chrome WebDriver并指定选项
    # driver = webdriver.Chrome(options=chrome_options,executable_path=os.environ['CHROMEDRIVER_PATH'])
    # url = 'https://www.spark.co.nz/online/shop/products/oppo_find_n2_flip_group/?offerId=oppo127374spo&planId=mbundle051026&ifpId=interest_free_payment_over_36_months'  # 将链接替换为你要访问的网页链接
    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://www.spark.co.nz/online/shop/handsets/?brand=oppo'
    driver.get(url)
    # 使用WebDriverWait来等待特定元素加载完成
    # 这里使用例子，等待10秒钟，直到ID为'content'的元素加载完成
    wait = WebDriverWait(driver, 10)
    # element = wait.until(EC.presence_of_element_located((By.ID, 'content')))
    # 获取完整页面的HTML
    html = driver.page_source
    # 通过BeautifulSoup解析页面内容
    bf = BeautifulSoup(html, 'html.parser')


def devices():
    devices = bf.find_all('div', {'class': 'ProductGalleryCard__StyledLinkRegion-sc-1dpk72t-9 coZSkm'})
    for device in devices:
        device_name = device.find('h5',{'class':'indexesm__BaseStyle5-sc-7wki3v-3 indexesm__SubheadingM-sc-7wki3v-9 lgOwLa gxHGdZ ProductGalleryCard__Title-sc-1dpk72t-3 kaoThv'})
        device_name = device_name.text
        #print(device_name.text)
        price = device.find('p', {
        'class': 'indexesm__BaseStyle5-sc-7wki3v-3 indexesm__BodySMedium-sc-7wki3v-13 lgOwLa qDLeV ProductGalleryCard__DeviceOnlyText-sc-1dpk72t-5 hbguLE'})
        price = price.text

        try:
            # 尝试定位元素
            sale = device.find_all('div', {'class': 'indexesm__Box-sc-7wki3v-41 jTbaO'})
            if len(sale)==1:
                try:
                    saving = sale[0].find('p',{'class':'indexesm__BaseStyle5-sc-7wki3v-3 indexesm__BodySMedium-sc-7wki3v-13 lgOwLa qDLeV'})
                    saving = saving.text.split("over")[0]
                    item = [device_name,price,saving,"not gift"]
                    #print(device_name,": ",price," ",saving," not gift")
                except:
                    gift = sale[0].find('p', {
                        'class': 'indexesm__BaseStyle5-sc-7wki3v-3 indexesm__BodySMedium-sc-7wki3v-13 hgqSRO qDLeV'})
                    gift = gift.text.split("[")[0]
                    item = [device_name, price, "not saving", gift]
                    #print(device_name, ": ", price, " not saving", " ", gift)
                #device_list.append(item)
            elif len(sale)==2:
                saving = sale[0].find('p', {
                    'class': 'indexesm__BaseStyle5-sc-7wki3v-3 indexesm__BodySMedium-sc-7wki3v-13 lgOwLa qDLeV'})
                saving = saving.text.split("over")[0]
                gift = sale[1].find('p',{'class':'indexesm__BaseStyle5-sc-7wki3v-3 indexesm__BodySMedium-sc-7wki3v-13 hgqSRO qDLeV'})
                gift = gift.text.split("[")[0]
                item = [device_name, price, saving, gift]
                #print(device_name, ": ", price, " ", saving," ",gift)
            elif len(sale) == 0:
                item = [device_name, price, "not saving", "not gift"]
                #print(device_name, ": ", price, "not on sale：")
            device_list.append(item)
            write_in(item)
            write_sql(item)
        except NoSuchElementException as e:
            print('not found', e)


def write_in(data):
    workBook = xlrd.open_workbook(name)
    worksheet = workBook.sheet_by_name('Spark')
    rows = worksheet.nrows  # 行数
    newWb = copy(workBook)
    newWs = newWb.get_sheet(0)
    newWs.write(rows, 0, data[0])
    newWs.write(rows, 1, data[1])
    newWs.write(rows, 2, data[2])
    newWs.write(rows, 3, data[3])
    #newWs.write(0, 3, rows)
    # print(rows)
    newWb.save(name)


def write_sql(data):
    Model = data[0].split(' ',1)[1]
    OneOffPrice = data[1].split('$')[1].replace(',','')
    data_to_insert = {
        'Brand': "OPPO",
        'Model': Model,
        'OneOffPrice': float(OneOffPrice),
        # 其他字段数据可以继续添加
    }
    # SQL插入语句
    insert_query = '''
            INSERT INTO Phones (Brand, Model, OneOffPrice)
            VALUES (%(Brand)s, %(Model)s, %(OneOffPrice)s)
            '''
    try:
        # 查询数据库中是否已经存在该手机型号
        query = "SELECT * FROM Phones WHERE Model = %s"
        cursor.execute(query, (Model))
        existing_rows = cursor.fetchone()
        if not existing_rows:
            # 执行插入语句
            cursor.execute(insert_query, data_to_insert)
            # 提交更改到数据库
            conn.commit()
            print("phone插入成功！")
        #else:
        #    print("phone exist")
        phone_id = existing_rows[0]
        query = "SELECT * FROM SparkSale WHERE PhoneID = %s AND Date = %s"
        cursor.execute(query, (phone_id, str(current_date)))
        existing = cursor.fetchone()
        #print(existing)
        if not existing:
            savingsamount = 0.0
            if data[2] != 'not saving':
                savingsamount = float(data[2].split('$')[1])
            discountedprice = float(existing_rows[3])-savingsamount
            freegift = 0
            giftdescription = 'not gift'
            if data[3] != 'not gift':
                freegift = 1
                giftdescription = data[3]
            date = str(current_date)
            insert_sql = "INSERT INTO SparkSale (PhoneID, SavingsAmount, DiscountedPrice,FreeGift,GiftDescription,Date) VALUES (%s, %s, %s,%s,%s,%s)"
            cursor.execute(insert_sql, (phone_id, savingsamount, discountedprice,freegift,giftdescription,date))
            conn.commit()
            print("数据插入成功！")
    except Exception as e:
            # 发生错误时回滚
            conn.rollback()
            print(f"saving插入失败：{e}")

def send_email():
    smtp_server = SMTP_SERVER
    smtp_port = SMTP_PORT
    user_email = EMAIL_ADDRESS
    recipient_email = 'sehunni1130@gmail.com'
    subject = 'OPPO * SPARK'
    message = 'The sale info in attachment.'

    # 创建 MIMEMultipart 邮件对象
    msg = MIMEMultipart()
    msg['From'] = user_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # 添加邮件正文
    msg.attach(MIMEText(message, 'plain'))

    # 添加附件
    attachment_path = name  # 替换为附件文件的路径
    with open(attachment_path, 'rb') as file:
        attachment = MIMEApplication(file.read())
    attachment.add_header('Content-Disposition', 'attachment', filename=str(name))
    msg.attach(attachment)

    # 连接到 SMTP 服务器
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # 启用 TLS 加密
    server.login(user_email, PASSWORD)

    # 构造邮件内容
    #msg = f"From: {user_email}\nTo: {recipient_email}\nSubject: {subject}\n\n{message}"

    # 发送邮件
    server.sendmail(user_email, recipient_email, msg.as_string())
    server.quit()

if save == 0:
    workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
    sheet1 = workbook.add_sheet("Spark")  # 新建sheet
    workbook.save(name)  # 保存
    write_in(["Device Name", "One off Price", "Saving", "Gift"])
    devices()
    # 关闭WebDriver
    driver.quit()
    # print(device_list)
    print("END")
    send_email()
    # 关闭游标和连接
    cursor.close()
    conn.close()

