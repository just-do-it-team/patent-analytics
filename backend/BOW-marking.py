import pandas as pd
import numpy as np
from tqdm import tqdm
import re
import nltk
from nltk.corpus import stopwords
from string import punctuation
russian_stopwords = stopwords.words("russian")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def name_to_bow(s):
    if s==np.nan:
        return ['']
    tokens = nltk.word_tokenize(s.lower())
    tokens = [token for token in tokens if token not in russian_stopwords and token not in punctuation]
    for i in tokens:
        if i == '``' or i == "''":
            tokens.remove(i)
    return tuple(tokens)


df_orgs = pd.read_csv("F:/DATASETS/lct2024/datasets/DatasetOrg_short3.csv", delimiter=';')
df_orgs.full_name = df_orgs.full_name.apply(lambda x: name_to_bow(x) if x is not np.nan else np.nan)
df_bd = pd.read_csv("F:/DATASETS/lct2024/datasets/resultInvention3.csv")
# df2 = df_bd[~(df_bd['head_or_branch'].notna() | df_bd['individual'].notna())].groupby('patent holders')['patent holders'].count().sort_values(ascending=False).reset_index(name='123')
# print(df2[:300])

def markit2(orgs, df):
    id = 0
    counter = 0
    df2 = df[~(df['head_or_branch'].notna() | df['individual'].notna())].groupby('patent holders')['patent holders'].count().sort_values(ascending=False).reset_index(name='123')
    print(df2[55:1500])
    for i, r in tqdm(df2[55:1500].iterrows()):
        holder = str(r['patent holders']).split(" (")[0]
        print(holder)
        holder_bow = name_to_bow(holder)
        find1_list = []
        find2_list = []
        for i in orgs.full_name.dropna().values:
            if match_bows(i, holder_bow) > 0.55:
                find1_list.append(i)
        if len(find1_list) == 1: # or (all(x == find1['inn'].values[0] for x in find1['inn'].values[:2])):
            print("+1")
            counter +=1
            df.loc[df['patent holders'].str.contains(holder, na=False), 'head_or_branch'] = orgs[orgs.full_name == find1_list[0]].head_or_branch.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'id_child'] = orgs[orgs.full_name == find1_list[0]].id_child.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'inn'] = orgs[orgs.full_name == find1_list[0]].inn.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'is_active'] = orgs[orgs.full_name == find1_list[0]].is_active.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'ogrn'] = orgs[orgs.full_name == find1_list[0]].ogrn.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'okfs'] = orgs[orgs.full_name == find1_list[0]].okfs.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'okfs_code'] = orgs[orgs.full_name == find1_list[0]].okfs_code.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'okopf'] = orgs[orgs.full_name == find1_list[0]].okopf.values[0]
            df.loc[df['patent holders'].str.contains(holder, na=False), 'okopf_code'] = orgs[orgs.full_name == find1_list[0]].okopf_code.values[0]
            if counter %10==0:
                print('saved')
                df.to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)
        elif len(find2_list)== 1:
            for i in orgs.short_name.dropna().values:
                if match_bows(i, holder_bow) > 0.55:
                    find2_list.append(i)
            if len(find2_list) == 1:  # or (all(x == find1['inn'].values[0] for x in find1['inn'].values[:2])):
                print("+1")
                counter += 1
                df.loc[df['patent holders'].str.contains(holder, na=False), 'head_or_branch'] = \
                orgs[orgs.full_name == find2_list[0]].head_or_branch.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'id_child'] = \
                orgs[orgs.full_name == find2_list[0]].id_child.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'inn'] = \
                orgs[orgs.full_name == find2_list[0]].inn.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'is_active'] = \
                orgs[orgs.full_name == find2_list[0]].is_active.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'ogrn'] = \
                orgs[orgs.full_name == find2_list[0]].ogrn.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'okfs'] = \
                orgs[orgs.full_name == find2_list[0]].okfs.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'okfs_code'] = \
                orgs[orgs.full_name == find2_list[0]].okfs_code.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'okopf'] = \
                orgs[orgs.full_name == find2_list[0]].okopf.values[0]
                df.loc[df['patent holders'].str.contains(holder, na=False), 'okopf_code'] = \
                orgs[orgs.full_name == find2_list[0]].okopf_code.values[0]
                if counter % 10 == 0:
                    print('saved')
                    df.to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)
        #     for org_address in find1.yr_address.dropna().unique():
        #         for holder_address in df[df['patent holders'].str.contains(holder, na=False)]['correspondence address'].dropna().unique():
        #             if match_bows(string_to_bow(org_address), string_to_bow(holder_address)) >0.65:
        #                 counter += 1
        #                 df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'head_or_branch'] = find1.head_or_branch.values[0]
        #                 df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'id_child'] = find1.id_child.values[0]
        #                 df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'inn'] = find1.inn.values[0]
        #                 df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'is_active'] = find1.is_active.values[0]
        #                 df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'ogrn'] = find1.ogrn.values[0]
        #                 df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'okfs'] = find1.okfs.values[0]
        #                 df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'okfs_code'] = find1.okfs_code.values[0]
        #                 df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'okopf'] = find1.okopf.values[0]
        #                 df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(holder_address), 'okopf_code'] = find1.okopf_code.values[0]
        #                 print("+1corr")
        #                 if counter % 10 == 0:
        #                     print('saved')
        #                     df.to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)
        # elif find1.empty:
        #     find3 = orgs[match_bows(orgs.short_name, holder_bow) > 0.65]
        #     if not find3.empty and (
        #             len(find3) == 1 or (all(x == find3['inn'].values[0] for x in find3['inn'].values[:2]))):
        #         print("+1")
        #         counter += 1
        #         df.loc[df['patent holders'].str.contains(holder, na=False), 'head_or_branch'] = find3.head_or_branch.values[0]
        #         df.loc[df['patent holders'].str.contains(holder, na=False), 'id_child'] = find3.id_child.values[0]
        #         df.loc[df['patent holders'].str.contains(holder, na=False), 'inn'] = find3.inn.values[0]
        #         df.loc[df['patent holders'].str.contains(holder, na=False), 'is_active'] = find3.is_active.values[0]
        #         df.loc[df['patent holders'].str.contains(holder, na=False), 'ogrn'] = find3.ogrn.values[0]
        #         df.loc[df['patent holders'].str.contains(holder, na=False), 'okfs'] = find3.okfs.values[0]
        #         df.loc[df['patent holders'].str.contains(holder, na=False), 'okfs_code'] = find3.okfs_code.values[0]
        #         df.loc[df['patent holders'].str.contains(holder, na=False), 'okopf'] = find3.okopf.values[0]
        #         df.loc[df['patent holders'].str.contains(holder, na=False), 'okopf_code'] = find3.okopf_code.values[0]
        #         if counter % 10 == 0:
        #             print('saved')
        #             df.to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)
        #     elif len(find3) > 1:
        #         for org_address in find3.yr_address.dropna().unique():
        #             for holder_address in df[df['patent holders'].str.contains(holder, na=False)]['correspondence address'].dropna().unique():
        #                 if match_bows(string_to_bow(org_address), string_to_bow(holder_address)) > 0.65:
        #                     counter += 1
        #                     df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
        #                         holder_address), 'head_or_branch'] = find3.head_or_branch.values[0]
        #                     df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
        #                         holder_address), 'id_child'] = find3.id_child.values[0]
        #                     df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
        #                         holder_address), 'inn'] = find3.inn.values[0]
        #                     df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
        #                         holder_address), 'is_active'] = find3.is_active.values[0]
        #                     df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
        #                         holder_address), 'ogrn'] = find3.ogrn.values[0]
        #                     df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
        #                         holder_address), 'okfs'] = find3.okfs.values[0]
        #                     df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
        #                         holder_address), 'okfs_code'] = find3.okfs_code.values[0]
        #                     df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
        #                         holder_address), 'okopf'] = find3.okopf.values[0]
        #                     df.loc[df['patent holders'].str.contains(holder, na=False) & df['correspondence address'].eq(
        #                         holder_address), 'okopf_code'] = find3.okopf_code.values[0]
        #                     print("+1c")
        #                     if counter % 10 == 0:
        #                         print('saved')
        #                         df.to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)
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
        return tuple(tokens)


def match_bows(l1, l2):
    p = round(len(set(l1) & set(l2))/max(len(l1),len(l2)),2)
    return p

markit2(df_orgs, df_bd).to_csv("F:/DATASETS/lct2024/datasets/resultInvention4.csv", index=False)