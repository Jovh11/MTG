import pandas as pd

df = pd.read_json('new_version.json')
# print(df.columns)
df_parsed = df[['name', 'mana_cost', 'oracle_text', 'type_line', 'power', 'toughness', 'cmc', 'prices', 'set', 'rarity']]
df_parsed = df_parsed.loc[df_parsed['set'] == 'j22'].reset_index(drop=True)
creatures = df_parsed['type_line'].str.contains('Creature', case=False, na=False)
creatures_parsed = df_parsed[creatures].reset_index(drop=True)
non_creature = ~df_parsed['type_line'].str.contains('Creature', case=False, na=False)
non_creatures = df_parsed[non_creature].reset_index(drop=True)
creatures_parsed = creatures_parsed[['name', 'mana_cost', 'cmc','oracle_text', 'power', 'toughness', 'prices', 'set', 'rarity']]
non_creatures = non_creatures[['name', 'mana_cost','cmc' ,'oracle_text', 'prices', 'set', 'rarity']]
improved_creatures = creatures_parsed.dropna().reset_index(drop=True)
improved_noncreatures = non_creatures.dropna().reset_index(drop=True)
unsets = ['sunf', 'unf', 'und', 'ust', 'unh', 'ugl', 'cmb1', 'cmb2']

for index, row in improved_creatures.iterrows():
    oracle = row['oracle_text']
    name = str(row['name'])
    mana_cost = row['mana_cost']
    power = row['power']
    toughness = row['toughness']
    rarity = row['rarity']
    new_name = 'This Card'
    replacement = ' '
    replaced = '\n'
    prices = row['prices']
    usd = prices['usd']
    comma = ','
    empty = ''
    empty_filler = '_'
    pt_before = '*'
    pt_filler = '4'
    new_oracle = oracle.replace(name, new_name)
    newer_oracle = new_oracle.replace(replaced, replacement)
    newest_oracle = newer_oracle.replace(comma, replacement)
    new_mana = mana_cost.replace(empty, empty_filler)
    new_power = power.replace(pt_before, pt_filler)
    new_toughness = toughness.replace(pt_before, pt_filler)
    improved_creatures.loc[index, 'oracle_text'] = newest_oracle
    improved_creatures.loc[index, 'prices'] = usd
    improved_creatures.loc[index, 'power'] = new_power
    improved_creatures.loc[index, 'toughness'] = new_toughness
    # improved_creatures.astype({'power': 'float32', 'toughness': 'float32'})
    if mana_cost == empty:
        improved_creatures.loc[index, 'mana_cost'] = new_mana
    if oracle == empty:
        improved_creatures.loc[index, 'oracle_text'] = empty_filler
    if rarity == 'mythic':
        improved_creatures.loc[index, 'rarity'] = 3
    elif rarity == 'rare':
        improved_creatures.loc[index, 'rarity'] = 2
    elif rarity == 'uncommon':
        improved_creatures.loc[index, 'rarity'] = 1
    elif rarity == 'common':
        improved_creatures.loc[index, 'rarity'] = 0
    else:
        improved_creatures.loc[index, 'rarity'] = 5

improved_creatures = improved_creatures.dropna(subset=['prices']).reset_index(drop=True)
values = {'mana_cost': '_'}
improved_creatures = improved_creatures.fillna(value=values)
improved_creatures = improved_creatures[~improved_creatures.set.isin(unsets)]
improved_creatures = improved_creatures.replace({'power': {'1+4':5, '4+1':5}})
improved_creatures = improved_creatures.replace({'toughness': {'1+4': 5, '4+1':5}})
improved_creatures = improved_creatures.astype({'power':'float64', 'toughness':'float64'})
# improved_creatures.to_csv('creatures.csv', index=[0])
# improved_creatures.to_csv('oracle_creatures.csv', index=[0])
improved_creatures.to_csv('c3.csv', index=[0])

for index, row in improved_noncreatures.iterrows():
    # print(index)
    oracle = row['oracle_text']
    name = str(row['name'])
    mana_cost = row['mana_cost']
    rarity = row['rarity']
    new_name = 'This Card'
    replacement = ' '
    replaced = '\n'
    comma = ','
    empty = ''
    empty_fill = '_'
    new_oracle = oracle.replace(name, new_name)
    newer_oracle = new_oracle.replace(replaced, replacement)
    newest_oracle = newer_oracle.replace(comma, replacement)
    new_mana = mana_cost.replace(empty, empty_fill)
    prices = row['prices']
    usd = prices['usd']
    improved_noncreatures.loc[index, 'oracle_text'] = newest_oracle
    improved_noncreatures.loc[index,'prices'] = usd
    if mana_cost == empty:
        improved_noncreatures.loc[index,'mana_cost'] = new_mana
    if oracle == empty:
        improved_noncreatures.loc[index, 'oracle_text'] = empty_fill
    if rarity == 'mythic':
        improved_noncreatures.loc[index, 'rarity'] = 3
    elif rarity == 'rare':
        improved_noncreatures.loc[index, 'rarity'] = 2
    elif rarity == 'uncommon':
        improved_noncreatures.loc[index, 'rarity'] = 1
    elif rarity == 'common':
        improved_noncreatures.loc[index, 'rarity'] = 0
    else:
        improved_noncreatures.loc[index, 'rarity'] = 5
    
improved_noncreatures = improved_noncreatures.dropna(subset=['prices']).reset_index(drop=True)
values = {'mana_cost': '_'}
improved_noncreatures = improved_noncreatures.fillna(value='values')
improved_noncreatures = improved_noncreatures[~improved_noncreatures.set.isin(unsets)]
# improved_noncreatures.to_csv('noncreatures.csv', index=[0])
# improved_noncreatures.to_csv('oracle_noncreatures.csv', index=[0])
improved_noncreatures.to_csv('nc3.csv', index=[0])
# print(improved_noncreatures.iloc[15])