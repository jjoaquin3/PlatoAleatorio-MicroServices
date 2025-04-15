# Importar las funciones de inicialización de los scripts
from scripts.kitchen_init_db_nosql import initialize_db_nosql_recipes as kitchen_init_recipes
from scripts.kitchen_init_db_nosql import initialize_db_nosql_orders as kitchen_init_orders
from scripts.restaurant_init_db_sql import initialize_db_sql as restaurant_init
from scripts.market_init_db_sql import initialize_db_sql as market_init
from scripts.warehouse_init_db_sql import initialize_db_sql as warehouse_init


# Llamar las funciones de inicialización
if __name__ == '__main__':
    kitchen_init_recipes()
    print('\n\n')
    kitchen_init_orders()
    print('\n\n')  
    restaurant_init() 
    print('\n\n')
    warehouse_init()
    print('\n\n')
    market_init() 
    
