#%% Importaciones y lectura de datos de establecimientos
import pandas as pd
from epiweeks import Week

# Leer datos de establecimientos
deis_a = pd.read_excel('DATA/Establecimientos DEIS MINSAL 02-07-2024.xlsx',
                         skiprows=1,
                         sheet_name='BASE_ESTABLECIMIENTO_2024-07-02')
deis_c = pd.read_excel('DATA/Establecimientos DEIS MINSAL 02-07-2024.xlsx',
                         skiprows=1,
                         sheet_name='Establecimientos Cerrados')

deis = pd.concat([deis_a, deis_c])
deis_dd_antiguo = deis.drop_duplicates(subset=['Código Antiguo '])
deis_dd_antiguo = deis_dd_antiguo.dropna(subset=['Código Antiguo '])
dict_codigo_antiguo = pd.Series(deis_dd_antiguo['Código Región'].values,
                                index=deis_dd_antiguo['Código Antiguo ']).to_dict()
print(dict_codigo_antiguo)

#%% Lectura de archivos CSV de Atenciones de Urgencia
df_2025 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\DATA\ATENCIONES_URGENCIA\au_2025\AtencionesUrgencia2025.csv', 
                      sep=';', encoding='LATIN')
df_2024 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\DATA\ATENCIONES_URGENCIA\au_2024\AtencionesUrgencia2024.csv', 
                      sep=';', encoding='LATIN')
df_2023 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\DATA\ATENCIONES_URGENCIA\au_2023\AtencionesUrgencia2023.csv', 
                      sep=';', encoding='LATIN')
df_2022 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\DATA\ATENCIONES_URGENCIA\au_2022\AtencionesUrgencia2022.csv', 
                      sep=';', encoding='LATIN')
df_2021 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\DATA\ATENCIONES_URGENCIA\au_2021\AtencionesUrgencia2021.csv', 
                      sep=';', encoding='LATIN')
df_2020 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DATA - Atenciones de Urgencias\AtencionesUrgencia2020.csv', 
                      sep=';', encoding='LATIN')
df_2019 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DATA - Atenciones de Urgencias\AtencionesUrgencia2019.csv', 
                      sep=';', encoding='LATIN')
df_2018 = pd.read_csv(r'C:\Users\fariass\OneDrive - SUBSECRETARIA DE SALUD PUBLICA\Escritorio\GIE\DATA - Atenciones de Urgencias\AtencionesUrgencia2018.csv', 
                      sep=';', encoding='LATIN')
#%%
ls_rm=[13.0,'13',13.,13]

df_2023=df_2023.loc[df_2023.CodigoRegion.isin(ls_rm)]
df_2024=df_2024.loc[df_2024.CodigoRegion.isin(ls_rm)]
df_2025=df_2025.loc[df_2025.CodigoRegion.isin(ls_rm)]
# Concatenar todos los DataFrames
df = pd.concat([df_2025, df_2024, df_2023])
#%%
del df_2025
del df_2024
del df_2023
del df_2022
del df_2021
del df_2020
del df_2019
del df_2018
#%%
# Convertir la columna 'fecha' a datetime (formato DD/MM/YYYY)
df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)

#%% Calcular la semana epidemiológica y el año epidemiológico
df['semana_epi'] = df['fecha'].apply(lambda x: Week.fromdate(x).week)
df['anio_epi'] = df['fecha'].apply(lambda x: Week.fromdate(x).year)
df['semana_epi_str'] = df['semana_epi'].apply(lambda x: f"{x:02d}") + '-' + df['anio_epi'].astype(str)

#%%
# Crear DataFrames individuales por año epidemiológico
df_2025_epi = df[df['anio_epi'] == 2025].copy()
df_2024_epi = df[df['anio_epi'] == 2024].copy()
df_2023_epi = df[df['anio_epi'] == 2023].copy()
df_2022_epi = df[df['anio_epi'] == 2022].copy()
df_2021_epi = df[df['anio_epi'] == 2021].copy()
df_2020_epi = df[df['anio_epi'] == 2020].copy()
df_2019_epi = df[df['anio_epi'] == 2019].copy()
df_2018_epi = df[df['anio_epi'] == 2018].copy()

#%% Diccionarios de causas
diccionario_causas_au = {
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

diccionario_causas_categorizada_au = {
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

columnas = ['Total', 'Menores_1', 'De_1_a_4', 'De_5_a_14', 'De_15_a_64','De_65_y_mas']

#%% Función para filtrar datos de la Región Metropolitana y agrupar por epiweek
def filter_rm_resp_epi(df_epi):
    # Se asume que la columna "CodigoRegion" existe; si no, se mapea desde IdEstablecimiento
    if 'CodigoRegion' not in df_epi.columns or df_epi['CodigoRegion'].isnull().all():
        df_epi['CodigoRegion'] = df_epi.IdEstablecimiento.map(dict_codigo_antiguo)
    df_rm = df_epi.loc[df_epi.CodigoRegion == 13].copy()
    
    # Filtrar según causas
    df_rm_resp = df_rm.loc[df_rm.IdCausa.isin(diccionario_causas_au.keys())].copy()
    df_rm_resp['Causa'] = df_rm_resp.IdCausa.map(diccionario_causas_au)
    df_rm_resp['Causa_category'] = df_rm_resp.IdCausa.map(diccionario_causas_categorizada_au)
    
    # Agrupar por establecimiento, epiweek, causa, etc.
    df_rm_resp = df_rm_resp.groupby(by=['NombreComuna','semana_epi_str','IdCausa','Causa'])[columnas].sum().reset_index()
    return df_rm_resp

#%% Procesar cada año epidemiológico y exportar Excel por cada epiweek
# Creamos un diccionario con los DataFrames de cada año epidemiológico
dfs_epi = {
    2025: df_2025_epi,
    2024: df_2024_epi,
    2023: df_2023_epi,
    2022: df_2022_epi,
    2021: df_2021_epi,
    2020: df_2020_epi,
    2019: df_2019_epi,
    2018: df_2018_epi
}

#%% Procesar y exportar cada año epidemiológico completo
for anio, df_year in dfs_epi.items():
    # Filtrar datos para Región Metropolitana
    df_rm_resp = filter_rm_resp_epi(df_year)
    # Exportar todo el año epidemiológico en un solo archivo
    filename = f"DATA/AU_EPIYEAR_{anio}.csv"
    df_rm_resp.to_csv(filename, index=False)
    print(f"Año epidemiológico {anio} exportado: {filename}")
# %%
