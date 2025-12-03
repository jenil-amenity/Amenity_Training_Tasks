import pandas as pd

df = pd.read_csv('./sales_data.csv')
##Sorting & Ranking:

# Sort the DataFrame by a single column in ascending order.
print("Print Ascending by columns\n", df.sort_values('Price'))
print()

# Sort the DataFrame by a single column in descending order.
print("Print Decending by columns\n", df.sort_values('Revenue', ascending=False))
print()

# Sort the DataFrame by multiple columns.
print("Sort by multiple columns \n", df.sort_values(['Region','Price'],ascending=[True, False]))
