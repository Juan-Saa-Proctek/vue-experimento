<template>
  <div class="settings-section">
    <h3 class="section-title">Configuración de Protocolos</h3>

    <LoadingSpinner v-if="loading" message="Cargando configuración..." />
    <ErrorState v-else-if="error" :message="error" retryable @retry="fetchProtocols" />

    <template v-else>
      <!-- MQTT -->
      <div class="protocol-card">
        <div class="protocol-header">
          <div class="protocol-title">
            <span class="protocol-icon"><SatelliteDish size="20" /></span>
            <span>MQTT</span>
            <span class="protocol-badge" :class="config.mqtt_enabled ? 'active' : 'inactive'">
              {{ config.mqtt_enabled ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
          <label class="toggle">
            <input type="checkbox" v-model="config.mqtt_enabled" />
            <span class="toggle-slider"></span>
          </label>
        </div>
        <div class="protocol-fields" v-if="config.mqtt_enabled">
          <div class="field-row">
            <div class="field-group">
              <label>Host</label>
              <input v-model="config.mqtt_host" class="field-input" placeholder="192.168.1.100" />
            </div>
            <div class="field-group small">
              <label>Puerto</label>
              <input v-model.number="config.mqtt_port" type="number" class="field-input" />
            </div>
          </div>
          <div class="field-row">
            <div class="field-group">
              <label>Usuario (opcional)</label>
              <input v-model="config.mqtt_user" class="field-input" placeholder="usuario" />
            </div>
            <div class="field-group">
              <label>Contraseña (opcional)</label>
              <input v-model="config.mqtt_password" type="password" class="field-input" placeholder="••••••" />
            </div>
          </div>
          <div class="topic-info">
            <span class="topic-label">Tópico esperado:</span>
            <code>vibmonitor/assets/{asset_id}/reading</code>
          </div>
        </div>
      </div>

      <!-- Serial -->
      <div class="protocol-card">
        <div class="protocol-header">
          <div class="protocol-title">
            <span class="protocol-icon"><Cable size="20" /></span>
            <span>Serial / UART</span>
            <span class="protocol-badge" :class="config.serial_enabled ? 'active' : 'inactive'">
              {{ config.serial_enabled ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
          <label class="toggle">
            <input type="checkbox" v-model="config.serial_enabled" />
            <span class="toggle-slider"></span>
          </label>
        </div>
        <div class="protocol-fields" v-if="config.serial_enabled">
          <div class="field-row">
            <div class="field-group">
              <label>Puerto</label>
              <input v-model="config.serial_port" class="field-input" placeholder="/dev/ttyUSB0 o COM3" />
            </div>
            <div class="field-group small">
              <label>Baudrate</label>
              <select v-model.number="config.serial_baudrate" class="field-input">
                <option :value="9600">9600</option>
                <option :value="19200">19200</option>
                <option :value="38400">38400</option>
                <option :value="115200">115200</option>
              </select>
            </div>
          </div>
          <div class="topic-info">
            <span class="topic-label">Formato esperado:</span>
            <code>{"asset_id": 1, "rms": 2.5}</code>
          </div>
        </div>
      </div>

      <!-- Modbus -->
      <div class="protocol-card">
        <div class="protocol-header">
          <div class="protocol-title">
            <span class="protocol-icon"><EthernetPort size="20" /></span>
            <span>Modbus TCP/RTU</span>
            <span class="protocol-badge" :class="config.modbus_enabled ? 'active' : 'inactive'">
              {{ config.modbus_enabled ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
          <label class="toggle">
            <input type="checkbox" v-model="config.modbus_enabled" />
            <span class="toggle-slider"></span>
          </label>
        </div>
        <div class="protocol-fields" v-if="config.modbus_enabled">
          <div class="field-row">
            <div class="field-group">
              <label>Host TCP</label>
              <input v-model="config.modbus_host" class="field-input" placeholder="192.168.1.200" />
            </div>
            <div class="field-group small">
              <label>Puerto</label>
              <input v-model.number="config.modbus_port" type="number" class="field-input" />
            </div>
          </div>
        </div>
      </div>

      <!-- PCH Engineering -->
      <div class="protocol-card">
        <div class="protocol-header">
          <div class="protocol-title">
            <span class="protocol-icon"><Server size="20" /></span>
            <span>PCH Engineering</span>
            <span class="protocol-badge" :class="config.pch_enabled ? 'active' : 'inactive'">
              {{ config.pch_enabled ? 'Activo' : 'Inactivo' }}
            </span>
          </div>
          <label class="toggle">
            <input type="checkbox" v-model="config.pch_enabled" />
            <span class="toggle-slider"></span>
          </label>
        </div>
        <div class="protocol-fields" v-if="config.pch_enabled">
          <div class="field-row">
            <div class="field-group small">
              <label>Servidor</label>
              <select v-model="config.pch_host" class="field-input">
                <option value="pchcloud">PCH Cloud</option>
                <option value="local">Local</option>
                <option value="demo">Demo</option>
              </select>
            </div>
            <div class="field-group small">
              <label>Intervalo (minutos)</label>
              <select v-model.number="config.pch_interval_minutes" class="field-input">
                <option :value="15">15 min</option>
                <option :value="30">30 min</option>
                <option :value="60">1 hora</option>
                <option :value="120">2 horas</option>
                <option :value="240">4 horas</option>
              </select>
            </div>
          </div>
          <div class="field-row">
            <div class="field-group">
              <label>Usuario</label>
              <input v-model="config.pch_user" class="field-input" placeholder="usuario PCH" />
            </div>
            <div class="field-group">
              <label>Contraseña</label>
              <input v-model="config.pch_password" type="password" class="field-input" placeholder="••••••" />
            </div>
          </div>
          <div class="topic-info">
            <span class="topic-label">Consulta la última grabación de cada activo PCH cada</span>
            <code>{{ config.pch_interval_minutes }} min</code>
          </div>
        </div>
      </div>

      <div class="actions">
        <span v-if="saved" class="saved-msg"><CircleCheckBig size="16" class="saved-icon" /> Configuración guardada.</span>
        <button class="save-btn" @click="saveProtocols" :disabled="saving">
          {{ saving ? 'Guardando...' : 'Guardar configuración' }}
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { settingsAPI } from '../../services/api.js'
import LoadingSpinner from '../common/LoadingSpinner.vue'
import ErrorState from '../common/ErrorState.vue'
import { SatelliteDish, Cable, EthernetPort, CircleCheckBig, Server } from 'lucide-vue-next'

const loading = ref(false)
const saving  = ref(false)
const saved   = ref(false)
const error   = ref(null)

const config = ref({
  mqtt_enabled:         false,
  mqtt_host:            '',
  mqtt_port:            1883,
  mqtt_user:            '',
  mqtt_password:        '',
  serial_enabled:       false,
  serial_port:          '',
  serial_baudrate:      115200,
  modbus_enabled:       false,
  modbus_host:          '',
  modbus_port:          502,
  pch_enabled:          false,
  pch_host:             'pchcloud',
  pch_user:             '',
  pch_password:         '',
  pch_interval_minutes: 60,
})

async function fetchProtocols() {
  loading.value = true
  error.value   = null
  try {
    config.value = await settingsAPI.getProtocols()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function saveProtocols() {
  saving.value = true
  saved.value  = false
  try {
    await settingsAPI.updateProtocols(config.value)
    saved.value = true
    setTimeout(() => saved.value = false, 5000)
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}

onMounted(() => fetchProtocols())
</script>

<style scoped>
.settings-section {
  background-color: var(--color-surface4);
  border-radius: 12px;
  padding: 24px;
  border: 1px solid var(--color-surface);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-title {
  color: var(--color-text-dark);
  font-size: 15px;
  font-weight: 600;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-surface2);
}

.protocol-card {
  background-color: var(--color-surface3);
  border-radius: 10px;
  padding: 16px 20px;
  border: 1px solid var(--color-surface);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.protocol-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.protocol-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-dark);
}

.protocol-icon {
  display: flex;
  align-items: center;
  gap: 6px;
}

.protocol-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 10px;
  border-radius: 10px;
}

.protocol-badge.active {
  background-color: rgba(0,200,81,0.15);
  color: var(--color-normal);
}

.protocol-badge.inactive {
  background-color: rgba(158,158,158,0.15);
  color: var(--color-offline);
}

.toggle {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
  cursor: pointer;
}

.toggle input { opacity: 0; width: 0; height: 0; }

.toggle-slider {
  position: absolute;
  inset: 0;
  background-color: var(--color-surface2);
  border-radius: 24px;
  transition: 0.3s;
}

.toggle-slider::before {
  content: "";
  position: absolute;
  width: 18px;
  height: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: 0.3s;
}

.toggle input:checked + .toggle-slider { background-color: var(--color-normal); }
.toggle input:checked + .toggle-slider::before { transform: translateX(20px); }

.protocol-fields {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-top: 8px;
  border-top: 1px solid var(--color-surface2);
}

.field-row {
  display: flex;
  gap: 12px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.field-group.small { max-width: 160px; }

.field-group label {
  font-size: 11px;
  color: var(--color-text-muted);
  text-transform: uppercase;
}

.field-input {
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 6px;
  padding: 8px 12px;
  color: var(--color-text-dark);
  font-size: 13px;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
  box-sizing: border-box;
}

.field-input:focus { border-color: var(--color-accent); }

.topic-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--color-text-muted);
}

code {
  background-color: var(--color-surface2);
  color: var(--color-normal);
  padding: 2px 8px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 12px;
}

.actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 8px;
}

.saved-msg {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--color-normal);
}

.save-btn {
  background-color: var(--color-accent);
  border: none;
  color: white;
  padding: 10px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: opacity 0.2s;
  margin-left: auto;
}

.save-btn:hover    { opacity: 0.85; }
.save-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>