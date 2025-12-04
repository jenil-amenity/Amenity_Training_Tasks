import pandas as pd

#Sorting & Ranking:
def sorting_ranking(file_path):
    df = pd.read_csv('./sales_data.csv')

    # Sort the DataFrame by a single column in ascending order.
    print("Print Ascending by columns\n", df.sort_values('Price'))
    print()

    # Sort the DataFrame by a single column in descending order.
    print("Print Decending by columns\n", df.sort_values('Revenue', ascending=False))
    print()

    # Sort the DataFrame by multiple columns.
    print("Sort by multiple columns \n", df.sort_values(['Region','Price'],ascending=[True, False]))

if __name__ == '__main__':
    sorting_ranking('./sales_data.csv')
