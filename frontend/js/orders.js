import { fetchOrders } from './api.js';  // Importa la función de api.js

function convertToLocalTime(timestamp) {
    // Crear un objeto Date usando el timestamp
    const date = new Date(timestamp * 1000); // Multiplicamos por 1000 porque el timestamp es en segundos
    date.setHours(date.getHours() - 6);  // Ajustamos la hora a GMT-6

    // Obtener los componentes de la fecha
    const day = String(date.getDate()).padStart(2, '0'); // Día con 2 dígitos
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Mes con 2 dígitos (Mes es 0-indexado)
    const year = date.getFullYear();  // Año completo
    const hours = String(date.getHours()).padStart(2, '0'); // Hora con 2 dígitos
    const minutes = String(date.getMinutes()).padStart(2, '0'); // Minutos con 2 dígitos
    const seconds = String(date.getSeconds()).padStart(2, '0'); // Segundos con 2 dígitos

    // Retornar la fecha formateada como dd/mm/yyyy hh:mm:ss
    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
}

async function displayOrders() {
    try {
        const orders = await fetchOrders();
        const container = document.getElementById('orders-container');
        container.innerHTML = '';  // Limpiar el contenedor

        orders.forEach(order => {
            const row = document.createElement('tr');  // Crear una fila de la tabla

            // Convertir los timestamps a fechas legibles
            const createdAt = convertToLocalTime(order.created_at);
            const updatedAt = convertToLocalTime(order.updated_at);

            // Agregar celdas para cada columna de la tabla
            row.innerHTML = `
                <td>${order.order}</td>
                <td>${order.recipe}</td>
                <td>${order.state}</td>
                <td>${order.step}</td>
                <td>${createdAt}</td>
                <td>${updatedAt}</td>                
            `;

            container.appendChild(row);  // Añadir la fila a la tabla
        });
    } catch (error) {
        console.error(error);
        alert("No se pudieron cargar las órdenes");
    }
}

// Llamar la función para cargar las órdenes al iniciar la página
displayOrders();
