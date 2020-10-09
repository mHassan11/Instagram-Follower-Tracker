from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import configparser as cfg
import pandas as pd
import datetime


# initialize the webdrivers
driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://www.instagram.com/')
# Get username and password from config.cfg
config = cfg.ConfigParser()
config.read('config.cfg')
uname = config.get('creds', 'username')
passWord = config.get('creds', 'password')
# Wait
driver.implicitly_wait(10)
# Sign In Using Username & Password
searchbox = driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input')
searchbox.send_keys(uname)
searchbox = driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input')
searchbox.send_keys(passWord)
searchBtn = driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')
searchBtn.click()
# Skip the pop-ups appeared on sign in
saveLogin = driver.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/div/div/div/div/button')
saveLogin.click()
notifBtn = driver.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]')
notifBtn.click()
# Navigate to the profile
driver.get('https://www.instagram.com/'+uname+'/followers/')
# Get the number of followers
temp = 0
max = 0
profileHtml = driver.page_source
soup = BeautifulSoup(profileHtml, "html.parser")
for e in soup.find_all(class_="g47SY"):
    max = e.get_text()
    # print('max = '+str(max))
    # print("temp = "+str(temp))
    if(int(max) >= int(temp)):
        temp = max
# Open Followers Pop Up
followersBtn = driver.find_element_by_xpath(
    '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
followersBtn.click()
# Scroll The followers Pop up
fBody = driver.find_element_by_xpath("//div[@class='isgrP']")
scroll = 0
while scroll < 100:
    driver.execute_script(
        'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
    time.sleep(.5)
    scroll += 1

fList = driver.find_elements_by_xpath("//div[@class='isgrP']//li")

#followers_list
follower_list = []
for each_f in fList:
    f_name = each_f.text.split('\n')[0]
    follower_list.append(f_name)
#save in csv


follower_df = pd.read_csv("followers.csv")
follower_df = follower_df.reset_index(drop=True)

time_now = datetime.datetime.now() #time right now
new_df = pd.DataFrame()
new_df[time_now] = follower_list
new_df = new_df.reset_index(drop=True)

df = [follower_df, new_df]
df_final = pd.concat(df, axis=1)
df_final.to_csv("followers.csv", index=False)

driver.close()