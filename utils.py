
def crawler(lookup_list):
    from time import sleep
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time
    import numpy as np

    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://gis.cpa.texas.gov/search")

    all_data = {}


    good = []
    bad = []

    for key in lookup_list.keys():

        time.sleep(1)

        input_add = driver.find_element(By.XPATH, '//*[@id="address"]')
        input_add.send_keys(lookup_list[key][0])

        input_city = driver.find_element(By.XPATH, '//*[@id="City"]')
        input_city.send_keys(lookup_list[key][1])

        input_zip = driver.find_element(By.XPATH, '//*[@id="ZipCode"]')
        input_zip.send_keys(lookup_list[key][2])

        driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[2]/div[2]/div[1]/div/div/div/form/div[7]/button[2]').click()
    
        time.sleep(5)

        tax_data = {}

        alert_element = driver.find_element(By.CSS_SELECTOR, '[role="alert"]')
        while 'Processing' in driver.find_element(By.CSS_SELECTOR, '[role="alert"]').text:
            time.sleep(2)
        if not alert_element.find_elements(By.XPATH, './/*'):
            print("No alert message found. Continuing...")

            # Find all tables containing tax information
            table_elements = driver.find_elements_by_xpath('//div[@class="table-container"]/table')


            for table in table_elements:
                rows = table.find_elements_by_tag_name('tr')
                jurisdiction_name = rows[0].find_element_by_tag_name('td').text
                tax_info = {rows[i].find_element_by_tag_name('th').text: rows[i].find_element_by_tag_name('td').text for i in range(1, len(rows))}

                if 'Type' in tax_info.keys():
                    tax_type = tax_info['Type']  # Directly assign the value of the 'Type' key
                    
                    # Add tax information to the dictionary
                    tax_data[f'{tax_type} CODE'] = tax_info['Code']
                    tax_data[f'{tax_type} RATE'] = tax_info['Tax Rate']
            
            good.append(key)
                    
        else:
            print("Alert message:", alert_element.text)
            tax_data['Fail'] = 'X'
            # Handle the alert message as needed
            bad.append(key)

        all_data[key] = tax_data

        input_add.clear()
        input_city.clear()
        input_zip.clear()

    driver.quit()
    return pd.DataFrame(data=all_data).T, good, bad

