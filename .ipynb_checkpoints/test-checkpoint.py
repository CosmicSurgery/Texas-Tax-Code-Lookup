from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://gis.cpa.texas.gov/search")

time.sleep(1)

nav_latlong= driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[2]/ul/li[3]/a/a').click()

input_lat = driver.find_element(By.XPATH, '//*[@id="latitude"]')
input_lat.send_keys("30.307313")

input_long = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[2]/div[2]/div[3]/div/div/div/form/div[3]/div/input')
input_long.send_keys("-97.739742")

input_search = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[2]/div[2]/div[3]/div/div/div/form/div[5]/button[2]').click()

# save_copy = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div[1]/div/span/button').click()

time.sleep(5)


# elements = driver.find_elements_by_xpath('//div[@class="table-container"]')
# print(elements)
# sub_elements = driver.find_elements_by_xpath('//div[@class="mt-5"]/div')

# Find all tables containing tax information
table_elements = driver.find_elements_by_xpath('//div[@class="table-container"]/table')

tax_data = {}

for table in table_elements:
    rows = table.find_elements_by_tag_name('tr')
    jurisdiction_name = rows[0].find_element_by_tag_name('td').text
    tax_info = {rows[i].find_element_by_tag_name('th').text: rows[i].find_element_by_tag_name('td').text for i in range(1, len(rows))}

    tax_data[jurisdiction_name] = tax_info

df = pd.DataFrame(data=tax_data)

print(df.head())

driver.quit()