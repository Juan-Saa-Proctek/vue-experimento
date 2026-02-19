import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ECharts from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart,GaugeChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DataZoomComponent,
  VisualMapComponent
} from 'echarts/components'

import App from './App.vue'
import router from './router/index.js'
import './assets/main.css'

// Registrar módulos de ECharts
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  GaugeChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DataZoomComponent,
  VisualMapComponent 
])

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.component('v-chart', ECharts)

app.mount('#app')