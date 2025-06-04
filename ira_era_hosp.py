#%%
# Importar librerías
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

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
    options=[2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    index=7  # Establecer 2023 como valor predeterminado
)

hospital = st.sidebar.selectbox('Seleccione si desea ver la información de APS o Hospital',['APS','Hospitales'],index=1)
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

covid_hosp = [
    'Hospitalizaciones - Covid-19 Identificado (U7.1)',
    'Hospitalizaciones - Covid-19 No Identificado (U7.2)'
]
total_hosp = ['Hospitalizaciones - Total']
total_resp_hosp_sin_covid = ['Hospitalizaciones - Sistema Respiratorio']
total_resp_hosp = ['Hospitalizaciones - Sistema Respiratorio'] + covid_hosp
# Filtrar dataframes para APS y hospitales
if hospital == 'Hospitales':
    df_rm = df_rm.loc[(df_rm.GLOSATIPOESTABLECIMIENTO == 'Hospital')]
else:
    df_rm = df_rm.loc[~(df_rm.GLOSATIPOESTABLECIMIENTO == 'Hospital')]
#%%
# def grafico_area_hopitalizaciones_semanal(df, col, title):
#     fig = go.Figure()

#     df_au = df[df['Causa'].isin(total_hosp)].groupby('semana')[col].sum().reset_index()
#     df_resp = df[df['Causa'].isin(total_resp_hosp)].groupby('semana')[col].sum().reset_index()
#     df_covid = df[df['Causa'].isin(covid_hosp)].groupby('semana')[col].sum().reset_index()

#     # Grupo 1: Hospitalizaciones
#     fig.add_trace(go.Scatter(
#         x=df_au['semana'], y=df_au[col], 
#         mode='lines', name='Hospitalizaciones'
#     ))

#     # Grupo 2: Respiratorios (suma de df_resp y df_covid)
#     df_resp_covid = df_resp.copy()
#     df_resp_covid[col] += df_covid[col]

#     fig.add_trace(go.Scatter(
#         x=df_resp_covid['semana'], y=df_resp_covid[col], 
#         mode='lines', name='Hospitalizaciones respiratorias (incluye Covid)'
#     ))

#     # Hospitalizaciones por Covid (individualmente)
#     fig.add_trace(go.Scatter(
#         x=df_covid['semana'], y=df_covid[col], 
#         mode='lines', name='Hospitalizaciones por Covid'
#     ))

#     fig.update_layout(
#         title=title,
#         xaxis_title='Semana',
#         yaxis_title='N° de Hospitalizaciones',
#         legend_title='Leyenda',
#         template=GLOBAL_THEME,
#         yaxis=dict(tickformat='.', tickprefix='', ticksuffix='', separatethousands=True),
#     )
#         # Concatenar los DataFrames
#     df_concatenado = pd.concat([
#         df_au.rename(columns={col: 'Hospitalizaciones'}),
#         df_resp_covid.rename(columns={col: 'Hospitalizaciones respiratorias (incluye Covid)'}),
#         df_covid.rename(columns={col: 'Hospitalizaciones por Covid'})
#     ], axis=1)

#     # Eliminar duplicados de la columna 'semana' que se repiten en la concatenación
#     df_concatenado = df_concatenado.loc[:, ~df_concatenado.columns.duplicated()]

#     return fig, df_concatenado

def grafico_area_hospitalizaciones_semanal(df, col, title):
    # Filtrar y agrupar los datos

    df_covid = df[df['Causa'].isin(covid_hosp)].groupby('semana')[col].sum().reset_index()
    df_total = df[df['Causa'].isin(total_hosp)].groupby('semana')[col].sum().reset_index()
    df_total_resp = df[df['Causa'].isin(total_resp_hosp)].groupby('semana')[col].sum().reset_index()

    # Crear la figura del gráfico
    fig = go.Figure()

    # Añadir trazas para cada grupo de causas

    fig.add_trace(go.Scatter(
        x=df_covid['semana'], y=df_covid[col], 
        mode='lines', name='Hospitalizaciones Covid-19'
    ))
    fig.add_trace(go.Scatter(
        x=df_total_resp['semana'], y=df_total_resp[col], 
        mode='lines', name='Hospitalizaciones respiratorias totales'
    ))
    fig.add_trace(go.Scatter(
        x=df_total['semana'], y=df_total[col], 
        mode='lines', name='Hospitalizaciones totales'
    ))
    # Configuración del diseño del gráfico
    fig.update_layout(
        title=title,
        xaxis_title='Semana',
        yaxis_title='N° Hospitalizaciones',
        legend_title='Leyenda',
        template=GLOBAL_THEME,
        yaxis=dict(tickformat='.', tickprefix='', ticksuffix='', separatethousands=True)
    )

    # Concatenar los DataFrames
    df_concatenado = pd.concat([
        df_covid.rename(columns={col: 'Covid-19'}),
        df_total_resp.rename(columns={col: 'Total Respiratorias'}),
        df_total.rename(columns={col: 'Total'})
    ], axis=1)

    # Eliminar duplicados de la columna 'semana' que se repiten en la concatenación
    df_concatenado = df_concatenado.loc[:, ~df_concatenado.columns.duplicated()]

    return fig, df_concatenado

