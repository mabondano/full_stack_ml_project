<template>
  <div class="signal-processor">
    <header>
      <nav>
        <ul>
          <li @click="handleMenuClick('file')">File</li>
          <li @click="handleMenuClick('edit')">Edit</li>
          <li @click="handleMenuClick('display')">Display</li>
          <li @click="handleMenuClick('data')">Data</li>
          <li @click="handleMenuClick('signalInput')">Signal Input</li>
          <li @click="handleMenuClick('rpnStack')">RPN Stack</li>
          <li @click="handleMenuClick('signalProcessing')">Signal Processing</li>
          <li @click="handleMenuClick('preferences')">Preferences</li>
          <li @click="handleMenuClick('help')">Help</li>
        </ul>
      </nav>
    </header>
    
    <div class="content">
      <!-- Sidebar for Signal Processing Options -->
      <aside v-if="activeMenu === 'signalProcessing'" class="sidebar">
        <h3>Signal Processing Options</h3>
        <ul>
          <li @click="handleSubMenuClick('signalGeneration')">Signal Generation</li>
          <li @click="handleSubMenuClick('digitalFiltering')">Digital Filtering</li>
          <li @click="handleSubMenuClick('frequencyAnalysis')">Frequency Analysis</li>
          <li @click="handleSubMenuClick('smoothingWindows')">Smoothing Windows</li>
          <li @click="handleSubMenuClick('distortionMeasurements')">Distortion Measurements</li>
          <li @click="handleSubMenuClick('dcRmsMeasurements')">DC/RMS Measurements</li>
          <li @click="handleSubMenuClick('limitTesting')">Limit Testing</li>
          <li @click="handleSubMenuClick('curveFitting')">Curve Fitting</li>
          <li @click="handleSubMenuClick('interpolation')">Interpolation</li>
          <li @click="handleSubMenuClick('probabilityStatistics')">Probability and Statistics</li>
          <li @click="handleSubMenuClick('linearAlgebra')">Linear Algebra</li>
          <li @click="handleSubMenuClick('optimization')">Optimization</li>
          <li @click="handleSubMenuClick('polynomials')">Polynomials</li>
        </ul>
      </aside>
      
      <!-- Main Content -->
      <main>
        <div v-if="activeMenu === 'signalInput'" class="signal-input">
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
          <SignalGenerator />
        </div>
        
        <div v-if="activeSubMenu === 'signalGeneration'">
          <SignalGenerator />
        </div>
      </main>
    </div>
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
      savedSignals: [],
      selectedSignal: "",
      fftResult: null,
      activeMenu: 'signalInput',
      activeSubMenu: null,
    };
  },
  methods: {
    handleMenuClick(menu) {
      this.activeMenu = menu;
      this.activeSubMenu = null;
    },
    handleSubMenuClick(subMenu) {
      this.activeSubMenu = subMenu;
    },
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
      if (this.selectedSignal) {
        alert(`Cargando la señal: ${this.selectedSignal}`);
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
header nav ul {
  list-style: none;
  display: flex;
  background-color: #333;
  padding: 10px;
  border-radius: 10px;
  justify-content: flex-start;
}

header nav ul li {
  margin: 0 15px;
  color: #fff;
  cursor: pointer;
}

header nav ul li:hover {
  text-decoration: underline;
}

.content {
  display: flex;
  align-items: flex-start;
}

.sidebar {
  width: 200px;
  background-color: #2d2d2d;
  padding: 20px;
  border-radius: 15px;
  margin-right: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.7);
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar ul li {
  margin-bottom: 10px;
  color: #ccc;
  cursor: pointer;
}

.sidebar ul li:hover {
  color: #fff;
}

main {
  flex: 1;
}

.signal-input, .signal-processing {
  margin: 20px;
  padding: 20px;
  border: 1px solid #444;
  border-radius: 15px;
  background-color: #2d2d2d;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.7);
}

button {
  margin: 10px;
  padding: 10px 20px;
  background-color: #ff5500;
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #e04e00;
}
</style>
