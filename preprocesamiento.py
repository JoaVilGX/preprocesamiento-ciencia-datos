import pandas as pd
import numpy as np
import argparse
import sys
from sklearn.preprocessing import LabelEncoder

def cargar_datos(ruta):
    """Carga un dataset desde un archivo CSV."""
    try:
        df = pd.read_csv(ruta)
        print(f"[OK] Dataset cargado: {ruta} -> {df.shape [0]} filas, {df.shape[1]} columnas")
        return df
    except Exception as e:
        print(f"[ERROR] No se pudo cargar el archivo: {e}")
        sys.exit(1)

def guardar_datos(df, ruta):
    """Guarda el DataFrame procesado en un archivo CSV."""
    try:
        df.to_csv(ruta, index=False)
        print(f"[OK] Dataset procesado guardado en: {ruta}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el archivo: {e}")
        sys.exit(1)

def manejar_nulos(df, estrategia='media', columnas_categoricas=None):
    """
    Reemplaza valores nulos
    estrategia: 'media' (solo numéricas), 'mediana', 'moda' (categóricas/numéricas), 'eliminar'
    """
    if estrategia == 'eliminar':
        antes = len(df)
        df = df.dropna()
        print(f"[INFO] Eliminación de nulos: {antes - len(df)} filas eliminadas")
        return df
    
    # Procesar columnas numéricas
    num_cols = df.select_dtypes(include=[np.number]).columns
    if estrategia == 'media':
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
        print(f"[INFO] Valores nulos reemplazados por la media en columnas numéricas")
    elif estrategia == 'mediana':
        df[num_cols] = df [num_cols].fillna(df[num_cols].median())
        print(f"[INFO] Valores nulos reemplazados por la mediana en columnas numéricas")
    
    # Para columnas categóricas (object), usar la moda (valor más frecuente)
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        moda = df[col].mode()[0] if not df[col].mode().empty else "DESCONOCIDO"
        df[col] = df[col].fillna(moda)
        print(f"[INFO] Columna categórica '{col}': nulos reemplazados por moda '{moda}'")

        return df

def normalizar(df, columnas=None):
    """
    Normalización Min-Max para columnas numéricas.
    Si columnas=None, aplica a todas las numéricas.
    """
    if columnas is None:
        columnas = df.select_dtypes(include=[np.number]).columns.tolist()
    else:
        # Verificar que las columnas existen y son numéricas
        columnas = [col for col in columnas if col in df.columns and pd.api.type.is_numeric_dtype(df[col])] 
    
    for col in columnas:
        min_val = df[col].min()
        max_val = df[col].max()
        if max_val - min_val != 0:
            df[col] = (df[col] - min_val) / (max_val - min_val)
        else:
            df[col] = 0
    print(f"[INFO] Normalización Min-Max aplicada a {len(columnas)} columnas: {columnas}")
    return df

def codificar_categoricas(df, metodo='onehot'):
    """
    Codifica variables categóricas.
    metodo: 'onehot' (crea columnas dummy) o 'label' (LabelEncoder).
    """
    cat_cols = df.select_dtypes(include=['object']).columns
    if len(cat_cols) == 0:
        print("[INFO] No hay columnas categóricas para codificar")
        return df
    
    if metodo == 'label':
        le = LabelEncoder()
        for col in cat_cols:
            df[col] = le.fit_transform(df[col].astype(str))
        print(f"[INFO] Label Encoding aplicado a {len(cat_cols)} columnas: {list(cat_cols)}")
    elif metodo == 'onehot':
        df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
        print(f"[INFO] One-Hot Encoding aplicado a {len(cat_cols)} columnas originales. Nuevas dimensiones: {df.shape}")
    else:
        print(f"[ERROR] Método de codificación '{metodo}' no reconocido. Use 'onehot' o 'label'.")
        sys.exit(1)
    return df

def eliminar_duplicados(df):
    """Elimina filas duplicadas basadas en todas las columnas."""
    antes = len(df)
    df = df.drop_duplicates()
    print(f"[INFO] Duplicados eliminados: {antes - len(df)} filas")
    return df

def preprocesamiento_completo(df, estrategia_nulos='media', metodo_codificacion='onehot', normalizar_columnas=None):
    """
    Aplica todo el flujo de preprocesamiento en orden:
    1. Manejo de nulos
    2. Eliminación de duplicados
    3. Codificación de categóricas
    4. Normalización (al final, sobre columnas numéricas resultantes)
    """
    print("\n--- Iniciando preprocesamiento completo ---")
    df_limpio = manejar_nulos(df, estrategia=estrategia_nulos)
    df_limpio = eliminar_duplicados(df_limpio)
    df_limpio = codificar_categoricas(df_limpio, metodo=metodo_codificacion)
    df_limpio = normalizar(df_limpio, columnas=normalizar_columnas)
    print("--- Preprocesamiento completado ---\n")
    return df_limpio

def demo():
    print("\n EJECUTANDO DEMO DE PRUEBA (sin argumentos)\n")
    datos_demo = {
        'edad': [25, 30, None, 35, 30, None],
        'ciudad': ['Madrid', 'Barcelona', 'Madrid', 'Valencia', 'Barcelona', 'Madrid'],
        'ingreso': [30000, 45000, 50000, None, 45000, 50000]
    }
    df = pd.DataFrame(datos_demo)
    print("Dataset original:")
    print(df)
    df_proc = preprocesamiento_completo(df)
    print("\nDataset procesado:")
    print(df_proc)
    print("\n Demo completada exitosamente.")

def main():
    if len (sys.argv) == 1:
        # Sin argumentos -> ejecutar demo
        demo()
        return
    parser = argparse.ArgumentParser(description='Preprocesamiento completo de un dataset CSV')
    parser.add_argument('input', help='Ruta del archivo CSV de entrada')
    parser.add_argument('output', help='Ruta del archivo CSV de salida')
    parser.add_argument('--estrategia_nulos', choices=['media', 'mediana', 'eliminar'],
                        default='media', help='Estrategia para valores nulos (por defecto: media)')
    parser.add_argument('--metodo_codificacion', choices=['onehot', 'label'], 
                        default='onehot', help='Método de codificación de categóricas (por defecto: onehot)')
    parser.add_argument('--normalizar_columnas', nargs='+', default=None, 
                        help='Lista de columnas específicas a normalizar (por defecto: todas numéricas)')
    args = parser.parser_args()

    print("\n=== PREPROCESAMIENTO DE DATASET ===\n")
    # Cargar datos
    df = cargar_datos(args.input)

    # Mostrar estadísticas iniciales
    print(f"\nResumen inicial:")
    print(f"    - Valores nulos por columna:\n{df.isnull().sum()}")
    print(f"    - Duplicados: {df.duplicated().sum()}")
    print(f"    - Tipos de columnas:\n{df.dtypes}")

    # Aplicar preprocesamiento
    df_proc = preprocesamiento_completo(
        df,
        estrategia_nulos=args.estrategia_nulos,
        metodo_codificacion=args.metodo_codificacion,
        normalizar_columnas=args.normalizar_columnas
    )
    
    # Guardar resultado
    guardar_datos(df_proc, args.output)

    print("Proceso finalizado exitosamente.")

if __name__ == "__main__":
    main()