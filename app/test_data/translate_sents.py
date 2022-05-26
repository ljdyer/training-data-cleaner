import pandas as pd
from googletrans import Translator

sent_file_path = 'kirin_jp_wiki_sents.txt'
en_sent_file_path = 'kirin_sents_en.txt'

# ====================
def write_excel(df: pd.DataFrame, path: str):
    """Write pandas dataframe to Excel file"""

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    sheet_name = 'training_data'
    df = df.applymap(escape_for_excel)
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column(0, 1, 50)  # First and second columns
    writer.save()


# ====================
with open(sent_file_path, encoding='utf8') as f:
    sents = f.readlines()


translator = Translator()
translations = []

for s in sents:
    translations.append(translator.translate(s).text)

with open(en_sent_file_path, 'w', encoding='utf8') as f:
    f.write('\n'.join(translations))