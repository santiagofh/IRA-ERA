#%%
import pandas as pd
df = pd.read_csv(f'data/df_2024_rm_resp.csv')
# %%
df_au=df.loc[df.IdCausa==1]
# %%
df_au_aps=df_au.loc[df_au.GLOSATIPOESTABLECIMIENTO!='Hospital']
# %%
df_au_sapu=df_au.loc[df_au.GLOSATIPOESTABLECIMIENTO=='SAPU']
# %%
