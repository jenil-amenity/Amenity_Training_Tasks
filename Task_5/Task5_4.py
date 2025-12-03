import pandas as pd


df = pd.read_csv('./sales_data.csv')
# Data Cleaning & Manipulation 

print("Identifying Nan values\n", df.isna())
print(df.columns[df.isna().any()].tolist())
print()

print("Count Total missing values by columns\n",df.isna().sum())
print()

mean = df['Price'].mean().round(2)
print("Fill Missing values with means \n",df['Price'].fillna(mean))
print()

print("Fill In Categorical Column\n", df['Category'].fillna('Unknown'))
print()
df_no_na = df.dropna()

print("Length before drop >> ",len(df))
print("Droping rows tha have missing values\n",df_no_na)
print("Length after dropping >> ",len(df_no_na))
print()

dropclm = df.drop('Revenue',axis=1)
print("Dropping specific Column [Revenue]\n",dropclm)
print()

df['Total'] = df['Price']*df['Quantity']
print("Adding New Column that is total\n",df)
print()
print("Before conversion \n",df.info())

df['OrderDate'] = pd.to_datetime(df['OrderDate'])
print("After conversion \n",df.info())
print()

df['OrderMonth'] = pd.DatetimeIndex(df['OrderDate']).month
print("Adding Month Column\n",df)
print()

print("Rename column\n",df.rename(columns={'Total':'TotalBill'}))
print()

print("Removing duplicate rows\n",df.drop_duplicates())
print()

convdt = {'Price' : str}
df = df.astype(convdt)
print("Changing Datatype\n",df.dtypes)
print()

def discount(total, discount):
    dis = total * (discount / 100)
    return total - dis
df['GrandTotal'] = df['Total'].apply(lambda x: discount(x,10))
print("Adding GrandTotal Column with discount\n", df)