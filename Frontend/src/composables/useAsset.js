import { computed, onMounted } from 'vue'
import { useAssetsStore } from '../stores/assetsStore.js'
import { useAlarmsStore } from '../stores/alarmsStore.js'

export function useAsset(assetId) {
  const assetsStore = useAssetsStore()
  const alarmsStore = useAlarmsStore()

  const asset = computed(() =>
    assetsStore.assets.find(a => a.id === Number(assetId))
  )

  const assetAlarms = computed(() =>
    alarmsStore.alarms.filter(a => a.assetId === Number(assetId))
  )

  const rmsPercentage = computed(() => {
    if (!asset.value) return 0
    return Math.min((asset.value.rmsActual / asset.value.rmsLimit) * 100, 100)
  })

  const statusColor = computed(() => {
    const colors = {
      normal:   'var(--color-normal)',
      warning:  'var(--color-warning)',
      critical: 'var(--color-critical)',
      offline:  'var(--color-offline)'
    }
    return colors[asset.value?.status] || colors.offline
  })

  function formatDate(iso) {
    if (!iso) return '—'
    return new Date(iso).toLocaleString('es-CO', {
      day: '2-digit', month: '2-digit', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    })
  }

  onMounted(async () => {
    if (assetsStore.assets.length === 0) await assetsStore.fetchAssets()
    await alarmsStore.fetchAlarms()
  })

  return { asset, assetAlarms, rmsPercentage, statusColor, formatDate }
}