
def main():
    import usaddress
    import pandas as pd
    import numpy as np
    import collections
    from time import sleep
    import pandas as pd
    from utils import crawler

    df = pd.read_excel('Test Data Texas.xlsx',sheet_name=1)
    raw_addresses = df['Shipping Address'].to_numpy()   
    processed_adds = []

    f = open("log1.txt", "a")

    for i,k in enumerate(raw_addresses):
        if type(k) is str:
            raw_addresses[i] = raw_addresses[i].replace('_x000D_\n',',')
            raw_addresses[i] = raw_addresses[i].replace('\n',',')
            try:
                processed_adds.append(usaddress.tag(raw_addresses[i])[0])
            except Exception as error:
                f.write("FAIL - ", error)
                processed_adds.append(collections.OrderedDict([('Recipient','bad')]))

    new_df = pd.DataFrame(processed_adds)
    df['Street Address'] = new_df['AddressNumber'] + ' ' + new_df['StreetName'] + ' ' + new_df['StreetNamePostType']
    df['city'] = new_df['PlaceName']

    lookup_list = {}
    unique_adds = df[['Street Address', 'city', 'Shipping Zip']].drop_duplicates()
    unique_adds = unique_adds.dropna()

    for item in unique_adds.to_numpy():
        key = item[0]  # Extracting the first part of the address as the key
        lookup_list[key] = tuple(item)
      
    new_df = crawler(lookup_list)
    merged_df = df.merge(new_df, how='left', left_on='Street Address', right_index=True)
    merged_df = merged_df.replace('NaN', '', regex=True)
    merged_df = merged_df.replace(np.nan, '', regex=True)

if __name__ == '__main__':
    main()