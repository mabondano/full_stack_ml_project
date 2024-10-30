<template>
  <div ref="plotContainer" style="width: 100%; height: 400px;"></div>
</template>

<script>
import Plotly from 'plotly.js-dist';

export default {
  props: {
    fftData: {
      type: Array,
      required: true,
    },
  },
  mounted() {
    this.plotFFT();
  },
  watch: {
    fftData: 'plotFFT',
  },
  methods: {
    plotFFT() {
      // Calcular la magnitud de la FFT
      const magnitudeData = this.fftData.map(point => Math.sqrt(point.real ** 2 + point.imag ** 2));
      
      // Definir los bins de frecuencia
      const frequencyBins = Array.from({ length: this.fftData.length }, (_, i) => i);
      
      // Definir la traza del gráfico
      const trace = {
        x: frequencyBins,
        y: magnitudeData,
        type: 'scatter', // Tipo de gráfica: dispersión
        mode: 'lines', // Mostrar solo la línea continua sin marcadores
        line: {
          shape: 'spline', // Hacer la línea suave y continua
          color: '#007bff', // Color azul definido para la línea
          width: 2 // Grosor de la línea para darle visibilidad
        },
        name: 'FFT Magnitude' // Nombre de la serie
      };
      
      // Definir el layout del gráfico
      const layout = {
        title: 'FFT Result',
        xaxis: {
          title: 'Frequency Bin',
        },
        yaxis: {
          title: 'Magnitude',
        },
      };

      Plotly.newPlot(this.$refs.plotContainer, [trace], layout);
    },
  },
};
</script>

<style scoped>
#plotContainer {
  width: 100%;
  height: 400px;
}
</style>
