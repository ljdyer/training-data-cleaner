from numpy import append
import pandas as pd
import random

data = pd.read_excel('kirin.xlsx')
data = data.applymap(lambda x: x.replace('\n', ''))

write_data_path = 'kirin_dataset.xlsx'

# ====================
def write_excel(df: pd.DataFrame, path: str):
    """Write pandas dataframe to Excel file"""

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    sheet_name = 'training_data'
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column(0, 1, 50)  # First and second columns
    writer.save()


# ====================
def append_row_to_df(df, JA, EN):

    return pd.concat([df, pd.DataFrame({'JA': JA, 'EN': EN}, index=[0])])


# ====================
def get_random_jp_and_en(df):

    random_row = data.sample(1).iloc[0]
    return random_row['JA'], random_row['EN']



data.columns = ['JA', 'EN']
data = append_row_to_df(data, 'hello', 'hello')
print(get_random_jp_and_en(data))

DOUBLE_DUP_NUMS = {
    1: 10,
    2: 5,
    3: 2
}

for num_to_add, amount in DOUBLE_DUP_NUMS.items():
    for _ in range(amount):
        ja, en = get_random_jp_and_en(data)
        data = append_row_to_df(data, ja, en)



SOURCE_DUP_NUMS = {
    1: 10,
    2: 5,
    3: 2
}

def shuffle_sentence(sentence: str) -> str:
    words = sentence.split()
    return ' '.join(random.sample(words, len(words)))

for num_to_add, amount in SOURCE_DUP_NUMS.items():
    for _ in range(amount):
        ja, en = get_random_jp_and_en(data)
        data = append_row_to_df(data, ja, shuffle_sentence(en))



for i in range(len(data)):
    rand_num = random.randrange(10)
    if rand_num == 0:
        data.iloc[i]['JA'] = ''
        data.iloc[i]['EN'] = ''
    elif rand_num == 1:
        data.iloc[i]['JA'] = ''
    elif rand_num == 2:
        data.iloc[i]['EN'] = ''

data = data.sample(frac=1).reset_index(drop=True)
print(data)

write_excel(data, write_data_path)