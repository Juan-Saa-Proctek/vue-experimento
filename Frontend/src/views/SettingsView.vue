<template>
  <div class="settings-view">
    <ConnectionSection />
    <ProtocolsSection />
    <ThresholdsSection />
    <AssetsSection />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAlarmsStore } from '../stores/alarmsStore.js'
import ConnectionSection from '../components/settings/ConnectionSection.vue'
import ProtocolsSection  from '../components/settings/ProtocolsSection.vue'
import ThresholdsSection from '../components/settings/ThresholdsSection.vue'
import AssetsSection     from '../components/settings/AssetsSection.vue'

const alarmsStore = useAlarmsStore()
onMounted(() => {
  alarmsStore.fetchAlarms(true) 
})
</script>

<style scoped>
.settings-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>