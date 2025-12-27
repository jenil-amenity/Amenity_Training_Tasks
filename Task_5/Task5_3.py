import pandas as pd

# Filtering Data
def data_filtering(file_path):
    df = pd.read_csv(file_path)

    print("Data Whose quantity > 10\n",df[df['Quantity'] > 10])
    print()

    print("Data which have Electronics Category \n",df[df['Category'] == 'Electronics'])
    print()

    print("Filter Region West and Price < 50 \n", df[(df['Region']== 'West') & (df['Price'] < 50)])
    print()

    print("Product wise filtering \n", df[(df['Product'] == 'Laptop') | (df['Product'] == 'Keyboard') | (df['Product'] == 'Mouse')])
    print()

    print("Filtering out null values \n", df.dropna(subset=['Quantity']))

if __name__ == '__main__':
    data_filtering('./sales_data.csv')