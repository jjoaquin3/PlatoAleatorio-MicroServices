import { fetchRecipes } from './api.js';  // Importa la función de api.js

async function displayRecipes() {
    try {
        const recipes = await fetchRecipes();
        const container = document.getElementById('recipes-container');
        container.innerHTML = '';  // Limpiar el contenedor

        recipes.forEach(recipe => {
            const row = document.createElement('tr');  // Crear una fila de la tabla

            // Crear el contenido de la celda para la receta
            const ingredientsList = recipe.ingredients.map(ingredient => `
                <li>${ingredient.name}: Quantity: ${ingredient.quantity}</li>
            `).join('');

            row.innerHTML = `
                <td>${recipe.recipe}</td>
                <td><ul>${ingredientsList}</ul></td>
            `;

            container.appendChild(row);  // Añadir la fila a la tabla
        });
    } catch (error) {
        console.error(error);
        alert("No se pudieron cargar las recetas");
    }
}

// Llamar la función para cargar las recetas al iniciar la página
displayRecipes();
