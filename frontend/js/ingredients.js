import { fetchIngredients } from './api.js';  // Importa la función de api.js

async function displayIngredients() {
    try {
        const ingredients = await fetchIngredients();
        const container = document.getElementById('ingredients-container');
        container.innerHTML = '';  // Limpiar el contenedor

        ingredients.forEach(ingredient => {
            const row = document.createElement('tr');  // Crear una fila de la tabla

            // Agregar celdas para cada columna de la tabla
            row.innerHTML = `
                <td>${ingredient.name}</td>
                <td>${ingredient.quantity}</td>
            `;

            container.appendChild(row);  // Añadir la fila a la tabla
        });
    } catch (error) {
        console.error(error);
        alert("No se pudieron cargar los ingredientes");
    }
}

// Llamar la función para cargar los ingredientes al iniciar la página
displayIngredients();
