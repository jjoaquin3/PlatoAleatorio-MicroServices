## Descripción del Proyecto

**PlatoAleatorio-MicroServices** 

🚀 Es un sistema basado en microservicios diseñado para automatizar la preparación de platos en un restaurante durante una jornada de donación de comida. El sistema permite que el gerente haga pedidos masivos de platos aleatorios, que la cocina prepare tras recibir los ingredientes, y que la bodega gestione el inventario y realice compras a la plaza de mercado cuando sea necesario.


### Propósito
El sistema gestiona todo el proceso desde la solicitud de un plato, pasando por la verificación de ingredientes en la bodega, hasta la compra de ingredientes faltantes en la plaza de mercado. Todo esto se realiza de manera asincrónica y escalable.

### Microservicios Involucrados
1. **Cocina (kitchen-server)**: Recibe y procesa los pedidos de platos aleatorios.
2. **Bodega (warehouse-server)**: Gestiona el inventario y despacha los igredientes.
3. **Plaza de Mercado (market-server)**: Procesa las compras de ingredientes faltantes a solicitud de la bodega.
4. **Middle (middle-server)**: 🔥 Orquesta las interacciones entre los diferentes servicios y coordina el flujo de trabajo de los pedidos.
5. **Middle Worker (middle-worker)**: 🔥 Se encarga de procesar tareas en segundo plano de forma asincrónica, como la verificación de stock y la gestión de compras.
6. **Report Service (reports-server)**: Proporciona informes  sobre los pedidos, ingredientes, y compras realizadas.
7. **Frontend (frontend-server)**: Interfaz para gestionar pedidos, visualizar estados y el inventario de ingredientes.

El sistema está diseñado para manejar pedidos masivos y funcionar de manera eficiente en un entorno de microservicios.

---
## 🔹 Arquitectura e Infraestructura

**PlatoAleatorio-LunchOrderMicroServices** se basa en una arquitectura de microservicios para gestionar las solicitudes de platos, ingredientes y compras. A continuación se describen los componentes principales de la arquitectura:

### Componentes Principales

- **Frontend**: 
  - **Nginx**: Servidor web y proxy inverso que redirige las solicitudes desde el frontend hacia los microservicios (middle-server, reports-server) y maneja las peticiones API con CORS habilitado. permitiendo el mapeo entre los dockers.


``` bash
├── index.html
├── ingredients.html
├── lunch.html
├── orders.html
├── purchases.html
├── recipes.html
├── assets
├── css
│   └── style.css
└── js
    ├── api.js
    ├── ingredients.js
    ├── lunch.js
    ├── orders.js
    ├── purchases.js
    └── recipes.js
``` 

- **Microservicios**:
  - **Cocina (kitchen-server)**: Gestiona las solicitudes de preparación de platos aleatorios, almacenando datos en **MongoDB**.
  - **Bodega (warehouse-server)**: Gestiona el inventario de ingredientes, realiza compras a la plaza de mercado cuando faltan ingredientes y usa **PostgreSQL**.
  - **Plaza de Mercado (market-server)**: Realiza las compras de ingredientes faltantes desde una **API externa** si no están disponibles en la bodega.
  - **Middle (middle-server)**: Orquesta el flujo entre cocina, bodega y plaza de mercado, manejando las interacciones asincrónicas.
  - **Middle Worker (middle-worker)**: Procesa tareas en segundo plano, como la verificación de ingredientes y la gestión de compras.
  - **Report Service (reports-server)**: Genera informes sobre pedidos, ingredientes y compras.

