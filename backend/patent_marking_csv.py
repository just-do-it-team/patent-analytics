import pandas as pd
import numpy as np
from tqdm import tqdm
pd.set_option('display.max_columns', None)
import warnings
warnings.filterwarnings('ignore')

orgs = pd.read_csv(r"F:\DATASETS\lct2024\datasets\DatasetOrg_short.csv", delimiter=';')
# print(orgs.columns)
# Index(['id_company', 'full_name', 'short_name', 'inn', 'ogrn',
#        'head_or_branch', 'okopf_code', 'okopf', 'okfs_code', 'okfs',
#        'is_active', 'id_child'],
df = pd.read_csv(r"F:\DATASETS\lct2024\datasets\База по промышленным образцам (1).csv")
df[['head_or_branch','id_child', 'inn', 'is_active', 'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code']] = np.nan
print(df.columns)
print(df.info()) #90193 | patent holders-90146 | patent holders in latin-9125 | authors 87586 | authors in latin 4801

counter = 0
patent_numbers = df['registration number'].to_numpy()
for number in tqdm(patent_numbers):
    patent_holder = df[df['registration number'].eq(number)]['patent holders'].values[0]
    patent_holder_l = df[df['registration number'].eq(number)]['patent holders in latin'].values[0]
    print(patent_holder, patent_holder_l)
    if patent_holder != np.nan:
        find1 = orgs[orgs.full_name.eq(patent_holder.split(' (')[0])]
        if not find1.empty and len(find1)==1:
            print('found1')
            df.loc[df['registration number'].eq(number), 'head_or_branch'] = find1.head_or_branch.values[0]
            df.loc[df['registration number'].eq(number), 'id_child'] = find1.id_child.values[0]
            df.loc[df['registration number'].eq(number), 'inn'] = find1.inn.values[0]
            df.loc[df['registration number'].eq(number), 'is_active'] = find1.is_active.values[0]
            df.loc[df['registration number'].eq(number), 'ogrn'] = find1.ogrn.values[0]
            df.loc[df['registration number'].eq(number), 'okfs'] = find1.okfs.values[0]
            df.loc[df['registration number'].eq(number), 'okfs_code'] = find1.okfs_code.values[0]
            df.loc[df['registration number'].eq(number), 'okopf'] = find1.okopf.values[0]
            df.loc[df['registration number'].eq(number), 'okopf_code'] = find1.okopf_code.values[0]
            counter +=1



print(counter)
df.to_csv(r"F:\DATASETS\lct2024\datasets\База по промышленным образцам_marked.csv", index=False)