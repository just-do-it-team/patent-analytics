import pandas as pd
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from multiprocessing import Pool
from tqdm import tqdm
import re

df_orgs = pd.read_csv(r"F:\DATASETS\lct2024\datasets\DatasetOrg_short.csv", delimiter=';')
df_bd = pd.read_csv(r"F:\DATASETS\lct2024\datasets\resultInvention2.csv")
# df_bd[['individual']] = np.nan
# print(df['patent holders'].nunique())
# x = round(df['patent holders'].unique().shape[0]/6)
# print(df['patent holders'].unique()[x*0:x*1])

# def markit(orgs, df):
#     print('hi')
#     counter = 0
#     for holder in tqdm(df[df['head_or_branch'].isna()]['patent holders'].unique()): # [slice_start:slice_end]:
#         if holder!=np.nan:
#             find1 = orgs[orgs.full_name.str.contains(str(holder).split(" (")[0], na=False)]
#             # find1 = orgs[orgs.full_name.eq(str(holder).split(' (')[0])]
#             if not find1.empty and len(find1) == 1:
#                 print("+1")
#                 counter +=1
#                 df.loc[df['patent holders'].eq(holder), 'head_or_branch'] = find1.head_or_branch.values[0]
#                 df.loc[df['patent holders'].eq(holder), 'id_child'] = find1.id_child.values[0]
#                 df.loc[df['patent holders'].eq(holder), 'inn'] = find1.inn.values[0]
#                 df.loc[df['patent holders'].eq(holder), 'is_active'] = find1.is_active.values[0]
#                 df.loc[df['patent holders'].eq(holder), 'ogrn'] = find1.ogrn.values[0]
#                 df.loc[df['patent holders'].eq(holder), 'okfs'] = find1.okfs.values[0]
#                 df.loc[df['patent holders'].eq(holder), 'okfs_code'] = find1.okfs_code.values[0]
#                 df.loc[df['patent holders'].eq(holder), 'okopf'] = find1.okopf.values[0]
#                 df.loc[df['patent holders'].eq(holder), 'okopf_code'] = find1.okopf_code.values[0]
#                 if counter %10==0:
#                     print(10)
#                     df.to_csv(f"F:/DATASETS/lct2024/datasets/resultInvention2.csv", index=False)
#     return df
# markit(df_orgs, df_bd).to_csv(f"F:/DATASETS/lct2024/datasets/resultInvention2.csv", index=False)

# def run_parallel():
#     num_workers = 4
#     x = round(df_bd['patent holders'].nunique()/num_workers)
#     with ProcessPoolExecutor(max_workers=num_workers) as executor:
#         for i in range(num_workers):
#             executor.submit(markit)


# if __name__ == '__main__':
#     df_orgs = pd.read_csv(r"F:\DATASETS\lct2024\datasets\DatasetOrg_short.csv", delimiter=';')
#     df_bd = pd.read_csv(r"F:\DATASETS\lct2024\datasets\База по промышленным образцам (1).csv")
#     df_result = pd.DataFrame(columns=['head_or_branch', 'id_child', 'inn', 'is_active', 'ogrn', 'okfs', 'okfs_code', 'okopf', 'okopf_code'])
#     num_workers = 2
#     x = round(df_bd['patent holders'].nunique() / num_workers)
#     with Pool(num_workers) as pool:
#         for i in range(num_workers):
#             for r in pool.map(markit, [df_orgs, df_bd, x*i, x*(i+1)]):
#                 df_result = pd.concat([df_result, r], ignore_index=True)
#     df_result.to_csv(f"F:/DATASETS/lct2024/datasets/marked/result.csv", index=False)
#     # run_parallel()

def markit2(orgs, df):
    id = 0
    counter = 0
    df2 = df[df['head_or_branch'].isna() | df['individual'].isna()].groupby('patent holders')['patent holders'].count().sort_values(ascending=False).reset_index(name='123')  ##['patent holders'].values
    for i, r in tqdm(df2[3531:7500].iterrows()):
        holder = str(r['patent holders']).split(" (")[0]
        print(holder)
        find1 = orgs[orgs.full_name.str.contains(str(r['patent holders']).split(" (")[0], na=False)]
        if not find1.empty and (len(find1) == 1 or (all(x == find1['inn'].values[0] for x in find1['inn'].values[:2]))):
            print("+1")
            # print(find1)
            counter +=1
            df.loc[df['patent holders'].eq(holder), 'head_or_branch'] = find1.head_or_branch.values[0]
            df.loc[df['patent holders'].eq(holder), 'id_child'] = find1.id_child.values[0]
            df.loc[df['patent holders'].eq(holder), 'inn'] = find1.inn.values[0]
            df.loc[df['patent holders'].eq(holder), 'is_active'] = find1.is_active.values[0]
            df.loc[df['patent holders'].eq(holder), 'ogrn'] = find1.ogrn.values[0]
            df.loc[df['patent holders'].eq(holder), 'okfs'] = find1.okfs.values[0]
            df.loc[df['patent holders'].eq(holder), 'okfs_code'] = find1.okfs_code.values[0]
            df.loc[df['patent holders'].eq(holder), 'okopf'] = find1.okopf.values[0]
            df.loc[df['patent holders'].eq(holder), 'okopf_code'] = find1.okopf_code.values[0]
            if counter %10==0:
                print('saved')
                df.to_csv(f"F:/DATASETS/lct2024/datasets/resultInvention2.csv", index=False)
        elif find1.empty and len(holder.split(' '))==3 and re.search(r'(?:^|\s)([а-яА-ЯёЁ]+(?:-[а-яА-ЯёЁ]+)?\s[а-яА-ЯёЁ]+\s[а-яА-ЯёЁ]+(?:ович|евич|ич|овна|евна|ична|иничнa))', holder) is not None:
            print('+id')
            counter+=1
            df.loc[df['patent holders'].eq(holder), 'individual'] = str(id)
            id+=1
            if counter %10==0:
                print('saved')
                df.to_csv(f"F:/DATASETS/lct2024/datasets/resultInvention2.csv", index=False)
    return df

markit2(df_orgs, df_bd).to_csv(f"F:/DATASETS/lct2024/datasets/resultInvention2.csv", index=False)