import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import psycopg2

# # Database Connection ====================================================================*****************************************************************==========================================
# db = psycopg2.connect(host="localhost", database="postgres",user="postgres", password="Mangesh@123", port="5432")
# mycursor = db.cursor()

# table = '''create table Amazon_Samsung(Description varchar (255), Price varchar (255), Brand varchar (255), Model_name varchar (255), Network_service_provider varchar (255), OS varchar (255), cellular_technology varchar (255)) '''
# mycursor.execute(table)
# db.commit()

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.maximize_window()

driver.get("https://www.amazon.in/")
print(driver.title)
time.sleep(2)

search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[2]/div[1]/input"))
    )
search.click()
time.sleep(2)
search.send_keys("Samsung")
time.sleep(2)

button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/header/div/div[1]/div[2]/div/form/div[3]/div/span/input"))
    )
button.click()
time.sleep(3)

phone = WebDriverWait(driver,10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//span[@class="a-size-medium a-color-base a-text-normal"]'))
)
time.sleep(2)
Phones = phone
# print(Phones)
print(len(phone))

for p in phone:
    p.click()
    time.sleep(5)

    driver.switch_to.window(driver.window_handles[1])

    des = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="productTitle"]')))
    time.sleep(2)
    Description = des.text
    print(Description)
    try:
        price = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]'))
        )
    except:
        price = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//span[@class="a-offscreen"]'))
        )

    time.sleep(2)
    Price = price.text
    Price = re.sub("00", "", Price)
    print(Price)

    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//table[@class="a-normal a-spacing-micro"]'))
    )
    time.sleep(2)
    Table = table.text
    # print(Table)
    
    try:
        brand = re.search('Brand.*', Table).group()
    except:
        brand = ""

    brand= re.sub('Brand', "", brand)
    print(brand)

    try:
        Model_name = re.search('Model Name.*', Table).group()
    except:
        Model_name = ""

    Model_name= re.sub('Model Name', "", Model_name)
    print(Model_name)

    try:
        Network_service_provider = re.search('Network Service Provider.*', str(Table)).group()
    except:
        Network_service_provider = ""

    Network_service_provider = re.sub('Network Service Provider', "", Network_service_provider)
    print(Network_service_provider)

    try:
        os = re.search("OS.*", Table).group()
    except:
        os = ""

    os = re.sub("OS","",os)
    print(os)

    try:
        cellular_technology = re.search("Cellular Technology.*", Table).group()
    except:
        cellular_technology = ""

    cellular_technology = re.sub("Cellular Technology", "", str(cellular_technology))
    print(cellular_technology)

    data = [Description, Price, brand, Model_name, Network_service_provider, os, cellular_technology]
    print(data)

    driver.close()

    driver.switch_to.window(driver.window_handles[0])

    print("\n")
    print("################################################################################################")

    db = psycopg2.connect(host="localhost", database="postgres",user="postgres", password="Mangesh@123", port="5432")
    mycursor = db.cursor()
    Insert = '''INSERT INTO Amazon_Samsung values(%s, %s, %s, %s, %s, %s, %s)'''
    mycursor.execute(Insert, data)
    db.commit()
    print("======================================== Data Inserted ========================================")


    print("\n")

time.sleep(5)

driver.quit()






















