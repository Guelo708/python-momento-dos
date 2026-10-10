import pandas as pd
from colorama import init, Fore, Style

# Inicializar colorama (autoreset asegura que el color vuelva a normal tras cada print)
init(autoreset=True)

def analizar_datos(df_unido: pd.DataFrame):
    """
    Realiza un análisis completo de datos sobre el DataFrame unificado,
    aplicando formatos numéricos claros, colores con colorama y métricas extendidas.
    """
    print(Fore.CYAN + Style.BRIGHT + "\n==================================================")
    print(Fore.YELLOW + Style.BRIGHT + "       ANÁLISIS DETALLADO DE DATOS - AGUAS PARAÍSO")
    print(Fore.CYAN + Style.BRIGHT + "==================================================")

    # -------------------------------------------------------------------------
    # 1. ANÁLISIS DE FRECUENCIA
    # -------------------------------------------------------------------------
    print(Fore.YELLOW + Style.BRIGHT + "\n1. Análisis de Frecuencia:")
    
    # Tipo de predio con mayor frecuencia
    frecuencia_tipo = df_unido["tipo_predio"].value_counts()
    tipo_top = frecuencia_tipo.idxmax()
    cant_top = frecuencia_tipo.max()
    print(f"   • Tipo de predio más recurrente: {Fore.GREEN + Style.BRIGHT}{tipo_top.title()}{Style.RESET_ALL} con {Fore.WHITE + Style.BRIGHT}{cant_top}{Style.RESET_ALL} registros.")

    # Sector con mayor cantidad de predios
    frecuencia_sector = df_unido["sector"].value_counts()
    sector_top = frecuencia_sector.idxmax()
    cant_sec_top = frecuencia_sector.max()
    print(f"   • Sector con mayor número de predios/facturas: {Fore.GREEN + Style.BRIGHT}{sector_top.title()}{Style.RESET_ALL} con {Fore.WHITE + Style.BRIGHT}{cant_sec_top}{Style.RESET_ALL} registros.")

    # -------------------------------------------------------------------------
    # 2. ANÁLISIS DE AGREGACIÓN (RECAUDO Y PROMEDIOS POR SECTOR)
    # -------------------------------------------------------------------------
    print(Fore.YELLOW + Style.BRIGHT + "\n2. Análisis de Agregación (Recaudo General por Sector):")
    
    agregado_sector = df_unido.groupby("sector")["monto_cobrado"].agg(["sum", "mean", "count"]).reset_index()
    
    # Formatear la salida para evitar notaciones científicas (e+05) y quitar decimales al promedio
    agregado_sector["Monto Total ($)"] = agregado_sector["sum"].apply(lambda x: f"${x:,.0f}")
    agregado_sector["Monto Promedio ($)"] = agregado_sector["mean"].apply(lambda x: f"${x:,.0f}")
    agregado_sector["Sector"] = agregado_sector["sector"].str.title()
    agregado_sector["Total Facturas"] = agregado_sector["count"]

    # Seleccionar columnas a mostrar
    df_agregado_view = agregado_sector[["Sector", "Monto Total ($)", "Monto Promedio ($)", "Total Facturas"]]

    # Imprimir encabezados de tabla con color Azul
    encabezados = f"{Fore.BLUE + Style.BRIGHT}{'Sector':<26} {'Monto Total ($)':<18} {'Monto Promedio ($)':<20} {'Total Facturas':<15}"
    print(encabezados)
    print(Fore.BLUE + "-" * 78)

    # Imprimir las filas de datos en blanco
    for _, fila in df_agregado_view.iterrows():
        print(f"{Fore.WHITE}{fila['Sector']:<26} {fila['Monto Total ($)']:<18} {fila['Monto Promedio ($)']:<20} {fila['Total Facturas']:<15}")

    # -------------------------------------------------------------------------
    # 3. ANÁLISIS DE MOROSIDAD POR SECTOR (NUEVO)
    # -------------------------------------------------------------------------
    print(Fore.YELLOW + Style.BRIGHT + "\n3. Análisis de Morosidad por Sector (Sectores en Riesgo):")
    
    # Filtrar solo facturas vencidas o pendientes
    df_mora = df_unido[df_unido["estado_factura"].isin(["vencida", "pendiente"])]
    mora_por_sector = df_mora.groupby("sector")["monto_cobrado"].agg(["sum", "count"]).reset_index()
    mora_por_sector = mora_por_sector.sort_values(by="sum", ascending=False)
    
    encabezados_mora = f"{Fore.RED + Style.BRIGHT}{'Sector Con Mayor Mora':<26} {'Monto En Mora ($)':<20} {'Facturas En Mora':<15}"
    print(encabezados_mora)
    print(Fore.RED + "-" * 65)

    for _, fila in mora_por_sector.iterrows():
        sector_nom = fila['sector'].title()
        monto_f = f"${fila['sum']:,.0f}"
        cant_f = fila['count']
        print(f"{Fore.WHITE}{sector_nom:<26} {Fore.RED}{monto_f:<20} {Fore.WHITE}{cant_f:<15}")

    # -------------------------------------------------------------------------
    # 4. ANÁLISIS CON FILTRADO Y CONTEO GENERAL
    # -------------------------------------------------------------------------
    print(Fore.YELLOW + Style.BRIGHT + "\n4. Resumen Global de Cartera y Mora:")
    conteo_mora = len(df_mora)
    monto_mora = df_mora["monto_cobrado"].sum()
    monto_total_facturado = df_unido["monto_cobrado"].sum()
    porcentaje_mora = (monto_mora / monto_total_facturado) * 100 if monto_total_facturado > 0 else 0

    print(f"   • Total de facturas en mora (Pendientes/Vencidas): {Fore.RED + Style.BRIGHT}{conteo_mora}{Style.RESET_ALL} de {len(df_unido)} facturas.")
    print(f"   • Monto total de dinero pendiente de recaudo: {Fore.RED + Style.BRIGHT}${monto_mora:,.0f}{Style.RESET_ALL}")
    print(f"   • Porcentaje global de morosidad sobre el recaudo: {Fore.YELLOW + Style.BRIGHT}{porcentaje_mora:.1f}%{Style.RESET_ALL}")

    # -------------------------------------------------------------------------
    # 5. ANÁLISIS DE MÉTODOS DE PAGO (NUEVO)
    # -------------------------------------------------------------------------
    print(Fore.YELLOW + Style.BRIGHT + "\n5. Análisis de Canales de Pago Preferidos por los Usuarios:")
    metodos_pago = df_unido[df_unido["metodo_pago"] != "sin registro"]["metodo_pago"].value_counts().reset_index()
    metodos_pago.columns = ["Método de Pago", "Cantidad"]

    encabezados_metodo = f"{Fore.CYAN + Style.BRIGHT}{'Método de Pago':<25} {'Transacciones Exitosas':<20}"
    print(encabezados_metodo)
    print(Fore.CYAN + "-" * 50)

    for _, fila in metodos_pago.iterrows():
        metodo_nom = fila['Método de Pago'].upper()
        cant_m = fila['Cantidad']
        print(f"{Fore.WHITE}{metodo_nom:<25} {cant_m:<20}")

    print(Fore.CYAN + Style.BRIGHT + "\n==================================================")
    print(Fore.GREEN + Style.BRIGHT + "            FIN DEL INFORME TÉCNICO")
    print(Fore.CYAN + Style.BRIGHT + "==================================================")