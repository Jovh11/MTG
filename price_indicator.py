import pandas as pd

df = pd.read_csv('MTGML_test.csv', index_col=[0])
desired_row = df.loc[df['name'] == 'Fabled Hero']
oracle = desired_row['oracle_text']
print(oracle)