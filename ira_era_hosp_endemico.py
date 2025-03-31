import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

GLOBAL_THEME = 'seaborn'

def create_endemic_corridor(df, cause, total_column, title):
    # Filtrar el dataframe para la causa específica
    df_cause = df.loc[df['Causa'].isin(cause)]
    
    # Agrupar los datos por año y semana
    grouped = df_cause.groupby(by=['año', 'semana'])[total_column].sum().reset_index()
    
    # Calcular la mediana y los cuartiles para cada semana
    quartiles = grouped.groupby('semana')[total_column].quantile([0.25, 0.5, 0.75]).unstack().reset_index()
    quartiles.columns = ['semana', 'percentil_25', 'mediana', 'percentil_75']
    
    # Agregar los datos del año seleccionado
    selected_year = grouped['año'].max()  # Seleccionar el último año disponible
    current_year_data = grouped[grouped['año'] == selected_year][['semana', total_column]]
    current_year_data.columns = ['semana', 'current_year_total']
    endemic_corridor = pd.merge(quartiles, current_year_data, on='semana', how='left')
    
    # Visualizar el corredor endémico
    fig = go.Figure()
    
    # Éxito (bajo el percentil 25)
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['percentil_25'], 
        mode='lines', 
        name='Éxito (Percentil 25)', 
        line=dict(color='rgba(0, 255, 0, 0.2)')
    ))
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=[0] * len(endemic_corridor), 
        mode='lines', 
        line=dict(color='rgba(0, 255, 0, 0.2)'), 
        fill='tonexty',
        fillcolor='rgba(0, 255, 0, 0.2)',
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Seguridad (entre percentil 25 y mediana)
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['mediana'], 
        mode='lines', 
        name='Seguridad (Mediana)', 
        line=dict(color='rgba(0, 0, 255, 0.2)')
    ))
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['percentil_25'], 
        mode='lines', 
        line=dict(color='rgba(0, 0, 255, 0.2)'), 
        fill='tonexty',
        fillcolor='rgba(0, 0, 255, 0.2)',
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Alerta (entre mediana y percentil 75)
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['percentil_75'], 
        mode='lines', 
        name='Alerta (Percentil 75)', 
        line=dict(color='rgba(255, 255, 0, 0.2)')
    ))
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['mediana'], 
        mode='lines', 
        line=dict(color='rgba(255, 255, 0, 0.2)'), 
        fill='tonexty',
        fillcolor='rgba(255, 255, 0, 0.2)',
        hoverinfo='skip',
        showlegend=False
    ))

    # Mediana histórica
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['mediana'], 
        mode='lines', 
        name='Mediana Histórica', 
        line=dict(color='blue')
    ))

    # Datos del año en curso
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['current_year_total'], 
        mode='lines+markers', 
        name=f'Año {selected_year}', 
        line=dict(color='red')
    ))

    fig.update_layout(
        title=f'Corredor Endémico de {title}',
        xaxis_title='Semana',
        yaxis_title='Total de Atenciones',
        template=GLOBAL_THEME,
        yaxis=dict(tickformat='.0f', tickprefix='', ticksuffix='')
    )
    
    st.plotly_chart(fig)
    
    return endemic_corridor

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

def load_data(start_year, end_year):
    dataframes = []
    for year in [year for year in range(start_year, end_year + 1) if year not in {2020, 2021}]:
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

st.title('Visualización del Corredor Endémico 2023')

hospital = st.sidebar.selectbox('Seleccione si desea ver la información de APS o Hospital', ['APS', 'Hospitales'], index=1)

start_year, end_year = 2018, 2024
selected_year = end_year 
list_df_rm = load_data(start_year, end_year)
if list_df_rm is None:
    st.stop()
df_rm = pd.concat(list_df_rm)

if hospital == 'Hospitales':
    df_rm = df_rm.loc[(df_rm.GLOSATIPOESTABLECIMIENTO == 'Hospital')]
else:
    df_rm = df_rm.loc[~(df_rm.GLOSATIPOESTABLECIMIENTO == 'Hospital')]

irab = [
    'Atenciones de urgencia - Neumonía (J12-J18)',
    'Atenciones de urgencia - Bronquitis/bronquiolitis aguda (J20-J21)',
    'Atenciones de urgencia - Crisis obstructiva bronquial (J40-J46)'
]
iraa = ['Atenciones de urgencia - IRA Alta (J00-J06)']
covid = [
    'Hospitalizaciones - Covid-19 Identificado (U7.1)',
    'Hospitalizaciones - Covid-19 No Identificado (U7.2)']
