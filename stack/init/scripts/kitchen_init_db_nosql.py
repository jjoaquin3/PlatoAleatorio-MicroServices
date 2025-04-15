import os
from pymongo import MongoClient
from datetime import datetime
import sys
import json

def initialize_db_nosql_orders():
    try:
        print("--- Iniciando orders colection.")         
        
        # Obtener las variables de entorno para la conexión
        mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        mongo_db = os.getenv("MONGO_DB")
        mongo_host = os.getenv("MONGO_HOST")
        mongo_port = os.getenv("MONGO_PORT")
        
        # URI de conexión a MongoDB
        #mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@mongodb:27017/{mongo_db}"
        #mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@mongodb:27017/{mongo_db}"
        mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
        
        # Establecer la conexión a la base de datos
        client = MongoClient(mongo_uri)
        db = client.get_database(mongo_db) 

        print("Conexión a MongoDB establecida correctamente.")              
        
        # Crear Orden de ejemplo
        new_order = {
            "order": 0,
            "state": "complete",
            "recipe": "Ketchup Fries",
            "step": "kitchen",
            "created_at": 1744642233,
            "updated_at": 1744642233,
            "ingredients": [
                {
                    "name": "potato",
                    "state": "complete",
                    "quantity": 4,
                    "pending": 0,
                    "send_out": 4
                },
                {
                    "name": "ketchup",
                    "state": "complete",
                    "quantity": 4,
                    "pending": 0,
                    "send_out": 4
                }
            ]
        }

        # Guardar cambios
        orders_collection = db.orders
        orders_collection.delete_many({})
        orders_collection.insert_one(new_order) 

        print("Orden inicial insertada correctamente.")
    
    except Exception as e:
        print("Error durante la inicialización de la base de datos:", e)
        sys.exit(1)  # Detener el contenedor en caso de error

    finally:
        # Cerrar conexión
        client.close()
        print("Conexión a MongoDB cerrada.")
    
    print("Inicialización completada exitosamente.")
    print("--- Finalizando orders colection.")

def initialize_db_nosql_recipes():
    try:
        print("--- Iniciando recipes colection.")         
        
        # Obtener las variables de entorno para la conexión
        mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        mongo_db = os.getenv("MONGO_DB")
        mongo_host = os.getenv("MONGO_HOST")
        mongo_port = os.getenv("MONGO_PORT")
        
        # URI de conexión a MongoDB
        #mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@mongodb:27017/{mongo_db}"
        #mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@mongodb:27017/{mongo_db}"
        mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/"
        
        # Establecer la conexión a la base de datos
        client = MongoClient(mongo_uri)
        db = client.get_database(mongo_db) 

        print("Conexión a MongoDB establecida correctamente.")              
        
        # Leer datos desde CSV y cargarlos en la tabla
        path = '/workspace/dataset/recipes.json'
        with open(path, "r") as f:
            recipes_data = json.load(f)

        # Guardar cambios
        recipes_collection = db.recipes
        recipes_collection.delete_many({})
        recipes_collection.insert_many(recipes_data) 

        print("Recipes insertadas correctamente.")
    
    except Exception as e:
        print("Error durante la inicialización de la base de datos:", e)
        sys.exit(1)  # Detener el contenedor en caso de error

    finally:
        # Cerrar conexión
        client.close()
        print("Conexión a MongoDB cerrada.")
    
    print("Inicialización completada exitosamente.")
    print("--- Finalizando recipes colection.")                

if __name__ == '__main__':
    initialize_db_nosql_orders()
    initialize_db_nosql_recipes()
