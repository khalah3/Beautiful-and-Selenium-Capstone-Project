#This project will use a Zillow search provided in the URL below to find the address,price,
#and link of every result from the search criteria using Beautiful soup to read the data.
#Selenium is then used to record these results in a good form and submit all the responses.

import time
import selenium
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium  import webdriver

#Selenium setup
Google_Form_url='https://docs.google.com/forms/d/e/1FAIpQLSfbXciKXyj4p_-OrC_1mtlCv0ZfxObLaCpmpjnpuJDjhlptcw/viewform?usp=sf_link'
chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach',True)
driver=webdriver.Chrome(options=chrome_options)



#BeautifulSoup Setup
Zillow_url='https://appbrewery.github.io/Zillow-Clone/'
zillow_response=requests.get(url=Zillow_url)
soup=BeautifulSoup(zillow_response.text, 'html.parser')


#Lists to contain links,prices, and addresses
search_links=[]
price_tags=[]
addresses=[]

#extract search links and add them to the search_links list using append
search=soup.find_all(name='a',class_='property-card-link')
for each_search in search:
    search_link=each_search['href']
    search_links.append(search_link)
#print the search_links output in a list
print(search_links)

#extract prices for each search link and add them to the price_tags list using append with some
#output formatting using replace
prices=soup.find_all(name='span',class_='PropertyCardWrapper__StyledPriceLine')
for each_price in prices:
    price=each_price.text
    price_without_comma=price.replace(',','')
    final_price=price_without_comma[:5]
    price_tags.append(final_price)


#Add each pirce to the price_tags lists
print(price_tags)

#extract address for each search link and add them to the addresses list using append with some
#output formatting using strip,split, and delitem, and then append each address to addresses list
addresses_all=soup.find_all(name='address')
#print(addresses_all)
for each_address in addresses_all:
    address=each_address.text.strip().split(',')
    address.__delitem__(0)
    addresses.append(','.join(address[0:3]))

#print the addresses list
print(addresses)



# Use selenium for google forms to submit the price,address,and link for each home. Since there
#are 44 homes you should end up with 44 responses in the google form.

for n in range(len(search_links)):
    driver.get(url=Google_Form_url)
    time.sleep(1)
    search_answer=driver.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_answer = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_answer = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(1)
    search_answer.send_keys(search_links[n])
    price_answer.send_keys(price_tags[n])
    address_answer.send_keys(addresses[n])
    submit = driver.find_element(By.XPATH,'/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span')
    submit.click()
