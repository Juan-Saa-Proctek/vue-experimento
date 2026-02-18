import { ref, onMounted, onUnmounted } from 'vue'

export function useRealtime(callback, interval = 2000) {
  const isRunning = ref(false)
  let timer = null

  function start() {
    if (isRunning.value) return
    isRunning.value = true
    timer = setInterval(callback, interval)
  }

  function stop() {
    isRunning.value = false
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  onMounted(() => start())
  onUnmounted(() => stop())

  return { isRunning, start, stop }
}