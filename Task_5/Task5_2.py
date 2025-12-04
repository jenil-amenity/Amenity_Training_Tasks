import pandas as pd

##Data Selection & Indexing:
def selection_indexing(file_path):

    df = pd.read_csv(file_path)
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
    
if __name__ == '__main__':
    selection_indexing('./sales_data.csv')