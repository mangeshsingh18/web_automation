from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import psycopg2


# # Database Connection ====================================================================*****************************************************************==========================================
# db = psycopg2.connect(host="localhost", database="postgres",user="postgres", password="Mangesh@123", port="5432")
# mycursor = db.cursor()

# table = '''create table Flipkart(Name varchar (255), Description varchar (255), Price varchar (255)) '''
# mycursor.execute(table)
# db.commit()


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.maximize_window()

# flipkart
driver.get("http://www.flipkart.in")
print(driver.title)
driver.find_element(By.XPATH, "/html/body/div[2]/div/div/button").click()

SearchBar = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input")
SearchBar.click()
time.sleep(2)
SearchBar.send_keys("Pixle 7")
time.sleep(2)

SearchButton = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[1]/div[2]/div[2]/form/div/button")
SearchButton.click()
time.sleep(3)

name = driver.find_elements(By.XPATH,'//div[(@class="_4rR01T")]')
time.sleep(1)

description = driver.find_elements(By.XPATH,'//div[(@class="fMghEO")]')
time.sleep(1)

price = driver.find_elements(By.XPATH,'//div[(@class="_30jeq3 _1_WHN1")]')
time.sleep(3)

for n,d,p in zip(name, description, price):
    Name = n.text
    Description = d.text
    Price = p.text

    data = [Name, Description, Price]
    print(data)

    db = psycopg2.connect(host="localhost", database="postgres",user="postgres", password="Mangesh@123", port="5432")
    mycursor = db.cursor()
    Insert = '''INSERT INTO Flipkart values(%s, %s, %s)'''
    mycursor.execute(Insert, data)
    db.commit()
    print("======================================== Data Inserted ========================================")

time.sleep(10)

driver.quit()











