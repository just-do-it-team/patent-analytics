import pandas as pd
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from multiprocessing import Pool
from tqdm import tqdm
import re
import nltk
from nltk.corpus import stopwords
from string import punctuation
russian_stopwords = stopwords.words("russian")
pd.set_option('display.max_columns', None)

df_orgs = pd.read_csv("F:/DATASETS/lct2024/datasets/DatasetOrg_short2.csv", delimiter=';')
# print(df_orgs)
df_bd = pd.read_csv("F:/DATASETS/lct2024/datasets/resultInvention3.csv")
# df_bd[['individual']] = np.nan
# df2 = df_bd[df_bd['head_or_branch'].isna() | df_bd['individual'].isna()].groupby('patent holders').count().reset_index().sort_values(by=['registration number'], ascending=False)
# print(df2)


def markit2(orgs, df):
    id = 0
    counter = 0
    df2 = df[~(df['head_or_branch'].notna() | df['individual'].notna())].groupby('patent holders')['patent holders'].count().sort_values(ascending=False).reset_index(name='123')
    print(df2[90:5000])
    for i, r in tqdm(df2[1000:5000].iterrows()):
        holder = str(r['patent holders']).split(" (")[0]
        print(holder)
        find1 = orgs[orgs.full_name.str.contains(str(r['patent holders']).split(" (")[0], na=False)]
        if not find1.empty and (len(find1) == 1 or (all(x == find1['inn'].values[0] for x in find1['inn'].values[:2]))):
            print("+1")
            counter +=1
            df.loc[df['patent holders'].str.contains(holder, na=False), 'head_or_branch'] = find1.head_or_branch.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'id_child'] = find1.id_child.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'inn'] = find1.inn.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'is_active'] = find1.is_active.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'ogrn'] = find1.ogrn.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'okfs'] = find1.okfs.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'okfs_code'] = find1.okfs_code.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'okopf'] = find1.okopf.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'okopf_code'] = find1.okopf_code.values[0]
            if counter %10==0:
                print('saved')
                df.to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)
        elif len(find1) > 1:
            for org_address in find1.yr_address.dropna().unique():
                for holder_address in df[df['patent holders'].str.contains(holder, na=False)]['correspondence address'].dropna().unique():
                    if match_bows(string_to_bow(org_address), string_to_bow(holder_address)) >0.65:
                        counter += 1
                        df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'head_or_branch'] = find1.head_or_branch.values[0]
                        df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'id_child'] = find1.id_child.values[0]
                        df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'inn'] = find1.inn.values[0]
                        df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'is_active'] = find1.is_active.values[0]
                        df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'ogrn'] = find1.ogrn.values[0]
                        df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'okfs'] = find1.okfs.values[0]
                        df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'okfs_code'] = find1.okfs_code.values[0]
                        df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'okopf'] = find1.okopf.values[0]
                        df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'okopf_code'] = find1.okopf_code.values[0]
                        print("+1corr")
                        if counter % 10 == 0:
                            print('saved')
                            df.to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)
        elif find1.empty and len(holder.split(' '))==3 and re.search(r'(?:^|\s)([а-яА-ЯёЁ]+(?:-[а-яА-ЯёЁ]+)?\s[а-яА-ЯёЁ]+\s[а-яА-ЯёЁ]+(?:ович|евич|ич|овна|евна|ична|иничнa))', holder) is not None:
            print('+id')
            counter+=1
            df.loc[df['patent holders'].str.contains(holder, na=False), 'individual'] = str(id) + ' ' + holder
            id+=1
            if counter %10==0:
                print('saved')
                df.to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)
        elif find1.empty:
            find3 = orgs[orgs.full_name.str.contains(str(r['patent holders']).split(" (")[0], na=False)]
            if not find3.empty and (
                    len(find3) == 1 or (all(x == find3['inn'].values[0] for x in find3['inn'].values[:2]))):
                print("+1")
                counter += 1
                df.loc[df['patent holders'].str.contains(holder, na=False), 'head_or_branch'] = find3.head_or_branch.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'id_child'] = find3.id_child.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'inn'] = find3.inn.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'is_active'] = find3.is_active.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'ogrn'] = find3.ogrn.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'okfs'] = find3.okfs.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'okfs_code'] = find3.okfs_code.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'okopf'] = find3.okopf.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'okopf_code'] = find3.okopf_code.values[0]
                if counter % 10 == 0:
                    print('saved')
                    df.to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)
            elif len(find3) > 1:
                for org_address in find3.yr_address.dropna().unique():
                    for holder_address in df[df['patent holders'].str.contains(holder, na=False)]['correspondence address'].dropna().unique():
                        if match_bows(string_to_bow(org_address), string_to_bow(holder_address)) > 0.65:
                            counter += 1
                            df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
                                holder_address), 'head_or_branch'] = find3.head_or_branch.values[0]
                            df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
                                holder_address), 'id_child'] = find3.id_child.values[0]
                            df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
                                holder_address), 'inn'] = find3.inn.values[0]
                            df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
                                holder_address), 'is_active'] = find3.is_active.values[0]
                            df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
                                holder_address), 'ogrn'] = find3.ogrn.values[0]
                            df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
                                holder_address), 'okfs'] = find3.okfs.values[0]
                            df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
                                holder_address), 'okfs_code'] = find3.okfs_code.values[0]
                            df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
                                holder_address), 'okopf'] = find3.okopf.values[0]
                            df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
                                holder_address), 'okopf_code'] = find3.okopf_code.values[0]
                            print("+1c")
                            if counter % 10 == 0:
                                print('saved')
                                df.to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)
    return df


def string_to_bow(s):
    if s==np.nan:
        return ['']
    tokens = nltk.word_tokenize(s.lower())[1:]
    tokens = [token for token in tokens if token not in russian_stopwords and token not in punctuation]
    for i in tokens:
        if i == '``' or i == "''" or i == 'г.':
            tokens.remove(i)
    if tokens[0].isdigit():
        return tokens[1:]
    else:
        return tokens


def match_bows(l1, l2):
    p = round(len(set(l1) & set(l2))/max(len(l1),len(l2)),2)
    return p

markit2(df_orgs, df_bd).to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)