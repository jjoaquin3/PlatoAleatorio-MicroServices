// lunch.js
import { requestLunch } from './api.js';  // Importa la función de api.js

document.getElementById('request-lunch-button').addEventListener('click', async () => {
    const orderId = 0;  // El order ID está predefinido como 0 en este caso

    try {
        console.log("A")
        // Llamar a la API para solicitar el platillo
        const lunchData = await requestLunch(orderId);
        console.log("B")
        // Mostrar la respuesta en la interfaz
        document.getElementById('lunch-order').textContent = lunchData.order;        
        document.getElementById('lunch-recipe').textContent = lunchData.recipe;        
        document.getElementById('lunch-message').textContent = lunchData.message;
        document.getElementById('lunch-response').style.display = 'block';  // Mostrar los detalles de la orden

    } catch (error) {
        console.error(error);
        alert('No se pudo obtener el platillo');
    }
});
