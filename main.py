import sys
from carga import cargar_datos_raw
from limpieza import limpiar_dataframes
from merge import realizar_merge
from analisis import analizar_datos

def mostrar_menu():
    print("\n" + "="*50)
    print("     SISTEMA DE ANÁLISIS DE DATOS - AGUAS PARAÍSO")
    print("="*50)
    print("1. Cargar datos crudos (Data/raw)")
    print("2. Limpiar DataFrames (Nulos, duplicados, sanitizar)")
    print("3. Validaciones pre-merge y realizar Merge")
    print("4. Análisis del conjunto de datos unido")
    print("5. Salir")
    print("="*50)

def main():
    # Variables de estado para almacenar los DataFrames entre opciones
    df_predios_raw = None
    df_facturas_raw = None

    df_predios_limpio = None
    df_facturas_limpio = None

    df_unido = None

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            print("\n[Opción 1: Carga de Datos]")
            df_predios_raw, df_facturas_raw = cargar_datos_raw()

        elif opcion == "2":
            print("\n[Opción 2: Limpieza de Datos]")
            if df_predios_raw is None or df_facturas_raw is None:
                print(" Primero debes cargar los datos seleccionando la Opción 1.")
            else:
                df_predios_limpio, df_facturas_limpio = limpiar_dataframes(df_predios_raw, df_facturas_raw)

        elif opcion == "3":
            print("\n[Opción 3: Validaciones Pre-Merge y Merge]")
            if df_predios_limpio is None or df_facturas_limpio is None:
                print("Primero debes limpiar los datos seleccionando la Opción 2.")
            else:
                df_unido = realizar_merge(df_predios_limpio, df_facturas_limpio)

        elif opcion == "4":
            print("\n[Opción 4: Análisis de Datos]")
            if df_unido is None:
                print(" Primero debes realizar el merge seleccionando la Opción 3.")
            else:
                analizar_datos(df_unido)

        elif opcion == "5":
            print("\n ¡Gracias por usar el sistema de Aguas Paraíso! Saliendo...")
            sys.exit()

        else:
            print(" Opción inválida. Por favor seleccione un número del 1 al 5.")

if __name__ == "__main__":
    main()