#%%
# Importar librerías
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

GLOBAL_THEME='seaborn'
# Crear una función para cargar datos según el año seleccionado
def load_data(year):
    try:
        df = pd.read_csv(f'data/df_{year}_rm_resp.csv')
        return df
    except FileNotFoundError:
        st.error(f'Archivo para el año {year} no encontrado.')
        return None

# Configuración de la aplicación Streamlit

logo_horizontal = 'img/horizontal_SEREMIRM_blue.png'
logo_icono = 'img/icon_SEREMIRM.png'
st.logo(logo_horizontal, icon_image=logo_icono)

# Selector de año
selected_year = st.sidebar.selectbox(
    'Seleccione el año',
    options=[2018, 2019, 2020, 2021, 2022, 2023, 2024],
    index=5  # Establecer 2023 como valor predeterminado
)

hospital = st.sidebar.selectbox('Seleccione si desea ver la información de APS o Hospital',['APS','Hospitales'],index=0)
# Titulo

st.title(f'Atenciones de Urgencia en {hospital} - RM 2018-2024')
# Cargar datos según el año seleccionado
df_rm = load_data(selected_year)
if df_rm is None:
    st.stop()

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
#%%
def grafico_area_atenciones_urgencia_semanal(df, col, title):
    fig = go.Figure()

    df_au = df[df['Causa'].isin(total_au)].groupby('semana')[col].sum().reset_index()
    df_resp = df[df['Causa'].isin(total_resp)].groupby('semana')[col].sum().reset_index()
    df_covid = df[df['Causa'].isin(covid)].groupby('semana')[col].sum().reset_index()
    df_influ = df[df['Causa'].isin(influ)].groupby('semana')[col].sum().reset_index()

    # Grupo 1: Atenciones de urgencias
    fig.add_trace(go.Scatter(
        x=df_au['semana'], y=df_au[col], 
        mode='lines', name='Atenciones de urgencias'
    ))

    # Grupo 2: Respiratorios (suma de df_resp y df_covid)
    df_resp_covid = df_resp.copy()
    df_resp_covid[col] += df_covid[col]

    fig.add_trace(go.Scatter(
        x=df_resp_covid['semana'], y=df_resp_covid[col], 
        mode='lines', name='Atenciones respiratorias (incluye Covid)'
    ))

    # Atenciones por Influenza (no acumuladas)
    fig.add_trace(go.Scatter(
        x=df_influ['semana'], y=df_influ[col], 
        mode='lines', name='Atenciones por Influenza'
    ))

    # Atenciones por Covid (individualmente)
    fig.add_trace(go.Scatter(
        x=df_covid['semana'], y=df_covid[col], 
        mode='lines', name='Atenciones por Covid'
    ))

    fig.update_layout(
        title=title,
        xaxis_title='Semana',
        yaxis_title='N° de Atenciones',
        legend_title='Leyenda',
        template=GLOBAL_THEME
    )
    return fig

def grafico_area_atenciones_respiratorias(df, col, title):
    # Filtrar y agrupar los datos
    df_iraa = df[df['Causa'].isin(iraa)].groupby('semana')[col].sum().reset_index()
    df_irab = df[df['Causa'].isin(irab)].groupby('semana')[col].sum().reset_index()
    df_influ = df[df['Causa'].isin(influ)].groupby('semana')[col].sum().reset_index()
    df_covid = df[df['Causa'].isin(covid)].groupby('semana')[col].sum().reset_index()
    df_otras = df[df['Causa'].isin(otras)].groupby('semana')[col].sum().reset_index()

    # Crear la figura del gráfico
    fig = go.Figure()

    # Añadir trazas para cada grupo de causas
    fig.add_trace(go.Scatter(
        x=df_iraa['semana'], y=df_iraa[col], 
        mode='lines', name='IRAS Altas'
    ))
    fig.add_trace(go.Scatter(
        x=df_irab['semana'], y=df_irab[col], 
        mode='lines', name='IRAS Bajas'
    ))
    fig.add_trace(go.Scatter(
        x=df_influ['semana'], y=df_influ[col], 
        mode='lines', name='Influenza'
    ))
    fig.add_trace(go.Scatter(
        x=df_covid['semana'], y=df_covid[col], 
        mode='lines', name='Covid-19'
    ))
    fig.add_trace(go.Scatter(
        x=df_otras['semana'], y=df_otras[col], 
        mode='lines', name='Otras causas respiratorias'
    ))

    # Configuración del diseño del gráfico
    fig.update_layout(
        title=title,
        xaxis_title='Semana',
        yaxis_title='N° Atenciones',
        legend_title='Leyenda',
        template=GLOBAL_THEME
    )

    return fig

