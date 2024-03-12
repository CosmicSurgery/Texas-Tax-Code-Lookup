
def main():
    import usaddress
    import pandas as pd
    import numpy as np
    import collections
    from time import sleep
    import time
    import pandas as pd
    from utils import crawler
    from datetime import date

    t0 = time.time()

    df = pd.read_excel('Test Data Texas.xlsx',sheet_name=1)
    raw_addresses = df['Shipping Address'].to_numpy()   
    processed_adds = []

    f = open("log1.txt", "a")
    today = date.today()
    bad_addresses = []
    for i,k in enumerate(raw_addresses):
        
        if type(k) is str:
            raw_addresses[i] = raw_addresses[i].replace('_x000D_\n',',')
            raw_addresses[i] = raw_addresses[i].replace('\n',',')
            try:
                processed_adds.append(usaddress.tag(raw_addresses[i])[0])
            except Exception as error:
                bad_addresses.append(f"FAIL - Untaggable \n{k}\n~~~\n")
                processed_adds.append(collections.OrderedDict([('Recipient','bad')]))
    
    f.write(f"{today}\n")
    for k in np.unique(bad_addresses):
        f.write(k + "\n")
    f.close()
    new_df = pd.DataFrame(processed_adds)
    df['Street Address'] = new_df['AddressNumber'] + ' ' + new_df['StreetName'] + ' ' + new_df['StreetNamePostType']
    df['city'] = new_df['PlaceName']

    lookup_list = {}
    unique_adds = df[['Street Address', 'city', 'Shipping Zip']].drop_duplicates()
    unique_adds = unique_adds.dropna()

    for item in unique_adds.to_numpy():
        key = item[0]  # Extracting the first part of the address as the key
        lookup_list[key] = tuple(item)
    
    try:
        new_df, good, bad = crawler(lookup_list)
        merged_df = df.merge(new_df, how='left', left_on='Street Address', right_index=True)
        merged_df = merged_df.replace('NaN', '', regex=True)
        merged_df = merged_df.replace(np.nan, '', regex=True)
    except Exception as error:
        print(error)
        good, bad = ['test'], ['test']

    taggable = len(list(lookup_list.keys()))
    untaggable = len(np.unique(bad_addresses))

    t1 = time.time()
    total_time = t1-t0

    f = open("log1.txt", "a")
    f.write(str(lookup_list) + "\n")
    f.write(f"Pre-processing: taggable addresses - {taggable}, untaggable addresses - {untaggable}\n ")
    f.write(str(bad_addresses)+'\n')
    f.write(f"Processing: processed - {len(good)}, unprocessed - {len(bad)}\n ")
    f.write(str(bad)+'\n')

    f.write(str(len(list(lookup_list.keys()))) + f" total time: {total_time}\n")


if __name__ == '__main__':
    main()