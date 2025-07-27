import pandas as pd

try:
    df = pd.read_csv('input_file.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('input_file.csv', encoding='ISO-8859-1')

df.to_csv('output_file.csv', index=False, encoding='utf-8-sig')