def grafico_atenciones_urgencia_pie(df, col, title):
    # Calcular totales por Causa
    total_urgencia = df[df['Causa'].isin(total_au)][col].sum()
    total_respiratorias = df[df['Causa'].isin(total_resp)][col].sum()
    total_covid = df[df['Causa'].isin(covid)][col].sum()
    
    # Calcular las atenciones de urgencia restantes
    total_otras = total_urgencia - (total_respiratorias + total_covid)
    
    # Calcular los porcentajes en relación a total_urgencia
    percentage_respiratorias = (total_respiratorias / total_urgencia) * 100
    percentage_covid = (total_covid / total_urgencia) * 100
    percentage_otras = (total_otras / total_urgencia) * 100

    # Etiquetas y valores para el gráfico de pastel
    labels = [
        'Atenciones de urgencia - Causas respiratorias', 
        'Atenciones de urgencia - Covid-19', 
        'Atenciones de urgencia - Otras causas'
    ]
    values = [percentage_respiratorias, percentage_covid, percentage_otras]
    
    # Crear la figura del gráfico de pastel
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    # Configuración del diseño del gráfico
    fig.update_layout(
        title=title,
        template=GLOBAL_THEME
    )
    
    return fig

def grafico_atenciones_urgencia_barras(df, col, title):
    # Calcular totales por Causa
    total_urgencia = df[df['Causa'].isin(total_au)][col].sum()
    total_respiratorias = df[df['Causa'].isin(total_resp)][col].sum()
    total_covid = df[df['Causa'].isin(covid)][col].sum()
    
    # Etiquetas y valores para el gráfico de barras horizontales
    labels = [
        'Atenciones de urgencia - Total',
        'Atenciones de urgencia - Causas respiratorias', 
        'Atenciones de urgencia - Covid-19', 
    ]
    values = [total_urgencia, total_respiratorias, total_covid]
    
    # Crear la figura del gráfico de barras horizontales
    fig = go.Figure(data=[go.Bar(x=values, y=labels, orientation='h')])
    
    # Configuración del diseño del gráfico
    fig.update_layout(
        title=title,
        xaxis_title='N° Atenciones',
        yaxis_title='Causa',
        legend_title='Causas',
        template=GLOBAL_THEME
    )
    
    return fig
#%%
# Graficos
## Gráfico de Área 1:
fig_area1_total = grafico_area_atenciones_urgencia_semanal(df_rm, 'Total', f'Atenciones de Urgencia - Todas las Edades {selected_year}')
fig_area1_menor1 = grafico_area_atenciones_urgencia_semanal(df_rm, 'Menores_1', f'Atenciones de Urgencia - Menor de 1 Año {selected_year}')
fig_area1_mayor65 = grafico_area_atenciones_urgencia_semanal(df_rm, 'De_65_y_mas', f'Atenciones de Urgencia - 65 años y más {selected_year}')

## Gráfico de Pie 2:
fig2_pie_total = grafico_atenciones_urgencia_pie(df_rm, 'Total', f'Atenciones de Urgencia - Todas las Edades en {hospital}. RM {selected_year}')
fig2_pie_menor1 = grafico_atenciones_urgencia_pie(df_rm, 'Menores_1', f'Atenciones de Urgencia - Menores de 1 Año en {hospital}. RM {selected_year}')
fig2_pie_mayor65 = grafico_atenciones_urgencia_pie(df_rm, 'De_65_y_mas', f'Atenciones de Urgencia - Mayores de 65 Años en {hospital}. RM {selected_year}')

