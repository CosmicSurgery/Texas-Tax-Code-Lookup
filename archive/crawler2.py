import usaddress
import pandas as pd
import numpy as np
import collections


def crawl():
#   lookup_list is a dictionary of tuples where the key is the street address, and the tuple is (address, city, zip)

    from time import sleep
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time

    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://gis.cpa.texas.gov/search")

    all_data = {}

    df = pd.read_excel('Test Data Texas2.xlsx',sheet_name=0)

    def clean_df(df):
        list_add = []
        j = []
        for i in range(len(df)):
            list_add.append(str(df['ship to address1'].iloc[i]) + ', ' + str(df['ship to address2'].fillna('').iloc[i]))
            try:
                j.append(usaddress.tag(list_add[-1])[0])
            except:
                j.append(collections.OrderedDict([('Recipient','bad')]))

        new_df = pd.DataFrame(j)
        nans = ~new_df['AddressNumber'].isna()
        new_df=new_df[nans]
        new_df.fillna('', inplace=True)
        df['Street Address'] = (new_df['AddressNumber'] + ' ' + new_df['StreetNamePreType'] + ' ' + 
                new_df['StreetNamePreDirectional'] + ' ' + new_df['StreetName'] + ' ' + 
                new_df['StreetNamePostType'] + ' ' + new_df['StreetNamePostDirectional'])
        lookup_list = {}
        debug = df[['Street Address', 'ship to city', 'ship to zip']][nans].drop_duplicates()
        for item in debug.to_numpy():
            key = item[0]  # Extracting the first part of the address as the key
            lookup_list[key] = tuple(item)

        return df, lookup_list

    df, lookup_list = clean_df(df)
    # lookup_list = {'7005 Rain Creek Pkwy': ('7005 Rain Creek Pkwy', 'Austin', '78759'), '6905 Nottoway Lane': ('6905 Nottoway Lane', 'Lumberton', '77657')}

    for key in lookup_list.keys():

        time.sleep(1)

        input_add = driver.find_element(By.XPATH, '//*[@id="address"]')
        input_add.send_keys(lookup_list[key][0])

        input_city = driver.find_element(By.XPATH, '//*[@id="City"]')
        input_city.send_keys(lookup_list[key][1])

        input_zip = driver.find_element(By.XPATH, '//*[@id="ZipCode"]')
        input_zip.send_keys(lookup_list[key][2])

        input_search = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[2]/div[2]/div[1]/div/div/div/form/div[7]/button[2]').click()
    
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

            print(tax_data) 

        else:
            print("Alert message:", alert_element.text)
            tax_data['Fail'] = 'X'
            # Handle the alert message as needed

        all_data[key] = tax_data

        input_add.clear()
        input_city.clear()
        input_zip.clear()

    driver.quit()
    new_df = pd.DataFrame(data=all_data).T
    merged_df = df.merge(new_df, how='left', left_on='Street Address', right_index=True)
    merged_df = merged_df.replace('NaN', '', regex=True)
    merged_df = merged_df.replace(np.nan, '', regex=True)

    merged_df.to_excel('debug2.xlsx')


if __name__ == '__main__'   :
    print('crawler loaded')
    crawl()