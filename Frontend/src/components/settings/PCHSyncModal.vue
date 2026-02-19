<template>
  <Teleport to="body">
    <div v-if="show" class="pch-overlay" @click.self="$emit('close')">
      <div class="pch-modal">

        <!-- Header -->
        <div class="pch-header">
          <div class="pch-title">
            <Server :size="20" />
            <span>Conectar Servidor PCH</span>
          </div>
          <button class="pch-close" @click="$emit('close')">
            <CircleX :size="18" />
          </button>
        </div>

        <!-- Body -->
        <div class="pch-body">

          <!-- Step 1: Credenciales -->
          <template v-if="step === 'form'">
            <p class="pch-subtitle">
              Importa activos industriales directamente desde tu servidor PCH Engineering.
            </p>
            <div class="pch-field">
              <label>Servidor</label>
              <select v-model="form.host">
                <option value="pchcloud">PCH Cloud</option>
                <option value="local">Local</option>
                <option value="demo">Demo</option>
              </select>
            </div>
            <div class="pch-field">
              <label>Usuario</label>
              <input v-model="form.username" type="text" placeholder="usuario" autocomplete="username" />
            </div>
            <div class="pch-field">
              <label>Contraseña</label>
              <input v-model="form.password" type="password" placeholder="••••••••" autocomplete="current-password" />
            </div>
            <div v-if="error" class="pch-error">
              <AlertCircle :size="14" /> {{ error }}
            </div>
            <div class="pch-actions">
              <button class="pch-btn-secondary" @click="$emit('close')">Cancelar</button>
              <button class="pch-btn-primary" :disabled="loading" @click="testConnection">
                <Loader2 v-if="loading" :size="14" class="spinning" />
                <span>{{ loading ? 'Conectando...' : 'Verificar conexión' }}</span>
              </button>
            </div>
          </template>

          <!-- Step 2: Preview de dispositivos -->
          <template v-if="step === 'preview'">
            <div class="pch-success-header">
              <CheckCircle2 :size="20" class="icon-success" />
              <span>{{ deviceCount }} dispositivos encontrados en <strong>{{ form.host }}</strong></span>
            </div>
            <div class="pch-device-list">
              <div v-for="d in devices" :key="d.key" class="pch-device-item">
                <Cpu :size="14" />
                <div>
                  <span class="device-name">{{ d.name || d.deviceId }}</span>
                  <span class="device-key">{{ d.key }}</span>
                </div>
              </div>
              <div v-if="devices.length === 0" class="pch-empty">
                No se encontraron dispositivos.
              </div>
            </div>
            <div v-if="error" class="pch-error">
              <AlertCircle :size="14" /> {{ error }}
            </div>
            <div class="pch-actions">
              <button class="pch-btn-secondary" @click="step = 'form'">Volver</button>
              <button class="pch-btn-primary" :disabled="loading || devices.length === 0" @click="syncAssets">
                <Loader2 v-if="loading" :size="14" class="spinning" />
                <span>{{ loading ? 'Sincronizando...' : 'Importar ' + deviceCount + ' activos' }}</span>
              </button>
            </div>
          </template>

          <!-- Step 3: Resultado -->
          <template v-if="step === 'done'">
            <div class="pch-result">
              <CheckCircle2 :size="40" class="icon-success" />
              <h3>Sincronización completada</h3>
              <div class="pch-stats">
                <div class="stat"><span>{{ syncResult.created }}</span><label>Creados</label></div>
                <div class="stat"><span>{{ syncResult.updated }}</span><label>Actualizados</label></div>
                <div class="stat"><span>{{ syncResult.total }}</span><label>Total</label></div>
              </div>
              <p v-if="syncResult.errors?.length" class="pch-warn">
                {{ syncResult.errors.length }} dispositivo(s) con error.
              </p>
            </div>
            <div class="pch-actions">
              <button class="pch-btn-primary" @click="handleDone">Listo</button>
            </div>
          </template>

        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Server, CircleX, AlertCircle, CheckCircle2, Loader2, Cpu } from 'lucide-vue-next'
import { pchAPI } from '../../services/api.js'

const props = defineProps({ show: Boolean })
const emit  = defineEmits(['close', 'synced'])

const step        = ref('form')
const loading     = ref(false)
const error       = ref(null)
const devices     = ref([])
const deviceCount = ref(0)
const syncResult  = ref(null)

const form = reactive({ host: 'pchcloud', username: '', password: '' })

