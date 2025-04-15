import { fetchPurchases } from './api.js';  // Importa la función de api.js

// Función para convertir la fecha de compra a formato 'dd/mm/yyyy hh:mm:ss' en GMT-6
function convertToLocalTime(timestamp) {
    const date = new Date(timestamp);  // El timestamp es una fecha ISO, no es necesario multiplicarlo por 1000
    date.setHours(date.getHours() - 6);  // Ajustamos la hora a GMT-6

    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
}

async function displayPurchases() {
    try {
        const purchases = await fetchPurchases();
        const container = document.getElementById('purchases-container');
        container.innerHTML = '';  // Limpiar el contenedor

        purchases.forEach(purchase => {
            const row = document.createElement('tr');  // Crear una fila de la tabla

            // Convertir la fecha de compra a formato legible
            const purchaseDate = convertToLocalTime(purchase.purchase_date);

            // Agregar celdas para cada columna de la tabla
            row.innerHTML = `
                <td>${purchase.ingredient_name}</td>
                <td>${purchase.quantity}</td>
                <td>${purchase.origin}</td>
                <td>${purchaseDate}</td>
            `;

            container.appendChild(row);  // Añadir la fila a la tabla
        });
    } catch (error) {
        console.error(error);
        alert("No se pudieron cargar las compras");
    }
}

// Llamar la función para cargar el historial de compras al iniciar la página
displayPurchases();
