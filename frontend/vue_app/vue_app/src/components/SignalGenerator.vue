<template>
    <div class="signal-generator">
      <h2>Generador de Señales</h2>
      <label for="signalType">Selecciona el Tipo de Señal:</label>
      <select v-model="selectedSignalType" id="signalType">
        <option value="sin">Onda Sinusoidal</option>
        <option value="square">Onda Cuadrada</option>
        <option value="triangle">Onda Triangular</option>
        <option value="delta">Delta de Dirac</option>
        <option value="step">Escalón Unitario</option>
      </select>
  
      <div class="parameters">
        <label for="numSamples">Número de Muestras (n):</label>
        <input type="number" v-model="numSamples" id="numSamples" />
  
        <label for="period">Periodo (T):</label>
        <input type="number" v-model="period" id="period" />
  
        <label for="phaseShift">Desfase:</label>
        <input type="number" v-model="phaseShift" id="phaseShift" />
  
        <label for="domain">Dominio:</label>
        <select v-model="selectedDomain" id="domain">
          <option value="temporal">Temporal</option>
          <option value="frecuencia">Frecuencia</option>
        </select>
      </div>
  
      <button @click="generateSignal">Generar Señal</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        selectedSignalType: "sin",
        numSamples: 128,
        period: 1,
        phaseShift: 0,
        selectedDomain: "temporal",
      };
    },
    methods: {
      generateSignal() {
        // Aquí implementaríamos la lógica para generar la señal con los parámetros definidos
        console.log("Generando señal:", {
          tipo: this.selectedSignalType,
          muestras: this.numSamples,
          periodo: this.period,
          desfase: this.phaseShift,
          dominio: this.selectedDomain,
        });
      },
    },
  };
  </script>
  
  <style scoped>
  /*
  .signal-generator {
    margin: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background-color: #f9f9f9;
  }
  
  .parameters {
    margin-top: 10px;
  }
  
  button {
    margin-top: 15px;
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
    */
  </style>
  