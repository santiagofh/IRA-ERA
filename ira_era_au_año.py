#%%
# Importar librerías
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from io import BytesIO

GLOBAL_THEME='seaborn'

# Crear una función para cargar datos según el año seleccionado
def load_data(start_year, end_year):
    dataframes = []
    for year in range(start_year, end_year + 1):
        try:
            df = pd.read_csv(f'data/df_{year}_rm_resp.csv')
            df['año'] = year  # Agregar columna de año
            dataframes.append(df)
        except FileNotFoundError:
            st.error(f'Archivo para el año {year} no encontrado.')
    if dataframes:
        return dataframes
    else:
        return None

# Configuración de la aplicación Streamlit
logo_horizontal = 'img/horizontal_SEREMIRM_blue.png'
logo_icono = 'img/icon_SEREMIRM.png'
st.logo(logo_horizontal, icon_image=logo_icono)

# Selector de intervalo de años
year_range = st.sidebar.slider('Seleccione el intervalo de años', 2018, 2024, 2025 (2018, 2023))
hospital = st.sidebar.selectbox('Seleccione si desea ver la información de APS o Hospital',['APS','Hospitales'],index=0)
# Cargar datos según el intervalo de años seleccionado
start_year, end_year = year_range
list_df_rm = load_data(start_year, end_year)
df_rm = pd.concat(list_df_rm)
if df_rm is None:
    st.stop()

# Resto del código para procesar y visualizar los datos
# Diccionario de mapeo de IdCausa a glosa_causa
diccionario_causas_au = {
    1: 'Atenciones de urgencia - Total',
    2: 'Atenciones de urgencia - Total Respiratorios',
    31: 'Atenciones de urgencia - Covid-19, No Identificado (U07.2)',
    30: 'Atenciones de urgencia - Covid-19, Identificado (U07.1)',
    6: 'Atenciones de urgencia - Otra causa respiratoria (J22, J30-J39, J47, J60-J98)',
    5: 'Atenciones de urgencia - Neumonía (J12-J18)',
    4: 'Atenciones de urgencia - Influenza (J09-J11)',
    10: 'Atenciones de urgencia - IRA Alta (J00-J06)',
    3: 'Atenciones de urgencia - Bronquitis/bronquiolitis aguda (J20-J21)',
    11: 'Atenciones de urgencia - Crisis obstructiva bronquial (J40-J46)',
    25: 'Hospitalizaciones - Total',
    7: 'Hospitalizaciones - Sistema Respiratorio',
    33: 'Hospitalizaciones - COVID-19 No Identificado (U7.2)',
    32: 'Hospitalizaciones - COVID-19 Identificado (U7.1)',
}

# Listas de causas
irab = [
    'Atenciones de urgencia - Neumonía (J12-J18)',
    'Atenciones de urgencia - Bronquitis/bronquiolitis aguda (J20-J21)',
    'Atenciones de urgencia - Crisis obstructiva bronquial (J40-J46)'
]
iraa = ['Atenciones de urgencia - IRA Alta (J00-J06)']
covid = [
    'Atenciones de urgencia - Covid-19, No Identificado (U07.2)',
    'Atenciones de urgencia - Covid-19, Identificado (U07.1)'
]
total_au = ['Atenciones de urgencia - Total']
total_resp = ['Atenciones de urgencia - Total Respiratorios']
influ = ['Atenciones de urgencia - Influenza (J09-J11)']
otras = ['Atenciones de urgencia - Otra causa respiratoria (J22, J30-J39, J47, J60-J98)']

# Filtrar dataframes para APS y hospitales
if hospital == 'Hospitales':
    df_rm = df_rm.loc[(df_rm.GLOSATIPOESTABLECIMIENTO == 'Hospital')]
else:
    df_rm = df_rm.loc[~(df_rm.GLOSATIPOESTABLECIMIENTO == 'Hospital')]

