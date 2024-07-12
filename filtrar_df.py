#%%
import pandas as pd

#%%
# Leer los datos de los archivos Excel
deis_a = pd.read_excel('DATA/Establecimientos DEIS MINSAL 02-07-2024.xlsx', skiprows=1, sheet_name='BASE_ESTABLECIMIENTO_2024-07-02')
deis_c = pd.read_excel('DATA/Establecimientos DEIS MINSAL 02-07-2024.xlsx', skiprows=1, sheet_name='Establecimientos Cerrados')

#%%
# Concatenar los DataFrames
deis = pd.concat([deis_a, deis_c])
deis_dd_antiguo = deis.drop_duplicates(subset=['Código Antiguo '])
deis_dd_antiguo = deis.dropna(subset=['Código Antiguo '])
dict_codigo_antiguo = pd.Series(deis_dd_antiguo['Código Región'].values, index=deis_dd_antiguo['Código Antiguo ']).to_dict()
print(dict_codigo_antiguo)
#%%
# Leer el archivo CSV
df_2024 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DATA - Atenciones de Urgencias\AtencionesUrgencia2024.csv', sep=';', encoding='LATIN')
df_2023 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DATA - Atenciones de Urgencias\AtencionesUrgencia2023.csv', sep=';', encoding='LATIN')
df_2022 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DATA - Atenciones de Urgencias\AtencionesUrgencia2022.csv', sep=';', encoding='LATIN')
df_2021 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DATA - Atenciones de Urgencias\AtencionesUrgencia2021.csv', sep=';', encoding='LATIN')
df_2020 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DATA - Atenciones de Urgencias\AtencionesUrgencia2020.csv', sep=';', encoding='LATIN')
df_2019 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DATA - Atenciones de Urgencias\AtencionesUrgencia2019.csv', sep=';', encoding='LATIN')
df_2018 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DATA - Atenciones de Urgencias\AtencionesUrgencia2018.csv', sep=';', encoding='LATIN')
#%%
diccionario_causas = {
    # Trastornos mentales y comportamentales
    # 'Trastornos neuróticos, trastornos relacionados con el estrés y trastornos somatomorfos (F40-F48) Incluído el trastorno de pánico (F41.0)': 40,
    # 'Trastornos del Humor (Afectivos) (F30-F39)': 39,
    # 'TOTAL CAUSAS DE TRASTORNOS MENTALES (F00-F99)': 36,
    # 'Ideación Suicida (R45.8)': 37,
    # 'Trastornos mentales y del comportamiento debidos al uso de sustancias psicoactivas (F10-F19)': 38,
    # 'Otros trastornos mentales no contenidos en las categorías anteriores': 41,
    # '- CAUSAS POR TRASTORNOS MENTALES (F00-F99)': 42,
    # Sistema circulatorio
    # 'TOTAL CAUSAS SISTEMA CIRCULATORIO': 12,
    # 'Infarto agudo miocardio': 13,
    # 'Accidente vascular encefálico': 14,
    # 'Crisis hipertensiva': 15,
    # 'Arritmia grave': 16,
    # 'Otras causas circulatorias': 17,
    # '-CAUSAS SISTEMA CIRCULATORIO': 22,
    # Sistema respiratorio
    'TOTAL CAUSAS SISTEMA RESPIRATORIO': 2,
    '- COVID-19, VIRUS IDENTIFICADO U07.1': 32,
    'Otra causa respiratoria (J22, J30-J39, J47, J60-J98)': 6,
    '- COVID-19, VIRUS NO IDENTIFICADO U07.2': 33,
    'Neumonía (J12-J18)': 5,
    'Influenza (J09-J11)': 4,
    'CAUSAS SISTEMA RESPIRATORIO': 7,
    'IRA Alta (J00-J06)': 10,
    'Bronquitis/bronquiolitis aguda (J20-J21)': 3,
    'Crisis obstructiva bronquial (J40-J46)': 11,
    # Traumatismos y envenenamientos
    # 'TOTAL TRAUMATISMOS Y ENVENENAMIENTO': 18,
    # 'Lesiones autoinfligidas intencionalmente (X60-X84)': 35,
    # 'Accidentes del tránsito': 19,
    # '- TRAUMATISMOS Y ENVENENAMIENTOS': 23,
    # Otras causas
    # 'TOTAL DEMÁS CAUSAS': 21,
    # 'Otras causas externas': 20,
    # '- LAS DEMÁS CAUSAS': 8,
    # 'DIARREA AGUDA (A00-A09)': 29,
    # 'CIRUGÍAS DE URGENCIA': 24,
    # 'TOTAL DEMANDA': 34,
    'SECCIÓN 2. TOTAL DE HOSPITALIZACIONES': 25,
    # 'Pacientes en espera de hospitalización que esperan menos de 12 horas para ser trasladados a cama hospitalaria': 28,
    # 'Pacientes en espera de hospitalización': 27,
    'SECCIÓN 1. TOTAL ATENCIONES DE URGENCIA': 1,
    'Covid-19, Virus no identificado U07.2': 31,
    'Covid-19, Virus identificado U07.1': 30,
}

