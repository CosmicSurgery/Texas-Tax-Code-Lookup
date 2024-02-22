def crawl(lookup_list):
#   lookup_list is a dictionary of tuples where the key is the street address, and the tuple is (address, city, zip)

    from time import sleep
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time

    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://gis.cpa.texas.gov/search")

    all_data = {}

    for key in lookup_list.keys():

        time.sleep(1)

        input_add = driver.find_element(By.XPATH, '//*[@id="address"]')
        input_add.send_keys(lookup_list[key][0])

        input_city = driver.find_element(By.XPATH, '//*[@id="City"]')
        input_city.send_keys(lookup_list[key][1])

        input_zip = driver.find_element(By.XPATH, '//*[@id="ZipCode"]')
        input_zip.send_keys(lookup_list[key][2])

        input_search = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[2]/div[2]/div[1]/div/div/div/form/div[7]/button[2]').click()
    

        # save_copy = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div[1]/div/span/button').click()

        time.sleep(5)

        tax_data = {}

        alert_element = driver.find_element(By.CSS_SELECTOR, '[role="alert"]')
        if not alert_element.find_elements(By.XPATH, './/*'):
            print("No alert message found. Continuing...")



            # elements = driver.find_elements_by_xpath('//div[@class="table-container"]')
            # print(elements)
            # sub_elements = driver.find_elements_by_xpath('//div[@class="mt-5"]/div')

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

                # tax_type = tax_info.get('Type', '')
                # if tax_type == 'STATE':
                #     tax_data['STATE CODE'] = tax_info['Code']
                #     tax_data['STATE RATE'] = tax_info['Tax Rate']
                # elif tax_type == 'CITY':
                #     tax_data['CITY CODE'] = tax_info['Code']
                #     tax_data['CITY RATE'] = tax_info['Tax Rate']
                # elif tax_type == 'TRANSIT':
                #     tax_data['TRANSIT CODE'] = tax_info['Code']
                #     tax_data['TRANSIT RATE'] = tax_info['Tax Rate']

            print(tax_data) 

        else:
            print("Alert message:", alert_element.text)
            # Handle the alert message as needed

        all_data[key] = tax_data

        input_add.clear()
        input_city.clear()
        input_zip.clear()
    
    print(pd.DataFrame(data=all_data).T)

    driver.quit()


if __name__ == '__main__'   :
    print('crawler loaded')
    lookup_list = {'7005 Rain Creek':('7005 Rain Creek', 'Austin','78759'), 'debug':('bad','da','12345'), '6905 Nottoway Lane':('6905 Nottoway Lane', 'Lumberton', '77657')}
    crawl(lookup_list)