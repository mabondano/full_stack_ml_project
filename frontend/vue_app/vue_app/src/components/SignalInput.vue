<template>
  <div class="signal-input">
    <h2>Signal Processor</h2>
    <textarea v-model="signalData" placeholder="Enter your signal data (comma-separated)"></textarea>
    <button @click="saveSignal">Save Signal</button>
    <button @click="loadSignal">Load Signal</button>
    <button @click="calculateFFT">Calculate FFT</button>
    <div v-if="fftResult">
      <h3>FFT Result:</h3>
      <FFTChart :fftData="fftResult" />
    </div>
  </div>
</template>

<script>
import FFTChart from './FFTChart.vue';

export default {
  components: {
    FFTChart
  },
  data() {
    return {
      signalData: "",
      fftResult: null
    };
  },
  methods: {
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

    async saveSignal_old() {
      if (this.signalData) {
        const data = this.signalData.split(",").map(Number);
        try {
          await fetch("http://127.0.0.1:9090/save_signal", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          });
          alert("Signal saved successfully!");
        } catch (error) {
          console.error("Error while saving the signal:", error);
        }
      } else {
        alert("No signal data to save.");
      }
    },   
    async saveSignal() {
      if (this.signalData) {
        const data = this.signalData.split(",").map(Number);
        const fileName = `signal_${new Date().toISOString().replace(/:/g, "-")}.csv`;

        // Convertir datos a formato CSV
        const csvContent = data.join(",");
        const blob = new Blob([csvContent], { type: "text/csv" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = fileName;
        link.click();

        // Mostrar mensaje de éxito con el nombre del archivo
        alert(`Señal guardada exitosamente como: ${fileName}`);
      } else {
        alert("No hay datos de señal para guardar.");
      }
    },    

    async loadSignal_old() {
      try {
        const response = await fetch("http://127.0.0.1:9090/load_signal");
        const result = await response.json();
        this.signalData = result.signal_data.join(",");
        alert("Signal loaded successfully!");
      } catch (error) {
        console.error("Error while loading the signal:", error);
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
              // Leer los datos del CSV y actualizar signalData
              this.signalData = e.target.result;
              alert(`Señal cargada exitosamente desde: ${file.name}`);
            } catch (error) {
              alert("Error al cargar el archivo. Asegúrate de que sea un archivo de señal válido en formato CSV.");
            }
          };
          reader.readAsText(file);
        }
      };

      input.click();
    }

  }
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

