from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import csv
import os

app = FastAPI(title="API de Empleados - TecnoMarket")

# Modelo Pydantic para la validación y respuesta
class EmpleadoSchema(BaseModel):
    EmpleadoID: int
    Nombre: str
    Apellido: str
    Puesto: str
    FechaContratacion: str
    TiendaID: int
    Salario: float
    HorasFormacion: int

# Lista en memoria para almacenar los empleados
empleados_data: List[EmpleadoSchema] = []

# Cargar los datos desde Empleados.csv al iniciar la app
@app.on_event("startup")
def load_empleados():
    csv_path = os.path.join("datos", "Empleados.csv")  # Ajusta la ruta si es distinta
    if not os.path.exists(csv_path):
        print(f"Archivo {csv_path} no encontrado. La lista de empleados estará vacía.")
        return

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            empleado = EmpleadoSchema(
                EmpleadoID=int(row["EmpleadoID"]),
                Nombre=row["Nombre"],
                Apellido=row["Apellido"],
                Puesto=row["Puesto"],
                FechaContratacion=row["FechaContratacion"],
                TiendaID=int(row["TiendaID"]),
                Salario=float(row["Salario"]),
                HorasFormacion=int(row["HorasFormacion"])
            )
            empleados_data.append(empleado)

    print(f"Se han cargado {len(empleados_data)} empleados desde {csv_path}.")

# Endpoint para obtener la lista de empleados
@app.get("/empleados/", response_model=List[EmpleadoSchema])
def get_empleados():
    return empleados_data

# Endpoint para obtener un empleado por ID
@app.get("/empleados/{empleado_id}", response_model=EmpleadoSchema)
def get_empleado(empleado_id: int):
    for emp in empleados_data:
        if emp.EmpleadoID == empleado_id:
            return emp
    raise HTTPException(status_code=404, detail="Empleado no encontrado")

# Endpoint para crear un nuevo empleado (opcional)
@app.post("/empleados/", response_model=EmpleadoSchema)
def create_empleado(empleado: EmpleadoSchema):
    # En este ejemplo, simplemente lo añadimos a la lista en memoria
    empleados_data.append(empleado)
    return empleado
# 