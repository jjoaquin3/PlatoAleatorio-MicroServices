from fastapi import APIRouter, HTTPException, Depends
from app.service.order_service import OrderService
from app.service.recipe_service import RecipeService
from app.model.schema.order import OrderSchema, OrderSchemaBuild, OrderUpdateStateRequest, OrderUpdateStepRequest, IngredientSchema
from app.security.auth import get_api_key
from pydantic import BaseModel
from typing import List
from app.model.order import Order

router = APIRouter()

@router.get("/orders", response_model=List[OrderSchema])
async def get_all_orders(
    api_key: str = Depends(get_api_key),  
    order_service: OrderService = Depends()  # Inyección del Servicio
):
    orders = await order_service.get_all_orders()
    if orders:
        return orders
    raise HTTPException(status_code=404, detail="No orders found")

@router.get("/orders/{order_number}", response_model=OrderSchema)
async def get_order_by_order(
    order_number: int,
    api_key: str = Depends(get_api_key),  
    order_service: OrderService = Depends()  # Inyección del Servicio
):
    order = await order_service.get_order_by_order(order_number)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order not found")


@router.put("/orders/step", response_model=dict)
#async def update_step(order_number: int, request: OrderUpdateStateRequest, api_key: str = Depends(get_api_key)):
async def update_step(
    request: OrderUpdateStepRequest,
    api_key: str = Depends(get_api_key),  
    order_service: OrderService = Depends()  # Inyección del Servicio
):
    print(">>> /orders/step (update_step) recibió:", request)
    #if order_service.update_step(request):
    #    return {"message": "Step updated successfully", "update": "ok"}
    #raise HTTPException(status_code=400, detail="Failed to update step")
    try:
        result = await order_service.update_step(request)
        if result:
            return {"message": "State updated successfully", "update": "ok"}
        else:
            raise HTTPException(status_code=400, detail="Failed to update state")
    except Exception as e:        
        print(f"Error al actualizar el estado de la orden: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/orders/state", response_model=dict)
#async def update_state(order_number: int, request: OrderUpdateStepRequest, api_key: str = Depends(get_api_key)):
async def update_state(
    request: OrderUpdateStateRequest,
    api_key: str = Depends(get_api_key),  
    order_service: OrderService = Depends()  # Inyección del Servicio
):
    print(">>> /orders/state (update_state) recibió:", request)
    #if order_service.update_state(request):
    #    return {"message": "State updated successfully", "update": "ok"}
    #raise HTTPException(status_code=400, detail="Failed to update state")
    try:
        result = await order_service.update_state(request)
        if result:
            return {"message": "State updated successfully", "update": "ok"}
        else:
            raise HTTPException(status_code=400, detail="Failed to update state")
    except Exception as e:        
        print(f"Error al actualizar el estado de la orden: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/orders", response_model=dict)
async def save_order(
    order_data: OrderSchema,  # Usando el modelo de Pydantic para validación
    api_key: str = Depends(get_api_key),
    order_service: OrderService = Depends()  # Inyección del Servicio
):
    # Llamada al servicio para guardar la orden
    print(">>> /orders (save order) recibió:", order_data)
    #if order_service.save_order(order_data.dict()): 
    #    return {"message": "Order saved successfully", "save": "ok"}    
    #raise HTTPException(status_code=400, detail="Failed to save order")
    try:
        # Llamada al servicio para guardar la orden
        result = await order_service.save_order(order_data)
        if result:
            return {"message": "Order saved successfully", "save": "ok"}
        else:
            raise HTTPException(status_code=400, detail="Failed to save order")
    except Exception as e:
        # Captura más detalles del error para devolverlos
        print(f"Error al guardar la orden: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/orders/build", response_model=OrderSchema) 
#async def build_order_recipe(order_data: OrderSchemaBuild, api_key: str = Depends(get_api_key)):
async def build_order_recipe(
    order_data: OrderSchemaBuild,
    api_key: str = Depends(get_api_key),  
    order_service: OrderService = Depends()  # Inyección del Servicio
):
    print(">>> /orders/build (build) recibió:", order_data)
    order = await order_service.build_order_recipe(order_data)
    if order:
        return order
    raise HTTPException(status_code=400, detail="Failed to build order with recipe")


@router.post("/orders/validate", response_model=dict)
#async def validate_ingredients(order_data: OrderSchema, api_key: str = Depends(get_api_key)):
async def validate_ingredients(
    order_data: OrderSchema,
    api_key: str = Depends(get_api_key),  
    order_service: OrderService = Depends()  # Inyección del Servicio
):
    if await order_service.validate_ingredients(order_data.dict()):
        return \
        {
            "message": "Ingredients validated successfully",
            "validate": "ok"
        }
    raise HTTPException(status_code=400, detail="Ingredient validation failed")