## Gráficos de Barra 3:
fig3_bar_total = grafico_atenciones_urgencia_barras(df_rm, 'Total', f'Atenciones de Urgencia - Todas las Edades en {hospital}. RM {selected_year}')
fig3_bar_menor1 = grafico_atenciones_urgencia_barras(df_rm, 'Menores_1', f'Atenciones de Urgencia Respiratoria - Menores de 1 Año en {hospital}. RM {selected_year}')
fig3_bar_mayor65 = grafico_atenciones_urgencia_barras(df_rm, 'De_65_y_mas', f'Atenciones de Urgencia Respiratoria - Mayores de 65 Años en {hospital}. RM {selected_year}')



# Configuración de la aplicación Streamlit


# Índice de navegación
st.sidebar.title("Índice de Navegación")
st.sidebar.markdown(f"""
- [Atenciones de urgencia por todas las causas, todas las causas respiratorias y COVID en {hospital}, RM](#atenciones-urgencia-todas-las-causas)
- [Atenciones de urgencia según tipo de causa respiratoria en {hospital}, RM](#atenciones-urgencia-segun-causas)
""")

# Gráficos de Área Apilada
st.markdown('<a name="atenciones-urgencia-todas-las-causas"></a>', unsafe_allow_html=True)
st.header(f'Atenciones de urgencia por todas las causas, todas las causas respiratorias y COVID en {hospital}, RM {selected_year}')

st.subheader('Todas las Edades')
st.plotly_chart(fig_area1_total)
st.markdown(f"Este gráfico muestra la evolución semanal del total de atenciones de urgencia por causas respiratorias y COVID-19 en todas las edades en {hospital} de la Región Metropolitana durante el año {selected_year}.")

st.subheader('Menores de 1 Año')
st.plotly_chart(fig_area1_menor1)
st.markdown(f"Este gráfico muestra la evolución semanal del total de atenciones de urgencia por causas respiratorias y COVID-19 en menores de 1 año en {hospital} de la Región Metropolitana durante el año {selected_year}.")

st.subheader('Mayores de 65 Años')
st.plotly_chart(fig_area1_mayor65)
st.markdown(f"Este gráfico muestra la evolución semanal del total de atenciones de urgencia por causas respiratorias y COVID-19 en mayores de 65 años en {hospital} de la Región Metropolitana durante el año {selected_year}.")

st.header(f'Distribución de Atenciones de Urgencia Respiratoria en {hospital}, RM {selected_year}')

st.subheader('Todas las Edades')
st.plotly_chart(fig2_pie_total)
st.plotly_chart(fig3_bar_total)
st.markdown(f"estos gráficos de torta y de barras muestra la bdistribución porcentual y la cantidad de las atenciones de urgencia por causas respiratorias y COVID-19 en relación al total de atenciones de urgencia en todas las edades en {hospital} de la Región Metropolitana durante el año {selected_year}.")


st.subheader('Menores de 1 Año')
st.plotly_chart(fig2_pie_menor1)
st.plotly_chart(fig3_bar_menor1)
st.markdown(f"estos gráficos de torta y de barras muestra la bdistribución porcentual y la cantidad de las atenciones de urgencia por causas respiratorias y COVID-19 en relación al total de atenciones de urgencia en menores de 1 año en {hospital} de la Región Metropolitana durante el año {selected_year}.")


st.subheader('Mayores de 65 Años')
st.plotly_chart(fig2_pie_mayor65)
st.plotly_chart(fig3_bar_mayor65)
st.markdown(f"estos gráficos de torta y de barras muestra la bdistribución porcentual y la cantidad de las atenciones de urgencia por causas respiratorias y COVID-19 en relación al total de atenciones de urgencia en mayores de 65 años en {hospital} de la Región Metropolitana durante el año {selected_year}.")


