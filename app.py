import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
#AJUSTAR FECHAS( Asumo que no hay nadie de más de cien años)----------------------------------------------------------------------------------------------
def adjust_year(dt):
    if pd.isna(dt):
        return dt  # Retorna la misma fecha si es NaT
    year = dt.year
    if year > datetime.now().year: #Cambiar la fecha si es mayor a la actual
        year -= 100
        return dt.replace(year=year)
    return dt
#LIMPIEZA TABLA-------------------------------------------------------------------------------------------------------------------------------------------
def clean_data(df):
    

    #Eliminamos filas con valores nulos
    df=df.dropna()
    #Eliminamos espacios de los nombres de las columnas
    df.columns=df.columns.str.strip()

    #Arreglar valores monetarios-----------------------------------------------------
    
    monetary_columns = ['VALOR PATRIMONIO', 'PRIMAS REALES', 'PRIMAS RESCATADAS', 'VARIACIÓN']
    for column in monetary_columns:
         if column in df.columns:
             df[column] = df[column].str.replace('€', '', regex=False).str.replace(',', '', regex=False).str.strip()
             df[column] = df[column].replace('-   ', '0', regex=False)
             df[column] = df[column].replace('-', '0', regex=False)
             df[column] = df[column].str.replace(r'^\s*-?\s*', lambda x: '-' if '-' in x.group() else '', regex=True)
             df[column] = df[column].astype(float)
    
    #Arreglar columna porcentaje-----------------------------------------------------
    df['%'] = df['%'].str.replace('%', '').astype(float) / 100
    #Arreglar fechas.----------------------------------------------------------------
    date_columns=['FECHA EFECTO','F. NACIMIENTO']
    for column in date_columns:
         df[column] = pd.to_datetime(df[column], errors='coerce', dayfirst=True)
         df[column] = df[column].apply(adjust_year)

    #Eliminar columnas con un solo valor. Es decir, que no aporta información.-------
    columnas_que_eliminar= [col for col in df.columns if df[col].nunique() == 1]
    df = df.drop(columns=columnas_que_eliminar)
    return df
#MAIN---------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    #Imagen side
     st.sidebar.image("bomba.jpeg",use_column_width=True)
     st.title("Hidrostal")

     nombre=st.text_input("Porfavor,ingresa tu nombre")
     if nombre:
        st.write(f"Bienvenido,{nombre}!¿Te gustaría preguntarle algo a la IA sobre la empresa?")
         # Verificar si se ingresó un nombre y mostrar un mensaje de bienvenida
        # Esperar a que se presione Enter antes de limpiar la caja de texto
     archivo_csv=st.file_uploader("Introduzca un csv",type=['csv'])
     if archivo_csv is not None:
        # Leer el CSV en un DataFrame de pandas
        df = pd.read_csv(archivo_csv)
    
        # Mostrar el DataFrame original
        st.subheader('Datos Originales')
        st.write(df)
    
        # Limpiar el DataFrame
        cleaned_df = clean_data(df)
    
        # Mostrar el DataFrame limpio
        st.subheader('Datos Limpiados')
        st.write(cleaned_df)
if __name__ == "__main__":
     main()