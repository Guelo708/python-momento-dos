import os
import pandas as pd

def realizar_merge(df_predios=None, df_facturas=None) -> pd.DataFrame:
    """
    Realiza las validaciones pre-merge y une los DataFrames.
    Si no recibe los DataFrames en memoria, los intenta cargar desde Data/processed/.
    """
    ruta_p = os.path.join("Data", "processed", "predios_limpio.csv")
    ruta_f = os.path.join("Data", "processed", "facturas_limpio.csv")

    # Si no vienen en memoria, cargarlos desde la carpeta processed
    if df_predios is None or df_facturas is None:
        if os.path.exists(ruta_p) and os.path.exists(ruta_f):
            print("\n Cargando datos limpios directamente desde Data/processed/...")
            df_predios = pd.read_csv(ruta_p)
            df_facturas = pd.read_csv(ruta_f)
        else:
            print(" No hay datos limpios en memoria ni en Data/processed/. Ejecute la Opción 2 primero.")
            return None

    print("\n--- Validaciones Pre-Merge ---")

    ids_predios = set(df_predios["id_predio"].unique())
    ids_facturas = set(df_facturas["id_predio"].unique())

    coincidencias = ids_facturas.intersection(ids_predios)
    huerfanos = ids_facturas.difference(ids_predios)

    print(f"Total predios únicos: {len(ids_predios)}")
    print(f"Total facturas asociadas a predios únicos: {len(ids_facturas)}")
    print(f"Predios con facturas coincidentes: {len(coincidencias)}")

    if huerfanos:
        print(f"Atención: Existen {len(huerfanos)} facturas asociadas a predios inexistentes.")
    else:
        print("Integridad referencial verificada: Todas las facturas coinciden con predios válidos.")

    # Unir DataFrames (Merge tipo inner)
    df_unido = pd.merge(df_facturas, df_predios, on="id_predio", how="inner")
    print(f"\nMerge completado. Resultado: {df_unido.shape[0]} filas y {df_unido.shape[1]} columnas.")
    return df_unido