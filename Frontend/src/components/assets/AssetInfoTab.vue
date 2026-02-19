<template>
  <div class="info-grid">
    <div class="info-card">
      <h3>Datos de Placa</h3>
      <div class="info-rows">
        <AssetInfoRow label="Tag"         :value="asset.tag" />
        <AssetInfoRow label="Nombre"      :value="asset.name" />
        <AssetInfoRow label="Tipo"        :value="asset.type" />
        <AssetInfoRow label="Ubicación"   :value="asset.location" />
        <AssetInfoRow label="RPM Nominal" :value="`${asset.rpmNominal} RPM`" />
        <AssetInfoRow label="Límite RMS"  :value="`${asset.rmsLimit} mm/s`" />
      </div>
    </div>

    <div class="info-card">
      <h3>Estado Actual</h3>
      <div class="info-rows">
        <AssetInfoRow
          label="RMS Actual"
          :value="`${asset.rmsActual.toFixed(2)} mm/s`"
          :highlight="asset.status"
        />
        <AssetInfoRow
          label="% del Límite"
          :value="`${rmsPercentage.toFixed(1)}%`"
          :highlight="asset.status"
        />
        <AssetInfoRow
          label="Última actualización"
          :value="formatDate(asset.lastUpdate)"
        />
      </div>
      <div class="status-row">
        <span class="info-label">Estado</span>
        <StatusBadge :status="asset.status" />
      </div>
    </div>
  </div>
</template>

<script setup>
import AssetInfoRow from './AssetInfoRow.vue'
import StatusBadge from '../common/StatusBadge.vue'

defineProps({
  asset:         { type: Object,   required: true },
  rmsPercentage: { type: Number,   required: true },
  formatDate:    { type: Function, required: true }
})
</script>

<style scoped>
.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.info-card {
  background-color: var(--color-surface4);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--color-surface);
}

.info-card h3 {
  color: var(--color-text-dark);
  font-size: 15px;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--color-surface4);
}

.info-rows {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
}

.status-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  border-radius: 8px;
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  transition: background 0.2s;
}

.status-row:hover {
  background-color: var(--color-surface3);
}

.info-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-dark);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
</style>