``` bash
├── kitchen-service
│   ├── dummy.txt
│   └── app
│       ├── main.py
│       ├── config
│       │   ├── database_nosql.py
│       │   ├── date_zone.py
│       │   └── dependencies.py
│       ├── controller
│       │   ├── order_controller.py
│       │   └── recipe_controller.py
│       ├── model
│       │   ├── order.py
│       │   ├── recipe.py
│       │   └── schema
│       │       ├── order.py
│       │       └── recipe.py
│       ├── repository
│       │   ├── order_repository.py
│       │   └── recipe_repository.py
│       ├── security
│       │   └── auth.py
│       ├── service
│       │   ├── order_service.py
│       │   └── recipe_service.py
│       └── util
├── market-service
│   ├── dummy.txt
│   └── app
│       ├── main.py
│       ├── config
│       │   ├── database.py
│       │   ├── date_zone.py
│       │   └── dependencies.py
│       ├── controller
│       │   └── market_controller.py
│       ├── model
│       │   ├── purchase.py
│       │   └── schema
│       │       └── purchase.py
│       ├── repository
│       │   └── purchase_repository.py
│       ├── security
│       │   └── auth.py
│       ├── service
│       │   └── market_service.py
│       └── util
│           └── external_api.py
├── middle-service
│   ├── worker.py
│   └── app
│       ├── main.py
│       ├── config
│       │   ├── date_zone.py
│       │   ├── dependencies.py
│       │   └── redis_client.py
│       ├── controller
│       │   ├── debug_controller.py
│       │   └── flow_controller.py
│       ├── model
│       │   ├── order.py
│       │   └── schema
│       │       └── order.py
│       ├── repository
│       │   └── remote_gateway.py
│       ├── security
│       │   └── auth.py
│       ├── service
│       │   ├── flow_service.py
│       │   └── queue_worker.py
│       └── util
│           └── retry.py
├── reports-service
│   ├── dummy.txt
│   └── app
│       ├── main.py
│       ├── config
│       ├── controller
│       │   └── reports_controller.py
│       ├── model
│       │   └── schema
│       │       └── order.py
│       ├── repository
│       │   └── remote_gateway.py
│       ├── security
│       │   └── auth.py
│       ├── service
│       │   └── reports_service.py
│       └── util
└── warehouse-service
    ├── dummy.txt
    └── app
        ├── main.py
        ├── config
        │   ├── database.py
        │   └── dependencies.py
        ├── controller
        │   └── ingredient_controller.py
        ├── model
        │   ├── ingredient.py
        │   └── schema
        │       └── ingredient.py
        ├── repository
        │   └── ingredient_repository.py
        ├── security
        │   └── auth.py
        └── service
            └── ingredient_service.py
```

- **Bases de Datos**:
  - **PostgreSQL**: Almacena el inventario de ingredientes y los detalles de las compras.
  - **MongoDB**: Almacena los datos de las órdenes y recetas.
  - **Redis**: Utilizado para manejar la comunicación asincrónica entre microservicios y almacenar datos en caché.

### Redes

- **kitchen_network**: Conecta el kitchen-server con su base de datos NoSQL y otros servicios relevantes.
- **warehouse_network**: Conecta el warehouse-server con su base de datos SQL y otros servicios.
- **market_network**: Conecta el market-server con la plaza de mercado y otros servicios.
- **restaurant_network**: Red común que permite la comunicación entre el frontend, microservicios y bases de datos.

### Diagrama


``` bash
                                +----------------------+
                                |      Frontend        |
                                |   (Comunicaciones +  |
                                |    proxy)            |
                                +----------+-----------+
                                           |
                       +-------------------+------------------+
                       |                                      |
                       v                                      v
             +----------------------+               +---------------------+
             |    Middle Server     |               |   Reports Service   |
             | (Orquestador Lógica) |               |  (Genera Informes)  |
             +----------------------+               +---------------------+



                       +----------------------+
                       |    Middle Server     |
                       | (Orquestador Lógica) |
                       +----------+-----------+
                                  |
               +------------------+------------------+
               |                                     |
               v                                     v
       +-------------------+                  +----------------------+
       |      Redis        | <--------------->|     Worker          |
       | (Colas Asíncronas)|                  |(Procesos Asíncronos)|
       +-------------------+                  +----------------------+




                           +----------------------+
                           |    Middle Server     |
                           | (Orquestador Lógica) |
                           +-----------+----------+
                                       |
            +--------------------------+-------------------------+
            |                          |                         |
            v                          v                         v
    +------------------+      +------------------+      +------------------+
    |   Kitchen        |      |   Warehouse      |      |   Market         |
    |   Server         |      |   Server         |      |   Server         |
    |  (MongoDB)       |      |  (PostgreSQL)    |      |  (PostgreSQL)    |
    +------------------+      +------------------+      +------------------+
``` 

- **Frontend**: La interfaz de usuario se conecta a Nginx, que redirige las solicitudes a los microservicios adecuados.
- **Middle**: El middle-server gestiona la lógica de negocio, verificando la disponibilidad de ingredientes y gestionando compras a través de la plaza de mercado.
- **Bodega**: El warehouse-server gestiona el inventario y realiza compras cuando es necesario.
- **Plaza de Mercado**: El market-server interactúa con la plaza de mercado externa para realizar compras de ingredientes faltantes.

---
## 🔹 Tecnologías

Este proyecto está construido utilizando una combinación de herramientas y tecnologías modernas para asegurar escalabilidad, rendimiento y facilidad de mantenimiento. A continuación se enumeran las principales tecnologías utilizadas:

