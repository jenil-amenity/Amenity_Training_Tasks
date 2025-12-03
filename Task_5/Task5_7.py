import pandas as pd

df = pd.read_csv('./sales_data.csv')
# Combining DataFrames (Use multiple small datasets):

# Concatenate two DataFrames vertically (stacking them).
df1 = df.head(5)
df2 = df.tail(6)

print("Concatenate two DataFrames \n",pd.concat([df1,df2], ignore_index=True))
print()

# Merge two DataFrames based on a common key column (like a SQL join).
print("Right join \n",pd.merge(df1,df2, on="OrderID", how="right"))
print()

df2 = df.head(5)
print("Left join \n",pd.merge(df1,df2, on="OrderID", how="left"))
print()
print("Outer join \n",pd.merge(df1,df2, on="OrderID", how="outer"))
print()

