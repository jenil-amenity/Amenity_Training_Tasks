import pandas as pd

df = pd.read_csv('./sales_data.csv')
##Loading & Initial Inspection
print("Head",df.head(7))
print()
print("Tail",df.tail(7))
print()
print("Shape",df.shape)
print()
print("Column Names >> ",df.columns)
print()
print("Column Type >> ",df.dtypes)
print()
print("Satistical Summary >> ",df.describe())
print()
print("Satistical Summary of All Columns >> ",df.describe(include='all'))
print()
print("Unique values >> ",df.nunique())
print()


