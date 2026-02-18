import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAlarmsStore = defineStore('alarms', () => {
  const alarms = ref([])
  const systemOnline = ref(true)

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

  return { alarms, systemOnline, activeCount, addAlarm, resolveAlarm, setSystemOnline }
})