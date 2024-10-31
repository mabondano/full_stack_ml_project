from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import csv
from typing import List
import os

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64
from fastapi.responses import JSONResponse
from scipy import signal
from numpy import arange, pi, sinc, log10



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
    

# Nueva funcionalidad: Calcular la FFT y generar una gráfica
@app.get("/calculate_fft")
async def calculate_fft_graph(
    wc: float = Query(pi/4, description="Cut-off frequency in radians (default is pi/4)"),
    M: int = Query(20, description="Filter length parameter (default is 20)")
):
    try:
        # Calculation Parameters
        N = 512  # DFT size
        n = arange(-M, M)
        h = wc / pi * sinc(wc * (n) / pi)  # Filter coefficients

        # Frequency Response
        w, Hh = signal.freqz(h, 1, whole=True, worN=N)
        
        # Plotting the results
        fig, axs = plt.subplots(3, 1)
        fig.set_size_inches((8, 8))
        plt.subplots_adjust(hspace=0.3)
        
        # Plotting the filter coefficients
        ax = axs[0]
        ax.stem(n + M, h, basefmt='b-')
        ax.set_xlabel("$n$", fontsize=22)
        ax.set_ylabel("$h_n$", fontsize=22)

        # Plotting the magnitude response
        ax = axs[1]
        ax.plot(w - pi, abs(np.fft.fftshift(Hh)))
        ax.axis(xmax=pi / 2, xmin=-pi / 2)
        ax.vlines([-wc, wc], 0, 1.2, color='g', lw=2., linestyle='--')
        ax.hlines(1, -pi, pi, color='g', lw=2., linestyle='--')
        ax.set_xlabel(r"$\omega$", fontsize=22)
        ax.set_ylabel(r"$|H(\omega)| $", fontsize=22)

        # Plotting the log-magnitude response
        ax = axs[2]
        ax.plot(w - pi, 20 * log10(abs(np.fft.fftshift(Hh))))
        ax.axis(ymin=-40, xmax=pi / 2, xmin=-pi / 2)
        ax.vlines([-wc, wc], 10, -40, color='g', lw=2., linestyle='--')
        ax.hlines(0, -pi, pi, color='g', lw=2., linestyle='--')
        ax.set_xlabel(r"$\omega$", fontsize=22)
        ax.set_ylabel(r"$20\log_{10}|H(\omega)| $", fontsize=18)

        # Save plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)
        
        # Encode the plot as base64
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        # Return as JSON
        return JSONResponse(content={"image": image_base64})

    except Exception as e:
        return {"error": str(e)}



