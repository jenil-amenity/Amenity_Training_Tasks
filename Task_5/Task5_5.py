import pandas as pd

# Grouping & Aggregation:
def grouping_aggr(file_path):
    df = pd.read_csv('./sales_data.csv')

    #Group data by a single column (e.g., 'Category') and calculate the sum of another column (e.g., 'Revenue') for each group.
    print("Group data by a single column sum\n", df.groupby('Category')['Revenue'].sum())
    print()

    # Group data by a single column and calculate the mean of another column.
    print("Group by single column Mean\n",df.groupby('Region')['Revenue'].mean())
    print()

    # Group data by multiple columns (e.g., 'Region', 'Category') and count the number of occurrences in each group.
    print("Group data by multiple columns and count accurence\n",df.groupby(['Region','Category']).size())
    print()

    # Find the minimum and maximum values of a numerical column for each group.
    print("Price min and max value by category >> \n ",df.groupby('Category')[['Price']].agg(['min','max']))
    print()

    # Calculate the number of unique items in a column for each group (e.g., unique products per category).

    print("Unique products per category >> \n",df.groupby('Category')['Product'].nunique())
    print()
    # Get the size of each group after grouping.
    print("Get size of each group after grouping \n",df.groupby('Region').size())
    print()
    # Use agg() to apply multiple aggregation functions at once after grouping.
    print("Use of agg() \n",df.groupby('Category').agg({'Price':'mean','Revenue':'sum', 'Quantity': 'count'}))

if __name__ == '__main__':
    grouping_aggr('./sales_data.csv')