# Función para mostrar y ocultar el DataFrame y permitir la descarga
def mostrar_dataframe(df, nombre):
    # Botón para mostrar u ocultar el DataFrame
    if st.button(f'Mostrar/Ocultar datos {nombre}'):
        if 'mostrar_df' not in st.session_state:
            st.session_state.mostrar_df = True
        else:
            st.session_state.mostrar_df = not st.session_state.mostrar_df

    # Mostrar DataFrame y botón de descarga si se activa la opción
    if 'mostrar_df' in st.session_state and st.session_state.mostrar_df:
        st.write(df)
        
        # Convertir DataFrame a un archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name=nombre)
            writer.close()
            processed_data = output.getvalue()
        
        st.download_button(
            label=f"Descargar {nombre} como Excel",
            data=processed_data,
            file_name=f'{nombre}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

def grafico_area_atenciones_urgencia_semanal_por_año(df, col, title):
    fig = go.Figure()
    df = df.loc[df.Causa.isin(covid + total_resp)]
    df = df.loc[~(df.semana == 53)]
    # Agrupar los datos por año y semana, y sumar las atenciones
    dataframes = []
    for year in df['año'].unique():
        df_year = df[df['año'] == year].groupby('semana')[col].sum().reset_index()
        df_year[col].replace(0, np.nan, inplace=True)
        df_year['año'] = year
        dataframes.append(df_year)
        
        # Añadir trazas para cada año
        fig.add_trace(go.Scatter(
            x=df_year['semana'], y=df_year[col], 
            mode='lines', name=str(year)
        ))

    # Concatenar los DataFrames
    df_concatenado = pd.concat(dataframes, ignore_index=True)

    # Configuración del diseño del gráfico
    fig.update_layout(
        title=title,
        xaxis_title='Semana',
        yaxis_title='N° de Atenciones',
        legend_title='Año',
        template=GLOBAL_THEME,
        yaxis=dict(tickformat='.0f', tickprefix='', ticksuffix='')
    )
    
    return fig, df_concatenado

def grafico_barras_atenciones_por_año(df, col, title):
    fig = go.Figure()
    df = df.loc[df.Causa.isin(covid + total_resp)]

    # Agrupar los datos por año y sumar las atenciones
    df_year = df.groupby('año')[col].sum().reset_index()

    # Definir colores para las barras
    colors = ['lightblue' if año in [2020, 2021] else 'steelblue' for año in df_year['año']]

    # Crear la figura del gráfico de barras horizontales
    fig.add_trace(go.Bar(
        x=df_year[col], 
        y=df_year['año'], 
        orientation='h', 
        text=[f'{val:,.0f}'.replace(',', '.') for val in df_year[col]],  # Formatear valores de text
        textposition='outside',
        marker_color=colors  # Aplicar los colores a las barras
    ))
    
    # Configuración del diseño del gráfico
    fig.update_layout(
        title=title,
        xaxis_title='N° de Atenciones',
        yaxis_title='Año',
        legend_title='Año',
        template=GLOBAL_THEME,
        xaxis=dict(
            tickformat='.0f',  # Esto formatea los ticks sin decimales
            separatethousands=True,  # Separa los miles
        )
    )
    
    return fig, df_year

#%%
st.header(f'Atenciones de urgencia por causas respiratorias y por COVID por años en {hospital}, RM')
# Ejemplo de uso
fig, df_area_total = grafico_area_atenciones_urgencia_semanal_por_año(df_rm, 'Total', 'Todas las edades')
fig_menor1, df_area_menor1 = grafico_area_atenciones_urgencia_semanal_por_año(df_rm, 'Menores_1', 'Menores de 1 año')
fig_mayor65, df_area_mayor65 = grafico_area_atenciones_urgencia_semanal_por_año(df_rm, 'De_65_y_mas', '65 años y más')

st.plotly_chart(fig)
st.plotly_chart(fig_menor1)
st.plotly_chart(fig_mayor65)

# %%
fig_bar_total, df_bar_total = grafico_barras_atenciones_por_año(df_rm, 'Total', 'Todas las edades')
fig_bar_menor1, df_bar_menor1 = grafico_barras_atenciones_por_año(df_rm, 'Menores_1', 'Menores de 1 año')
fig_bar_mayor65, df_bar_mayor65 = grafico_barras_atenciones_por_año(df_rm, 'De_65_y_mas', '65 años y más')

st.plotly_chart(fig_bar_total)
st.plotly_chart(fig_bar_menor1)
st.plotly_chart(fig_bar_mayor65)


#%%
import pandas as pd
from io import BytesIO
def reorganizar_dataframe_por_año(df,col):
    """
    Reorganiza el DataFrame para que cada columna corresponda a un año con sus totales por semana.
    """
    df_pivot = df.pivot(index='semana', columns='año', values=col)
    df_pivot.columns = [f'{col}' for col in df_pivot.columns]
    df_pivot.reset_index(inplace=True)
    return df_pivot

# Función para descargar todos los DataFrames en un solo archivo Excel
def descargar_todos_los_dfs():
    # Crear un objeto BytesIO para guardar el archivo Excel en memoria
    output = BytesIO()

    # Crear un objeto ExcelWriter con pandas y xlsxwriter
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Guardar cada DataFrame en una pestaña separada
        reorganizar_dataframe_por_año(df_area_total,'Total').to_excel(writer, index=False, sheet_name='Todas las Edades - Área')
        reorganizar_dataframe_por_año(df_area_menor1,'Menores_1').to_excel(writer, index=False, sheet_name='Menores de 1 Año - Área')
        reorganizar_dataframe_por_año(df_area_mayor65,'De_65_y_mas').to_excel(writer, index=False, sheet_name='Mayores de 65 Años - Área')
        df_bar_total.to_excel(writer, index=False, sheet_name='Todas las Edades - Barras')
        df_bar_menor1.to_excel(writer, index=False, sheet_name='Menores de 1 Año - Barras')
        df_bar_mayor65.to_excel(writer, index=False, sheet_name='Mayores de 65 Años - Barras')
        
        # Asegurarse de que el archivo se haya escrito completamente en el objeto BytesIO
        writer.close()
        processed_data = output.getvalue()

    # Descargar el archivo Excel
    st.download_button(
        label="Descargar todos los datos como Excel",
        data=processed_data,
        file_name=f'Atenciones_Urgencia_Respiratoria_{start_year}_{end_year}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Llamar a la función para generar el botón de descarga
descargar_todos_los_dfs()
