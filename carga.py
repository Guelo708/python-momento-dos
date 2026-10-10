import os
import pandas as pd

def cargar_datos_raw():
    """
    Carga los archivos CSV crudos desde Data/raw/ y retorna dos DataFrames:
    df_predios y df_facturas.
    """
    ruta_predios = os.path.join("Data", "raw", "predios.csv")
    ruta_facturas = os.path.join("Data", "raw", "facturas.csv")

    try:
        df_predios = pd.read_csv(ruta_predios)
        df_facturas = pd.read_csv(ruta_facturas)
        print(" Archivos 'predios.csv' y 'facturas.csv' cargados exitosamente desde Data/raw/.")
        return df_predios, df_facturas
    except Exception as e:
        print(f"Error al cargar los archivos desde Data/raw/: {e}")
        return None, None