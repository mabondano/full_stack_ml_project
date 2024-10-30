<template>
  <div class="signal-input">
    <h2>Signal Processor</h2>
    <textarea v-model="signalData" placeholder="Enter your signal data here (comma-separated)"></textarea>
    <br />
    <button @click="saveSignal">Save Signal</button>
    <button @click="loadSignal">Load Signal</button>
    <button @click="calculateFFT">Calculate FFT</button>
    <br />
    <label for="savedSignals">Choose a saved signal:</label>
    <select v-model="selectedSignal" @change="loadSelectedSignal" id="savedSignals">
      <option v-for="(file, index) in savedSignals" :key="index" :value="file">{{ file }}</option>
    </select>
    <br />
    <div v-if="fftResult">
      <h3>FFT Result:</h3>
      <FFTChart :fftData="fftResult" />
    </div>
    <button @click="showSignalGenerator = !showSignalGenerator">
      {{ showSignalGenerator ? 'Hide Signal Generator' : 'Show Signal Generator' }}
    </button>
    <SignalGenerator v-if="showSignalGenerator" />

  </div>
</template>


<script>
import FFTChart from './FFTChart.vue';
import SignalGenerator from './SignalGenerator.vue';

export default {
  components: {
    FFTChart,
    SignalGenerator
  },
  data() {
    return {
      signalData: "",
      savedSignals: [],  // Lista de señales guardadas
      selectedSignal: "", // Señal seleccionada del dropdown
      fftResult: null,
      showSignalGenerator: false      
    };
  },
  created() {
    // Cargar señales guardadas desde localStorage cuando se inicie el componente
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key.startsWith("signal_")) {
        this.savedSignals.push(key);
      }
    }
  },  
  methods: {
    async saveSignal() {
      if (this.signalData) {
        const data = this.signalData.split(",").map(Number);
        const fileName = `signal_${new Date().toISOString().replace(/:/g, "-")}.csv`;

        // Guardar datos en formato CSV
        const csvContent = data.join(",");
        const blob = new Blob([csvContent], { type: "text/csv" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = fileName;
        link.click();

        // Agregar el archivo a la lista de señales guardadas
        this.savedSignals.push(fileName);

        // Guardar también la señal en localStorage
        localStorage.setItem(fileName, this.signalData);

        // Mostrar mensaje de éxito con el nombre del archivo
        alert(`Señal guardada exitosamente como: ${fileName}`);
      } else {
        alert("No hay datos de señal para guardar.");
      }
    },
    async loadSignal() {
      const input = document.createElement("input");
      input.type = "file";
      input.accept = ".csv";

      input.onchange = async (event) => {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            try {
              // Leer los datos del CSV y actualizar el modelo signalData
              this.signalData = e.target.result;
              alert(`Señal cargada exitosamente desde: ${file.name}`);
            } catch (error) {
              alert("Error al cargar el archivo. Asegúrate de que sea un archivo CSV válido.");
            }
          };
          reader.readAsText(file);
        }
      };

      input.click();
    },
    loadSelectedSignal() {
      // Método para cargar la señal seleccionada de la lista desplegable
      if (this.selectedSignal) {
        const savedData = localStorage.getItem(this.selectedSignal);
        if (savedData) {
          this.signalData = savedData;
          alert(`Señal cargada exitosamente desde: ${this.selectedSignal}`);
        } else {
          alert("No se encontró la señal seleccionada en el almacenamiento.");
        }
      }
    },

    async calculateFFT() {
      const data = this.signalData.split(",").map(Number);
      try {
        const response = await fetch("http://127.0.0.1:9090/fft", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ data }),
        });
        const result = await response.json();
        this.fftResult = result.fft;
      } catch (error) {
        console.error("Error while calculating FFT:", error);
      }
    },
  },
};
</script>


<style scoped>
.signal-input {
  margin: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
}
textarea {
  width: 100%;
  height: 100px;
  margin-bottom: 10px;
}
button {
  margin-top: 10px;
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
</style>
