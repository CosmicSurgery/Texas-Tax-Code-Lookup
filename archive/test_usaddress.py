import usaddress
import pandas as pd
import numpy as np

df = pd.read_excel('Test Data Texas.xlsx',sheet_name=1)

l = df['Shipping Address'].to_numpy()
j = []

for i,k in enumerate(l):
    if type(k) is str:
        l[i] = k.replace('_x000D_\n',',')
        try:
            j.append(usaddress.tag(l[i]))
        except:
            pass

new_df = pd.DataFrame(j)
new_df.to_excel('test.xlsx')
print(new_df.head(10))
