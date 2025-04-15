// api.js

// Para el frontend dentro del contenedor:
/*const API_URL = 'http://reports-service:8000';  // Nombre de contenedor en la red Docker

// Si el frontend está accediendo desde el navegador, usa localhost
if (window.location.hostname === 'localhost') {
    API_URL = 'http://localhost:8005';  // Cambiar para solicitudes desde el navegador
}
*/
const API_URL = '/api'

const API_KEY = 'secret123';  // API Key para la autenticación

// Función para obtener todas las órdenes
async function fetchOrders() {
    const response = await fetch(`${API_URL}/orders`, {
        method: 'GET',
        headers: {
            'X-API-KEY': API_KEY  // Incluir la API Key en las cabeceras
        }
    });
    if (!response.ok) {
        throw new Error('Error al obtener las órdenes');
    }
    return await response.json();
}

// Función para obtener todos los ingredientes
async function fetchIngredients() {
    const response = await fetch(`${API_URL}/ingredients`, {
        method: 'GET',
        headers: {
            'X-API-KEY': API_KEY  // Incluir la API Key en las cabeceras
        }
    });
    if (!response.ok) {
        throw new Error('Error al obtener los ingredientes');
    }
    return await response.json();
}

// Función para obtener todas las compras
async function fetchPurchases() {
    const response = await fetch(`${API_URL}/purchases`, {
        method: 'GET',
        headers: {
            'X-API-KEY': API_KEY  // Incluir la API Key en las cabeceras
        }
    });
    if (!response.ok) {
        throw new Error('Error al obtener las compras');
    }
    return await response.json();
}

// Función para obtener todas las recetas
async function fetchRecipes() {
    const response = await fetch(`${API_URL}/recipes`, {
        method: 'GET',
        headers: {
            'X-API-KEY': API_KEY  // Incluir la API Key en las cabeceras
        }
    });
    if (!response.ok) {
        throw new Error('Error al obtener las recetas');
    }
    return await response.json();
}

async function requestLunch(orderId) {
    console.log("1");
    const response = await fetch(`${API_URL}/lunch`, {  // Endpoint de solicitud de lunch
        method: 'POST',
        headers: {
            'X-API-KEY': API_KEY,  // API Key en las cabeceras
            'Content-Type': 'application/json',  // Indicamos que estamos enviando JSON
        },        
        body: JSON.stringify({ order: orderId })  // Enviamos el número de la orden como JSON
    });
    console.log("2")
    if (!response.ok) {
        console.log("3")
        const error = await response.json();
        console.error('Error en respuesta:', error);
        console.log("4")
        throw new Error('Error al realizar la solicitud de platillo');
    }
    console.log("5")
    const responseBody = await response.text();
    try {
        console.log("6")
        const data = JSON.parse(responseBody);  // Intentar convertirlo a JSON
        console.log("7")
        return data;
    } catch (error) {
        console.log("8")
        console.error('No es JSON:', responseBody);
        console.log("9")
        throw new Error('La respuesta no es JSON');
        console.log("10")
    }

    //return await response.json();  // Retorna la respuesta en formato JSON
}

// Exportar las funciones para ser usadas en otros archivos
export { fetchOrders, fetchIngredients, fetchPurchases, fetchRecipes, requestLunch  };
