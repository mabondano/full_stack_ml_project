from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

import csv
from typing import List
import os

app = FastAPI()

# Configurar CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Puedes especificar la URL del frontend aquí
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Signal(BaseModel):
    data: list

@app.post("/fft")
async def calculate_fft(signal: Signal):
    try:
        data_array = np.array(signal.data)
        fft_result = np.fft.fft(data_array)
        # Convertir los números complejos a una representación JSON-friendly
        fft_serializable = [{"real": val.real, "imag": val.imag} for val in fft_result]
        return {"fft": fft_serializable}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def read_root():
    return {"message": "Hello, Merly! FastAPI is working!"}


# Directorio para guardar las señales
SIGNAL_DIR = "saved_signals"

# Crear el directorio si no existe
os.makedirs(SIGNAL_DIR, exist_ok=True)

@app.post("/save_signal")
async def save_signal(signal_data: List[float]):
    try:
        file_path = os.path.join(SIGNAL_DIR, "signal_data.csv")
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(signal_data)
        return {"message": "Signal saved successfully!", "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving signal: {e}")

@app.get("/load_signal")
async def load_signal():
    try:
        file_path = os.path.join(SIGNAL_DIR, "signal_data.csv")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="No saved signal found.")

        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            signal_data = list(reader)[0]  # Solo hay una fila con los datos
            signal_data = [float(value) for value in signal_data]
        
        return {"signal_data": signal_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading signal: {e}")