- **Docker**: Contenerización de los microservicios para garantizar un entorno consistente y aislado durante el desarrollo y despliegue.
- **Docker Compose**: Orquestación de los contenedores Docker para simplificar la configuración y el manejo de los microservicios y sus dependencias.
- **Python**: Lenguaje principal para el desarrollo de los microservicios, utilizando frameworks como **FastAPI** y **Uvicorn**.
- **FastAPI**: Framework para crear las APIs de los microservicios con un rendimiento excepcional y fácil manejo de validaciones.
- **Redis**: Sistema de almacenamiento en caché y gestión de colas asincrónicas, utilizado para manejar tareas de procesamiento en segundo plano.
- **PostgreSQL**: Base de datos relacional utilizada para almacenar el inventario de ingredientes y las compras.
- **MongoDB**: Base de datos NoSQL utilizada para almacenar los datos de las órdenes y recetas.
- **Nginx**: Servidor web y proxy inverso, usado para redirigir solicitudes y manejar la carga entre los servicios.
- **API Externa**: Interacción con una API externa para realizar compras de ingredientes faltantes cuando no están disponibles en el inventario.

Estas tecnologías permiten que el sistema sea escalable, eficiente y fácil de mantener.

---
## 🔹 Instrucciones de Configuración y Despliegue

### Configuración del Entorno Local

Para configurar el entorno local y levantar todos los servicios utilizando Docker, sigue los siguientes pasos:

1. **Clona el repositorio:**

   Primero, clona el repositorio en tu máquina local:
```bash
    git clone https://github.com/jjoaquin3/PlatoAleatorio-MicroServices.git
```

    Entra y busca la carpeta stack

```bash
    cd PlatoAleatorio-MicroServices/stack
```

2. **Construir y levantar los contenedores:**

Utiliza Docker Compose para construir y levantar los contenedores.

```bash
docker-compose -p alegra up --build -d
```
Donde "alegra" es el nombre que se la asigna al proyecto esto te ayuda identifar mejor los recursos.

Esto iniciará todos los servicios definidos en el archivo `docker-compose.yml`, incluidos los contenedores para las bases de datos y microservicios. Estan configurados para que se inicien las DB y el contenedor `restaurant-db-init` se apagara al terminar la iniciaclización.

3. **Inicializar las bases de datos:**

El servicio de inicialización de bases de datos (`restaurant-db-init`) se encargará de preparar las bases de datos al iniciar los contenedores. Asegúrate de que este servicio esté corriendo para que las bases de datos se configuren correctamente.

### Despliegue en un Servidor

Para desplegar el proyecto en un servidor, sigue estos pasos:

1. **Configura Docker en tu servidor:**

