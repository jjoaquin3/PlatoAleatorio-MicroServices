import psycopg2
import pandas as pd
import os
import sys

def initialize_db_sql():
    try:
        print("--- Iniciando market schema.")         
        # Establecer la conexión a la base de datos
        connection = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER_MARKET'),
            password=os.getenv('POSTGRES_PASSWORD_MARKET')
        )
        cursor = connection.cursor()
        print("Conexión a la base de datos establecida correctamente.")
        
        # Obtener el nombre del esquema desde las variables de entorno
        schema = os.getenv('POSTGRES_SCHEMA_MARKET')
        
        # Crear el esquema si no existe
        #cursor.execute(f'CREATE SCHEMA IF NOT EXISTS {schema};')
        
        # Crear la tabla purchases si no existe en el esquema
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {schema}.purchases (
                id SERIAL PRIMARY KEY,
                ingredient_name VARCHAR(255) NOT NULL,
                quantity INT NOT NULL,
                origin VARCHAR(32) NULL,
                purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        print("Esquema y tabla creados exitosamente.")
        
        # Truncar la tabla antes de insertar nuevos datos
        cursor.execute(f'TRUNCATE TABLE {schema}.purchases;')

        # Leer datos desde el archivo CSV y cargarlos en la tabla
        path = '/workspace/dataset/purchases.csv'
        df = pd.read_csv(path, sep='|')
        for index, row in df.iterrows():
            cursor.execute(f'''
                INSERT INTO {schema}.purchases (ingredient_name, quantity, origin) 
                VALUES (%s, %s, %s);
            ''', (row['name'], row['quantity'], "start"))
        
        print("Datos insertados correctamente en la base de datos.")

        # Confirmar los cambios y cerrar la conexión
        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        print("Error durante la inicialización de la base de datos:", e)
        sys.exit(1)  # Esto asegura que el contenedor se detenga si hay un fallo.
    
    print("Inicialización completada exitosamente.")
    print("--- Finalizando market schema.")         

if __name__ == '__main__':
    initialize_db_sql()