# total_au = ['Atenciones de urgencia - Total']
total_resp = ['Hospitalizaciones - Sistema Respiratorio'] + covid
# influ = ['Atenciones de urgencia - Influenza (J09-J11)']
# otras = ['Atenciones de urgencia - Otra causa respiratoria (J22, J30-J39, J47, J60-J98)']

causas_dict = {
    # 'Total Atenciones de urgencias': total_au,
    'Total Respiratorios': total_resp,
    # 'IRAB': irab,
    # 'IRAA': iraa,
    # 'COVID': covid,
    # 'Influenza': influ,
    # 'Otras': otras
}

causa_select = st.sidebar.selectbox('Seleccione causa:', causas_dict.keys(), 0)
causa = causas_dict[causa_select]
dict_columnas = {'Total': 'Total de la población', 
                 'Menores_1': 'Menores de 1 año', 
                 'De_1_a_4': '1 a 4 años', 
                 'De_5_a_14': '5 a 14 años', 
                 'De_15_a_64': '15 a 64 años',
                 'De_65_y_mas': 'Mayores de 65 años'}

st.markdown("""
### ¿Qué es un corredor endémico?
Un corredor endémico es una herramienta epidemiológica utilizada para monitorear enfermedades infecciosas y otros eventos de salud a lo largo del tiempo. Se basa en el análisis de datos históricos para determinar los límites esperados de ocurrencia de una enfermedad durante un período específico (por ejemplo, semanal). Estos límites ayudan a identificar niveles de éxito, seguridad, alerta y alerta roja.

#### Componentes del Corredor Endémico:
- **Éxito (Percentil 25)**: Representa el límite bajo del corredor endémico. Si los casos están por debajo de este límite, se considera que la situación está bajo control.
- **Seguridad (Mediana)**: Representa el valor medio de los casos esperados. Los casos entre el percentil 25 y la mediana indican una situación dentro del rango normal.
- **Alerta (Percentil 75)**: Representa el límite superior del corredor endémico. Los casos entre la mediana y el percentil 75 indican una situación de alerta.
- **Alerta Roja (por encima del Percentil 75)**: Representa una situación crítica donde los casos superan significativamente el nivel esperado.
- **Consideraciones Especiales**: Los años 2020 y 2021 han sido excluidos del cálculo del corredor endémico debido a las distorsiones provocadas por la pandemia de COVID-19, asegurando así que el análisis se base en datos que reflejen condiciones epidemiológicas más estables.
        
#### Instrucciones:
1. Seleccione si desea ver la información de APS (Atención Primaria de Salud) o Hospitales.
2. Seleccione la causa de las atenciones de urgencia que desea analizar.
3. Observe los gráficos generados para cada grupo de edad.

Esta herramienta proporciona una visualización clara de las tendencias de atención de urgencia para diferentes causas y grupos de edad, ayudando a identificar situaciones anómalas y a tomar decisiones informadas.
""")

for key, value in dict_columnas.items():
    df_endemic_corridor = create_endemic_corridor(df_rm, cause=causa, total_column=key, title=value)

#%%
import pandas as pd
from io import BytesIO

def descargar_dataframes_endemicos(dataframes, nombres_hojas, file_name):
    # Crear un objeto BytesIO para guardar el archivo Excel en memoria
    output = BytesIO()

    # Crear un objeto ExcelWriter con pandas y xlsxwriter
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Guardar cada DataFrame en una pestaña separada
        for df, nombre_hoja in zip(dataframes, nombres_hojas):
            df.to_excel(writer, index=False, sheet_name=nombre_hoja)
        
        # Asegurarse de que el archivo se haya escrito completamente en el objeto BytesIO
        writer.close()
        processed_data = output.getvalue()

    # Descargar el archivo Excel
    st.download_button(
        label="Descargar todos los datos como Excel",
        data=processed_data,
        file_name=file_name,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# En tu flujo de trabajo principal
dataframes = []
nombres_hojas = []

for key, value in dict_columnas.items():
    df_endemic_corridor = create_endemic_corridor(df_rm, cause=causa, total_column=key, title=value)
    dataframes.append(df_endemic_corridor[['semana','percentil_75','mediana','percentil_25','current_year_total']])
    nombres_hojas.append(f'{value} - End')

# Llamar a la función para descargar los DataFrames
descargar_dataframes_endemicos(dataframes, nombres_hojas, f'Corredor_Endemico_{selected_year}.xlsx')