async function testConnection() {
  error.value = null
  loading.value = true
  try {
    const res = await pchAPI.testConnection(form.host, form.username, form.password)
    devices.value     = res.devices || []
    deviceCount.value = res.device_count || 0
    step.value = 'preview'
  } catch (e) {
    error.value = e.message || 'No se pudo conectar al servidor PCH'
  } finally {
    loading.value = false
  }
}

async function syncAssets() {
  error.value = null
  loading.value = true
  try {
    const res = await pchAPI.syncAssets(form.host, form.username, form.password)
    syncResult.value = res
    step.value = 'done'
  } catch (e) {
    error.value = e.message || 'Error durante la sincronización'
  } finally {
    loading.value = false
  }
}

function handleDone() {
  emit('synced')
  emit('close')
  step.value = 'form'
  devices.value = []
  syncResult.value = null
  error.value = null
}
</script>

<style scoped>
.pch-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.pch-modal {
  background-color: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 12px;
  width: 480px;
  max-width: 95vw;
  box-shadow: 0 20px 60px rgba(0,0,0,0.25);
  overflow: hidden;
}

.pch-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  border-bottom: 1px solid var(--color-surface2);
}

.pch-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 15px;
  color: var(--color-text-dark);
}

.pch-close {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-text-muted);
  padding: 4px;
  border-radius: 4px;
  transition: background 0.15s;
}
.pch-close:hover { background-color: var(--color-surface3); }

.pch-body { padding: 20px; }

.pch-subtitle {
  color: var(--color-text-muted);
  font-size: 13px;
  margin-bottom: 18px;
  line-height: 1.5;
}

.pch-field { margin-bottom: 14px; }

.pch-field label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-dark);
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.pch-field input,
.pch-field select {
  width: 100%;
  padding: 8px 14px;
  border: 1px solid var(--color-surface);
  border-radius: 8px;
  font-size: 13px;
  color: var(--color-text-dark);
  background-color: var(--color-surface3);
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.2s;
}
.pch-field input:focus,
.pch-field select:focus {
  border-color: var(--color-accent);
  background-color: var(--color-surface4);
}

.pch-error {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: var(--color-surface3);
  color: var(--color-critical);
  font-size: 13px;
  padding: 8px 12px;
  border-radius: 8px;
  margin-bottom: 14px;
  border: 1px solid var(--color-surface);
}

.pch-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 18px;
}

.pch-btn-primary {
  display: flex;
  align-items: center;
  gap: 6px;
  background-color: var(--color-accent);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.pch-btn-primary:hover:not(:disabled) { opacity: 0.85; }
.pch-btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

.pch-btn-secondary {
  background-color: var(--color-surface3);
  color: var(--color-text-dark);
  border: 1px solid var(--color-surface);
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.pch-btn-secondary:hover { opacity: 0.85; }

.pch-success-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  margin-bottom: 14px;
  color: var(--color-text-dark);
}
.icon-success { color: var(--color-normal); }

.pch-device-list {
  border: 1px solid var(--color-surface);
  border-radius: 8px;
  max-height: 220px;
  overflow-y: auto;
}
.pch-device-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-bottom: 1px solid var(--color-surface);
  color: var(--color-text-muted);
  font-size: 13px;
}
.pch-device-item:last-child { border-bottom: none; }

.device-name {
  display: block;
  font-weight: 600;
  color: var(--color-text-dark);
  font-size: 13px;
}
.device-key {
  display: block;
  color: var(--color-text-muted);
  font-size: 11px;
  font-family: monospace;
}
.pch-empty {
  padding: 20px;
  text-align: center;
  color: var(--color-text-muted);
  font-size: 13px;
}

.pch-result {
  text-align: center;
  padding: 10px 0 6px;
}
.pch-result h3 {
  margin: 12px 0 16px;
  font-size: 17px;
  color: var(--color-text-dark);
}
.pch-stats {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 14px;
}
.stat span {
  display: block;
  font-size: 28px;
  font-weight: 800;
  color: var(--color-accent);
}
.stat label {
  font-size: 12px;
  color: var(--color-text-muted);
  text-transform: uppercase;
}
.pch-warn {
  font-size: 12px;
  color: var(--color-critical);
  background-color: var(--color-surface3);
  padding: 6px 10px;
  border-radius: 5px;
  border: 1px solid var(--color-surface);
}

.spinning { animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>