def grafico_hospitalizaciones_urgencia_pie(df, col, title):
    # Calcular totales por Causa
    val_total_hosp = df[df['Causa'].isin(total_hosp)][col].sum()
    val_total_respiratorias = df[df['Causa'].isin(total_resp_hosp)][col].sum()
    val_total_resp_hosp_sin_covid = df[df['Causa'].isin(total_resp_hosp_sin_covid)][col].sum()
    val_covid_hosp = df[df['Causa'].isin(covid_hosp)][col].sum()

    # Calcular los porcentajes en relación a total_urgencia
    percentage_respiratorias = (val_total_respiratorias / val_total_hosp) * 100 if val_total_hosp != 0 else 0
    percentage_total = 100  # Este valor siempre debe ser 100 ya que representa el total


    # Etiquetas y valores para el gráfico de pastel
    labels = [
        'Hospitalizaciones - Causas respiratorias', 
        'Hospitalizaciones - Total'
    ]
    values = [percentage_respiratorias, 100 - percentage_respiratorias]

    
    # Crear la figura del gráfico de pastel
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    # Configuración del diseño del gráfico
    fig.update_layout(
        title=title,
        template=GLOBAL_THEME
    )

    fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=20,
                      marker=dict(line=dict(color='#000000', width=0.5)))
    
    # Crear un DataFrame con los datos del gráfico
    df_pie = pd.DataFrame({
        'Causa': labels,
        'Porcentaje': values,
        'Total Atenciones': [val_total_respiratorias,val_total_hosp]
    })
    
    return fig, df_pie

def grafico_atenciones_urgencia_barras(df, col, title):
    # Calcular totales por Causa
    val_total = df[df['Causa'].isin(total_hosp)][col].sum()
    val_total_respiratorias = df[df['Causa'].isin(total_resp_hosp)][col].sum()
    val_total_resp_hosp_sin_covid = df[df['Causa'].isin(total_resp_hosp_sin_covid)][col].sum()
    val_total_covid = df[df['Causa'].isin(covid_hosp)][col].sum()
    
    # Etiquetas y valores para el gráfico de barras horizontales
    labels = [
        'Hospitalizaciones - Total',
        'Hospitalizaciones - Total causas respiratorias (incluye Covid)', 
        'Hospitalizaciones -Total causas respiratorias (No incluye Covid)', 
        'Hospitalizaciones - Covid-19', 
    ]
    values = [val_total, val_total_respiratorias, val_total_resp_hosp_sin_covid , val_total_covid]
    formatted_values = [f'{value:,.0f}'.replace(',', '.') for value in values]

    # Crear la figura del gráfico de barras horizontales
    fig = go.Figure(data=[go.Bar(x=values, 
                                 y=labels, 
                                 orientation='h', 
                                 text=formatted_values, 
                                 textposition='auto')])
    
    # Configuración del diseño del gráfico
    fig.update_layout(
        title=title,
        xaxis_title='N° Atenciones',
        yaxis_title='Causa',
        legend_title='Causas',
        template=GLOBAL_THEME,
        xaxis=dict(tickformat='.', tickprefix='', ticksuffix='', separatethousands=True)
    )

    # Crear un DataFrame con los datos del gráfico
    df_barras = pd.DataFrame({
        'Causa': labels,
        'Total Atenciones': values
    })
    
    return fig, df_barras

import streamlit as st
import pandas as pd
from io import BytesIO

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

#%%
# Graficos
## Gráfico de Área 1:
fig_area1_total, df_area1_total = grafico_area_hospitalizaciones_semanal(df_rm, 'Total', f'Hospitalizaciones - Todas las Edades {selected_year}')
fig_area1_menor1, df_area1_menor1= grafico_area_hospitalizaciones_semanal(df_rm, 'Menores_1', f'Hospitalizaciones - Menor de 1 Año {selected_year}')
fig_area1_mayor65, df_area1_mayor65 = grafico_area_hospitalizaciones_semanal(df_rm, 'De_65_y_mas', f'Hospitalizaciones - 65 años y más {selected_year}')

## Gráfico de Pie 2:
fig2_pie_total, df_pie_total = grafico_hospitalizaciones_urgencia_pie(df_rm, 'Total', f'Hospitalizaciones - Todas las Edades en {hospital}. RM {selected_year}')
fig2_pie_menor1, df_pie_menor1 = grafico_hospitalizaciones_urgencia_pie(df_rm, 'Menores_1', f'Hospitalizaciones - Menores de 1 Año en {hospital}. RM {selected_year}')
fig2_pie_mayor65, df_pie_mayor65 = grafico_hospitalizaciones_urgencia_pie(df_rm, 'De_65_y_mas', f'Hospitalizaciones - Mayores de 65 Años en {hospital}. RM {selected_year}')

