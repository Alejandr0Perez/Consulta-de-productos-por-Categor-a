from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Conectar con MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.ShopiteszREST  # Conexión con la base de datos ShopiteszREST

# Modelo Pydantic para Producto
class Producto(BaseModel):
    _id: int
    nombre: str
    descripcion: str
    precio: float
    existencia: int
    marca: str
    color: str
    costoEnvio: float
    idCategoria: int
    estatus: str
    idVendedor: int

# Operación: Consulta de productos por Categoría
@app.get("/Productos/categoría/{idCategoria}", response_model=List[Producto])
async def consultar_productos_por_categoria(idCategoria: int):
    try:
        # Consultar productos por categoría desde la base de datos
        productos = await db.productos.find({"idCategoria": idCategoria}).to_list(length=None)
        if productos:
            # Formatear los resultados
            return productos
        else:
            raise HTTPException(status_code=404, detail="No se encontraron productos para esta categoría")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
