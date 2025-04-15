import os
import sys
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

def initialize_db_sql():
    print("--- Iniciando resturant db.")  
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    POSTGRES_SCHEMA_WAREHOUSE = os.getenv("POSTGRES_SCHEMA_WAREHOUSE")
    POSTGRES_SCHEMA_MARKET = os.getenv("POSTGRES_SCHEMA_MARKET")

    POSTGRES_USER_WAREHOUSE = os.getenv("POSTGRES_USER_WAREHOUSE")
    POSTGRES_PASSWORD_WAREHOUSE = os.getenv("POSTGRES_PASSWORD_WAREHOUSE")

    POSTGRES_USER_MARKET = os.getenv("POSTGRES_USER_MARKET")
    POSTGRES_PASSWORD_MARKET = os.getenv("POSTGRES_PASSWORD_MARKET")
    
    # Establecer la conexión a la base de datos
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )    
    cur = conn.cursor()
    print("Conexión a la base de datos establecida correctamente.")

    # Crear los esquemas y usuarios si no existen
    try:
        # Crear usuarios y otorgar permisos
        print("Crear Esquemas.")
        cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {};").format(sql.Identifier(POSTGRES_SCHEMA_WAREHOUSE)))
        cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {};").format(sql.Identifier(POSTGRES_SCHEMA_MARKET)))

        # Crear usuarios
        print("Crear Usuarios.")
        cur.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s;").format(sql.Identifier(POSTGRES_USER_WAREHOUSE)), [POSTGRES_PASSWORD_WAREHOUSE])
        cur.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s;").format(sql.Identifier(POSTGRES_USER_MARKET)), [POSTGRES_PASSWORD_MARKET])

        # Asegurarse de que el usuario 'postgres' tiene permisos en los esquemas
        print("Otorgar permisos al usuario 'POSTGRES_USER'.")
        cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON SCHEMA {} TO {};").format(sql.Identifier(POSTGRES_SCHEMA_WAREHOUSE), sql.Identifier(POSTGRES_USER)))
        cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON SCHEMA {} TO {};").format(sql.Identifier(POSTGRES_SCHEMA_MARKET), sql.Identifier(POSTGRES_USER)))

        # Otorgar permisos a los usuarios en los esquemas
        print("Crear Permisos 1.")
        cur.execute(sql.SQL("GRANT USAGE, CREATE ON SCHEMA {} TO {};").format(sql.Identifier(POSTGRES_SCHEMA_WAREHOUSE), sql.Identifier(POSTGRES_USER_WAREHOUSE)))
        cur.execute(sql.SQL("GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA {} TO {};").format(sql.Identifier(POSTGRES_SCHEMA_WAREHOUSE), sql.Identifier(POSTGRES_USER_WAREHOUSE)))

        print("Crear Permisos 2.")
        cur.execute(sql.SQL("GRANT USAGE, CREATE ON SCHEMA {} TO {};").format(sql.Identifier(POSTGRES_SCHEMA_MARKET), sql.Identifier(POSTGRES_USER_MARKET)))
        cur.execute(sql.SQL("GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA {} TO {};").format(sql.Identifier(POSTGRES_SCHEMA_MARKET), sql.Identifier(POSTGRES_USER_MARKET)))

        print("Crear Permisos 3.")
        # Otorgar permisos generales para conexión a la base de datos
        cur.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO {};").format(sql.Identifier(POSTGRES_DB), sql.Identifier(POSTGRES_USER_WAREHOUSE)))
        cur.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO {};").format(sql.Identifier(POSTGRES_DB), sql.Identifier(POSTGRES_USER_MARKET)))

        # Confirmar cambios
        conn.commit()
        print("Base de datos inicializada correctamente.")

    except Exception as e:
        print(f"Error durante la inicialización de la base de datos: {e}")
        conn.rollback()

    finally:
        # Cerrar conexión
        cur.close()
        conn.close()

    print("Inicialización completada exitosamente.")
    print("--- Finalizando restaurant db.")  

if __name__ == '__main__':
    initialize_db_sql()