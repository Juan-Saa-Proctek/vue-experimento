import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { alarmsAPI } from '../services/api.js'

export const useAlarmsStore = defineStore('alarms', () => {
  const alarms       = ref([])
  const systemOnline = ref(true)
  const loading      = ref(false)
  const error        = ref(null)

  const activeCount = computed(() =>
    alarms.value.filter(a => a.active).length
  )

  async function fetchAlarms(activeOnly = false) {
    loading.value = true
    error.value   = null
    try {
      const data = await alarmsAPI.getAll(activeOnly)
      alarms.value = data.map(a => ({
        id:        a.id,
        assetId:   a.asset_id,
        assetTag:  a.asset_tag,
        assetName: a.asset_name,
        severity:  a.severity,
        message:   a.message,
        rmsValue:  a.rms_value,
        active:    a.active,
        timestamp: a.timestamp
      }))
    } catch (e) {
      error.value = e.message
      systemOnline.value = false

    } finally {
      loading.value = false
    }
  }

  async function resolveAlarm(alarmId) {
    try {
      await alarmsAPI.resolve(alarmId)
      await fetchAlarms()
    } catch (e) {
      error.value = e.message
    }
  }

  function setSystemOnline(status) {
    systemOnline.value = status
  }

  return { alarms, systemOnline, activeCount, loading, error, fetchAlarms, resolveAlarm, setSystemOnline }
})