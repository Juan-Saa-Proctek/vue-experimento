import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { mockAlarms } from '../mock/alarms.mock.js'

export const useAlarmsStore = defineStore('alarms', () => {
  const alarms = ref([...mockAlarms])
  const systemOnline = ref(true)
  const loading = ref(false)
  const error = ref(null)

  const activeCount = computed(() =>
    alarms.value.filter(a => a.active).length
  )

  function addAlarm(alarm) {
    alarms.value.unshift({ ...alarm, id: Date.now(), active: true })
  }

  function resolveAlarm(id) {
    const alarm = alarms.value.find(a => a.id === id)
    if (alarm) alarm.active = false
  }

  function setSystemOnline(status) {
    systemOnline.value = status
  }

  async function fetchAlarms() {
    loading.value = true
    error.value = null
    try {
      // TODO: reemplazar por llamada real
      // const data = await api.getAlarms()
      // alarms.value = data
      alarms.value = [...mockAlarms]
    } catch (e) {
      error.value = 'No se pudieron cargar las alarmas'
    } finally {
      loading.value = false
    }
  }

  return { alarms, systemOnline, activeCount, loading, error, addAlarm, resolveAlarm, setSystemOnline, fetchAlarms }
})