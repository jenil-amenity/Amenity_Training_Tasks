import pandas as pd

df = pd.read_csv('./sales_data.csv')
##Data Selection & Indexing:
print("Products >> ",df['Product'])
print()

print("Columns Data >>",df[['Product','Price','Quantity']])
print()

print("Specific Row >> ",df.iloc[3])
print()

print("Indexing 5 to 10 >> ",df.iloc[5:10])
print()

df = df.set_index('OrderID')
specific_row = df.loc['ORD006']

print("Fetch through Index >> ",specific_row)
print()

print("Columns with indexing >> \n",df.loc[['ORD002','ORD005'], ['Product','Region']])
print()

print("Columns with indexing >> \n",df.iloc[[0,2,4], [1,3]])