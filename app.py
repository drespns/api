from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///./productos.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy para la tabla Productos
class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    categoria = Column(String, index=True)
    precio_costo = Column(Float)
    precio_venta = Column(Float)
    proveedor = Column(String)
    fecha_lanzamiento = Column(String)  # Usamos string para simplificar

# Crear las tablas (si no existen)
Base.metadata.create_all(bind=engine)

# Inicialización de la aplicación FastAPI
app = FastAPI(title="API de Productos - TecnoMarket")

# Esquema Pydantic para la validación y respuesta
class ProductoSchema(BaseModel):
    id: int
    nombre: str
    categoria: str
    precio_costo: float
    precio_venta: float
    proveedor: str
    fecha_lanzamiento: str

    class Config:
        orm_mode = True

# Endpoint para obtener la lista de productos
@app.get("/productos/", response_model=List[ProductoSchema])
def read_productos():
    db = SessionLocal()
    productos = db.query(Producto).all()
    db.close()
    return productos

# Endpoint para obtener un producto por ID
@app.get("/productos/{producto_id}", response_model=ProductoSchema)
def read_producto(producto_id: int):
    db = SessionLocal()
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    db.close()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Endpoint para crear un nuevo producto
@app.post("/productos/", response_model=ProductoSchema)
def create_producto(producto: ProductoSchema):
    db = SessionLocal()
    db_producto = Producto(
        id=producto.id,
        nombre=producto.nombre,
        categoria=producto.categoria,
        precio_costo=producto.precio_costo,
        precio_venta=producto.precio_venta,
        proveedor=producto.proveedor,
        fecha_lanzamiento=producto.fecha_lanzamiento
    )
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    db.close()
    return db_producto
# 