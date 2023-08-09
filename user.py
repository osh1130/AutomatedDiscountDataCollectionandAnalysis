from telnetlib import EC

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
# 创建Chrome WebDriver选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 设置为headless模式，不显示浏览器窗口
chrome_options.add_argument("--disable-gpu")  # 禁用GPU加速，可避免一些兼容性问题

# 创建Chrome WebDriver并指定选项
driver = webdriver.Chrome(options=chrome_options)
#url = 'https://www.spark.co.nz/online/shop/products/oppo_find_n2_flip_group/?offerId=oppo127374spo&planId=mbundle051026&ifpId=interest_free_payment_over_36_months'  # 将链接替换为你要访问的网页链接
url = 'https://www.spark.co.nz/online/shop/handsets/?brand=oppo'
driver.get(url)
# 使用WebDriverWait来等待特定元素加载完成
# 这里使用例子，等待10秒钟，直到ID为'content'的元素加载完成
wait = WebDriverWait(driver, 10)
#element = wait.until(EC.presence_of_element_located((By.ID, 'content')))
# 获取完整页面的HTML
html = driver.page_source
# 通过BeautifulSoup解析页面内容
bf = BeautifulSoup(html, 'html.parser')
#print(bf)

def in_device():
    body = bf.find_all('div',{'class': 'indexesm__Box-sc-7wki3v-41 PaymentOptions__FullWidthContainer-sc-cobdti-0 dQJBaS hxqdWb'})
    for item in body:
        info = item.text
        #print(info)
        month = info.split(' ')[0]
        everymonth = info.split('$')[1].split('/')[0]
        if month == 'Pay':
            everymonth = everymonth.replace(',', '')
            oneoff = float(everymonth)
        else:
            save = int(month) * float(everymonth) -oneoff
            print(save,month)
            #print(month,everymonth)

def device_list():
    nums = bf.find_all('div', {'class': 'ProductGalleryCard__StyledLinkRegion-sc-1dpk72t-9 coZSkm'})
    nums = len(nums)
    prices = bf.find_all('p', {
        'class': 'indexesm__BaseStyle5-sc-7wki3v-3 indexesm__BodySMedium-sc-7wki3v-13 lgOwLa qDLeV ProductGalleryCard__DeviceOnlyText-sc-1dpk72t-5 hbguLE'})
    devives = bf.find_all('h5',{'class':'indexesm__BaseStyle5-sc-7wki3v-3 indexesm__SubheadingM-sc-7wki3v-9 lgOwLa gxHGdZ ProductGalleryCard__Title-sc-1dpk72t-3 kaoThv'})
    savings = bf.find_all('div', {'class': 'ProductGalleryCard__StyledLinkRegion-sc-1dpk72t-9 coZSkm'})
    for i in range(nums):
        price = prices[i].text
        price = price.split('$')[1]
        devive = devives[i].text
        print(devive,": ",price)

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
                    print(device_name,": ",price," ",saving," not gift")
                except:
                    gift = sale[0].find('p', {
                        'class': 'indexesm__BaseStyle5-sc-7wki3v-3 indexesm__BodySMedium-sc-7wki3v-13 hgqSRO qDLeV'})
                    gift = gift.text.split("[")[0]
                    print(device_name, ": ", price, " not saving", " ", gift)
            elif len(sale)==2:
                saving = sale[0].find('p', {
                    'class': 'indexesm__BaseStyle5-sc-7wki3v-3 indexesm__BodySMedium-sc-7wki3v-13 lgOwLa qDLeV'})
                saving = saving.text.split("over")[0]
                gift = sale[1].find('p',{'class':'indexesm__BaseStyle5-sc-7wki3v-3 indexesm__BodySMedium-sc-7wki3v-13 hgqSRO qDLeV'})
                gift = gift.text.split("[")[0]
                print(device_name, ": ", price, " ", saving," ",gift)
            elif len(sale) == 0:
                print(device_name, ": ", price, "not on sale：")
        except NoSuchElementException as e:
            print(device_name, ": ", price,"not on sale：", e)
# 关闭WebDriver
devices()
driver.quit()
print("END")