## Gráficos de Barra 3:
fig3_bar_total, df_bar_total = grafico_atenciones_urgencia_barras(df_rm, 'Total', f'Hospitalizaciones - Todas las Edades en {hospital}. RM {selected_year}')
fig3_bar_menor1, df_bar_menor1 = grafico_atenciones_urgencia_barras(df_rm, 'Menores_1', f'Hospitalizaciones Respiratoria - Menores de 1 Año en {hospital}. RM {selected_year}')
fig3_bar_mayor65, df_bar_mayor65 = grafico_atenciones_urgencia_barras(df_rm, 'De_65_y_mas', f'Hospitalizaciones Respiratoria - Mayores de 65 Años en {hospital}. RM {selected_year}')



# Configuración de la aplicación Streamlit


# Índice de navegación
st.sidebar.title("Índice de Navegación")
st.sidebar.markdown(f"""
- [Hospitalizaciones por todas las causas, todas las causas respiratorias, Influenza y COVID en {hospital}, RM](#atenciones-urgencia-todas-las-causas)
- [Hospitalizaciones según tipo de causa respiratoria en {hospital}, RM](#atenciones-urgencia-segun-causas)
""")

# Gráficos de Área Apilada
st.markdown('<a name="atenciones-urgencia-todas-las-causas"></a>', unsafe_allow_html=True)
st.header(f'Hospitalizaciones por todas las causas, todas las causas respiratorias, Influenza y COVID en {hospital}, RM {selected_year}')

st.subheader('Todas las Edades')

st.plotly_chart(fig_area1_total)
st.markdown(f"El gráfico muestra la evolución semanal del total de Hospitalizaciones por causas respiratorias, Influenza  y COVID-19 en todas las edades en {hospital} de la Región Metropolitana durante el año {selected_year}.")

st.subheader('Menores de 1 Año')
st.plotly_chart(fig_area1_menor1)
st.markdown(f"El gráfico muestra la evolución semanal del total de Hospitalizaciones por causas respiratorias, Influenza  y COVID-19 en menores de 1 año en {hospital} de la Región Metropolitana durante el año {selected_year}.")

st.subheader('Mayores de 65 Años')
st.plotly_chart(fig_area1_mayor65)
st.markdown(f"El gráfico muestra la evolución semanal del total de Hospitalizaciones por causas respiratorias, Influenza  y COVID-19 en mayores de 65 años en {hospital} de la Región Metropolitana durante el año {selected_year}.")

st.header(f'Distribución de Hospitalizaciones Respiratoria en {hospital}, RM {selected_year}')

st.subheader('Todas las Edades')
st.plotly_chart(fig2_pie_total)
st.plotly_chart(fig3_bar_total)
st.markdown(f"Los gráficos anteriores, tanto de torta como de barras, muestran la distribución porcentual y la cantidad total de Hospitalizaciones por causas respiratorias y COVID-19, en comparación con el total de Hospitalizaciones en todas las edades en {hospital}, ubicado en la Región Metropolitana, durante el año {selected_year}.")

st.subheader('Menores de 1 Año')
st.plotly_chart(fig2_pie_menor1)
st.plotly_chart(fig3_bar_menor1)
st.markdown(f"Los gráficos anteriores, tanto de torta como de barras, muestran la distribución porcentual y la cantidad total de Hospitalizaciones por causas respiratorias y COVID-19, en comparación con el total de Hospitalizaciones de las personas menores de 1 año en {hospital}, ubicado en la Región Metropolitana, durante el año {selected_year}.")


st.subheader('Mayores de 65 Años')
st.plotly_chart(fig2_pie_mayor65)
st.plotly_chart(fig3_bar_mayor65)
st.markdown(f"Los gráficos anteriores, tanto de torta como de barras, muestran la distribución porcentual y la cantidad total de Hospitalizaciones por causas respiratorias y COVID-19, en comparación con el total de Hospitalizaciones de las personas mayores de 65 años en {hospital}, ubicado en la Región Metropolitana, durante el año {selected_year}.")

#%%
def descargar_todos_los_dfs():
    # Crear un objeto BytesIO para guardar el archivo Excel en memoria
    output = BytesIO()

    # Crear un objeto ExcelWriter con pandas y xlsxwriter
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Guardar cada DataFrame en una pestaña separada
        df_area1_total.to_excel(writer, index=False, sheet_name='Todas las Edades - Area')
        df_area1_menor1.to_excel(writer, index=False, sheet_name='Menores de 1 Año - Area')
        df_area1_mayor65.to_excel(writer, index=False, sheet_name='Mayores de 65 Años - Area')
        df_pie_total.to_excel(writer, index=False, sheet_name='Todas las Edades - Pie')
        df_pie_menor1.to_excel(writer, index=False, sheet_name='Menores de 1 Año - Pie')
        df_pie_mayor65.to_excel(writer, index=False, sheet_name='Mayores de 65 Años - Pie')
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
        file_name=f'Atenciones_Urgencia_{selected_year}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
# Llamar a la función para generar el botón de descarga
descargar_todos_los_dfs()