Asegúrate de tener Docker y Docker Compose instalados en el servidor. Si no los tienes, puedes seguir las guías oficiales:
- [Instalar Docker](https://docs.docker.com/get-docker/)
- [Instalar Docker Compose](https://docs.docker.com/compose/install/)

2. **Sube el código al servidor:**

Puedes subir el código de tu proyecto a tu servidor utilizando cualquier  método que prefieras.

3. **Levanta los contenedores en el servidor:**

Una vez que el código esté en el servidor, navega al directorio del proyecto y ejecuta el siguiente comando para iniciar los contenedores:

```bash
docker-compose -p alegra up --build -d
```

Esto configurará y levantará todos los servicios en el servidor.

### Enlace al Repositorio Privado de GitHub

El código fuente de este proyecto está alojado en un repositorio privado de GitHub.
Esta privado pero ahi vamos.

```
- **Repositorio privado en GitHub**: `https://github.com/jjoaquin3/PlatoAleatorio-MicroServices.git`
```

---
## 🔹 EndPoints y API

A continuación se listan los principales endpoints disponibles para interactuar con los microservicios:

### Endpoints de **Middle Server** (Orquestador Lógica)

- **POST /orders/request**  
  Solicita la preparación de un nuevo plato aleatorio.
  - **Body**: `{ "order": <order_id> }`
  - **Respuesta**: `{ "order": <order_id>, "recipe": <recipe_name> }`

- **POST /orders/validate**  
  Valida si los ingredientes están disponibles y gestiona el proceso de preparación.
  - **Body**: `{ "order": <order_id>, "state": "complete" | "pending" }`
  - **Respuesta**: `{ "state": <new_state>, "step": <current_step> }`

### Endpoints de **Kitchen Server** (Cocina)

- **POST /orders/build**  
  Crea una nueva orden de cocina con los ingredientes disponibles.
  - **Body**: `{ "order": <order_id>, "recipe": <recipe_name> }`
  - **Respuesta**: `{ "state": "process", "step": "kitchen" }`

- **GET /orders/{<order_id>}**  
  Obtiene el estado actual de la orden en la cocina.
  - **Respuesta**: `{ "order": <order_id>, "state": <state>, "step": <step> }`

### Endpoints de **Warehouse Server** (Bodega)

- **POST /ingredients/get_ingredients_by_order**  
  Solicita los ingredientes necesarios para la preparación de un plato.
  - **Body**: `{ "order": <order_id> }`
  - **Respuesta**: `{ "ingredients": <list_of_ingredients>, "step": "warehouse" }`

- **POST /ingredients/update_inventory**  
  Actualiza el inventario de ingredientes en la bodega.
  - **Body**: `{ "ingredient": <ingredient_name>, "quantity": <quantity> }`
  - **Respuesta**: `{ "status": "success", "updated_inventory": <updated_inventory> }`

### Endpoints de **Market Server** (Plaza de Mercado)

- **POST /market/purchase**  
  Realiza una compra de ingredientes en la plaza de mercado.
  - **Body**: `{ "order": <order_id>, "ingredient": <ingredient_name> }`
  - **Respuesta**: `{ "status": "success", "quantity_sold": <quantity> }`

- **GET /market/status**  
  Verifica el estado de los ingredientes disponibles en el mercado.
  - **Respuesta**: `{ "ingredient": <ingredient_name>, "quantity_available": <quantity> }`

### Endpoints de **Reports Service** (Informes)

- **GET /reports/orders**  
  Obtiene un informe de todas las órdenes procesadas.
  - **Respuesta**: `{ "orders": <list_of_orders> }`

- **GET /reports/ingredients**  
  Obtiene un informe de los ingredientes utilizados.
  - **Respuesta**: `{ "ingredients": <list_of_ingredients> }`

- **GET /reports/purchases**  
  Obtiene un informe de todas las compras realizadas en el mercado.
  - **Respuesta**: `{ "purchases": <list_of_purchases> }`

  - **GET /reports/recipes**  
  Obtiene un informe de todas las recetas.
  - **Respuesta**: `{ "recipes": <list_of_recibes> }`

---
## 🔹 Consideraciones lo que se viene o ya esta

A continuación, se incluyen algunas consideraciones y recomendaciones importantes.

### 1. **Arquitectura Desacoplada**
   - **Microservicios**:Todos los microservicios estén bien definidos y se comuniquen a través de APIs claras. La arquitectura es completamente desacoplada, lo que facilita el escalado y el mantenimiento.

   - **Uso de Docker**: Utilizar Docker y Docker Compose garantiza que el entorno de desarrollo sea consistente en diferentes máquinas. Asegúrate de que todos los servicios puedan ser levantados con `docker-compose` sin problemas.

### 2. **Manejo de Errores y Logs**
   - **Manejo adecuado de errores**: Es esencial que todos los microservicios manejen errores correctamente y devuelvan respuestas informativas cuando algo falla. Usando códigos de estado HTTP adecuados y mensajes de error claros.
   - **Logs**: Cada microservicio registra los errores y las interacciones importantes, especialmente los relacionados con la validación de ingredientes, la creación de órdenes y la interacción con la plaza de mercado.

### 3. **Asincronía y Gestión de Tareas**
   - **Uso de Redis y Worker**: Se utiliza Redis para gestionar las colas y la comunicación asincrónica entre los microservicios. Los Workers deben encargarse de las tareas en segundo plano (como las compras pendientes de ingredientes) de manera eficiente.
   - **Control de Concurrencia**: Las tareas asincrónicas se gestionen correctamente, evitando bloqueos o fallos en la ejecución de tareas concurrentes.

### 4. **Base de Datos y Consistencia**
   - **Consistencia de Datos**:Las bases de datos estén siempre actualizadas y consistentes, especialmente cuando se manejan cambios en el inventario o el estado de las órdenes. Chequear compose.
   - **Uso de MongoDB y PostgreSQL**: MongoDB para almacenar las órdenes y recetas de manera flexible y **PostgreSQL** para gestionar el inventario y las compras de manera relacional.

### 5. **Escalabilidad**
   - **Escalabilidad Horizontal**: La arquitectura puedes agregar más instancias de microservicios para manejar una carga mayor sin que el sistema se vea afectado.  **Docker** y **Docker Compose** para facilitar la creación de múltiples instancias de los microservicios según sea necesario.
   
   ##### PD. La orden 0 es solo para ver si el init lograba insertar algo a mongo pero va a parecer que esta complete y en kitchen :)
---

🔥 **¡Listo! 



