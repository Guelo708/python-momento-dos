import os
import pandas as pd
import numpy as np

def limpiar_monto_moneda(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """Limpia el símbolo de moneda ($) y comas, convirtiendo a numérico."""
    df_limpio = df.copy()
    if columna in df_limpio.columns:
        df_limpio[columna] = (
            df_limpio[columna]
            .astype(str)
            .str.replace('$', '', regex=False)
            .str.replace(',', '', regex=False)
            .str.strip()
        )
        df_limpio[columna] = pd.to_numeric(df_limpio[columna], errors='coerce')
    return df_limpio

def limpiar_dataframes(df_predios: pd.DataFrame, df_facturas: pd.DataFrame):
    """
    Limpia ambos DataFrames:
    - Elimina duplicados
    - Sanitiza texto a minúsculas / quita espacios al inicio y final
    - Valida e imputa valores nulos
    - Limpia valores de moneda
    - Guarda copias limpias en Data/processed/
    """
    print("\n--- Iniciando proceso de limpieza ---")

    # Copias de trabajo
    df_p = df_predios.copy()
    df_f = df_facturas.copy()

    # 1. Validar y eliminar filas duplicadas
    duplicados_p = df_p.duplicated().sum()
    duplicados_f = df_f.duplicated().sum()
    df_p = df_p.drop_duplicates()
    df_f = df_f.drop_duplicates()
    print(f"Duplicados eliminados -> Predios: {duplicados_p}, Facturas: {duplicados_f}")

    # 2. Sanitizar columnas de texto: minúsculas y strip (quitar espacios sobrantes)
    for col in df_p.select_dtypes(include=['object']).columns:
        df_p[col] = df_p[col].astype(str).str.strip().str.lower()

    for col in df_f.select_dtypes(include=['object']).columns:
        df_f[col] = df_f[col].astype(str).str.strip().str.lower()

    # 3. Limpieza de montos en facturas
    df_f = limpiar_monto_moneda(df_f, "monto_cobrado")

    # 4. Validar y manejar valores nulos
    # En predios: si vereda o texto viene 'nan' o nulo, asignar 'el paraiso'
    df_p["vereda"] = df_p["vereda"].replace(["nan", "none", "", np.nan], "el paraiso")

    # En facturas: imputar el promedio en montos nulos y 'sin registro' en método de pago
    monto_promedio = df_f["monto_cobrado"].mean()
    df_f["monto_cobrado"] = df_f["monto_cobrado"].fillna(monto_promedio)
    df_f["metodo_pago"] = df_f["metodo_pago"].replace(["nan", "none", "", np.nan], "sin registro")

    # 5. Guardar copias en Data/processed/
    os.makedirs(os.path.join("Data", "processed"), exist_ok=True)
    df_p.to_csv(os.path.join("Data", "processed", "predios_limpio.csv"), index=False)
    df_f.to_csv(os.path.join("Data", "processed", "facturas_limpio.csv"), index=False)

    print("Limpieza completada. Datos procesados guardados en Data/processed/.")
    return df_p, df_f