diccionario_causas_au={
    1   :'Atenciones de urgencia - Total',
    2   :'Atenciones de urgencia - Total Respiratorios',
    31  :'Atenciones de urgencia - Covid-19, No Identificado (U07.2)',
    30  :'Atenciones de urgencia - Covid-19, Identificado (U07.1)',
    6   :'Atenciones de urgencia - Otra causa respiratoria (J22, J30-J39, J47, J60-J98)',
    5   :'Atenciones de urgencia - Neumonía (J12-J18)',
    4   :'Atenciones de urgencia - Influenza (J09-J11)',
    10  :'Atenciones de urgencia - IRA Alta (J00-J06)',
    3   :'Atenciones de urgencia - Bronquitis/bronquiolitis aguda (J20-J21)',
    11  :'Atenciones de urgencia - Crisis obstructiva bronquial (J40-J46)',
    25  :'Hospitalizaciones - Total',
    7   :'Hospitalizaciones - Sistema Respiratorio',
    33  :'Hospitalizaciones - Covid-19 No Identificado (U7.2)',
    32  :'Hospitalizaciones - Covid-19 Identificado (U7.1)',
}
diccionario_causas_categorizada_au={
    1   :'Atenciones de urgencia - Total',
    2   :'Atenciones de urgencia - Total Respiratorios',
    31  :'Atenciones de urgencia - Covid-19',
    30  :'Atenciones de urgencia - Covid-19',
    6   :'Atenciones de urgencia - Otra causa respiratoria (J22, J30-J39, J47, J60-J98)',
    5   :'Atenciones de urgencia - IRAs Bajas',
    4   :'Atenciones de urgencia - Influenza (J09-J11)',
    10  :'Atenciones de urgencia - IRA Alta (J00-J06)',
    3   :'Atenciones de urgencia - IRAs Bajas',
    11  :'Atenciones de urgencia - IRAs Bajas',
    25  :'Hospitalizaciones - Total',
    7   :'Hospitalizaciones - Sistema Respiratorio',
    33  :'Hospitalizaciones - Covid-19',
    32  :'Hospitalizaciones - Covid-19',
}
#%%
# Filtrar datos para la Región Metropolitana de Santiago
# 2024
def filter_rm_resp(df):
    try:
        df_rm = df.loc[df.CodigoRegion == 13]
    except:
        df['CodigoRegion']=df.IdEstablecimiento.map(dict_codigo_antiguo)
        df_rm = df.loc[df.CodigoRegion == 13]
    df_rm_resp = df_rm.loc[df_rm.IdCausa.isin(diccionario_causas_au.keys())]
    df_rm_resp['Causa'] = df_rm_resp.IdCausa.map(diccionario_causas_au)
    df_rm_resp['Causa_category'] = df_rm_resp.IdCausa.map(diccionario_causas_categorizada_au)
    df_rm_resp=df_rm_resp.groupby(by=['GLOSATIPOESTABLECIMIENTO','semana','IdCausa','Causa'])[columnas].sum().reset_index()
    return df_rm_resp

# %%
df_2024_rm_resp=filter_rm_resp(df_2024)
df_2023_rm_resp=filter_rm_resp(df_2023)
df_2022_rm_resp=filter_rm_resp(df_2022)
df_2021_rm_resp=filter_rm_resp(df_2021)
df_2020_rm_resp=filter_rm_resp(df_2020)
df_2019_rm_resp=filter_rm_resp(df_2019)
df_2018_rm_resp=filter_rm_resp(df_2018)
#%%
columnas=['Total', 'Menores_1', 'De_1_a_4', 'De_5_a_14', 'De_15_a_64','De_65_y_mas']

#%%
df_2024_rm_resp.to_csv('DATA/df_2024_rm_resp.csv')
df_2023_rm_resp.to_csv('DATA/df_2023_rm_resp.csv')
df_2022_rm_resp.to_csv('DATA/df_2022_rm_resp.csv')
df_2021_rm_resp.to_csv('DATA/df_2021_rm_resp.csv')
df_2020_rm_resp.to_csv('DATA/df_2020_rm_resp.csv')
df_2019_rm_resp.to_csv('DATA/df_2019_rm_resp.csv')
df_2018_rm_resp.to_csv('DATA/df_2018_rm_resp.csv')
# %%
