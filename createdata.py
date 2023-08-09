import pymysql
from cryptography.fernet import Fernet

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='my_database')
cursor = conn.cursor()


create_phones_table = '''
CREATE TABLE Phones (
    PhoneID INT AUTO_INCREMENT PRIMARY KEY,
    Brand VARCHAR(255),
    Model VARCHAR(255),
    OneOffPrice DECIMAL(10, 2)
);
'''


create_spark_table = '''
CREATE TABLE SparkSale (
    DiscountID INT AUTO_INCREMENT PRIMARY KEY,
    PhoneID INT,
    SavingsAmount DECIMAL(10, 2),
    DiscountedPrice DECIMAL(10, 2),
    FreeGift TINYINT NOT NULL,
    GiftDescription VARCHAR(255),
    Date VARCHAR(255),
    FOREIGN KEY (PhoneID) REFERENCES Phones(PhoneID)
);
'''

# 执行创建表的SQL语句
#cursor.execute(create_phones_table)
cursor.execute(create_spark_table)

cursor.close()
conn.close()
