<template>
    <div>
      <canvas id="fftChart"></canvas>
    </div>
  </template>
  
  <script>
  import { onMounted } from 'vue';
  import Chart from 'chart.js/auto';
  
  export default {
    name: 'FFTChart',
    props: {
      fftData: {
        type: Array,
        required: true
      }
    },
    setup(props) {
      onMounted(() => {
        const ctx = document.getElementById('fftChart').getContext('2d');
        
        // Crear gráfico de línea con los datos de la FFT
        new Chart(ctx, {
          type: 'line',
          data: {
            labels: props.fftData.map((_, index) => index),
            datasets: [
              {
                label: 'FFT Magnitude',
                data: props.fftData.map(point => Math.sqrt(point.real ** 2 + point.imag ** 2)),
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: false
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Frequency Bin'
                }
              },
              y: {
                title: {
                  display: true,
                  text: 'Magnitude'
                }
              }
            },
            plugins: {
              tooltip: {
                enabled: true,
                callbacks: {
                  label: function(tooltipItem) {
                    const { real, imag } = props.fftData[tooltipItem.dataIndex];
                    return `Real: ${real}, Imaginary: ${imag}`;
                  }
                }
              }
            }
          }
        });
      });
    }
  };
  </script>
  
  <style scoped>
  #fftChart {
    max-width: 600px;
    max-height: 400px;
  }
  </style>
  