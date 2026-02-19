<template>
  <div class="settings-view">
    <ConnectionSection />
    <ProtocolsSection />
    <ThresholdsSection />
    <AssetsSection />
  </div>
</template>

<script setup>
import ConnectionSection from '../components/settings/ConnectionSection.vue'
import ProtocolsSection  from '../components/settings/ProtocolsSection.vue'
import ThresholdsSection from '../components/settings/ThresholdsSection.vue'
import AssetsSection     from '../components/settings/AssetsSection.vue'
</script>

<style scoped>
.settings-view {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>