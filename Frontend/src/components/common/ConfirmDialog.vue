<template>
  <teleport to="body">
    <transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click="handleCancel">
        <div class="modal-content" @click.stop>
          <div class="modal-icon" :class="type">
            <AlertTriangle v-if="type === 'warning'" :size="48" />
            <AlertCircle v-if="type === 'danger'" :size="48" />
            <Info v-if="type === 'info'" :size="48" />
          </div>
          
          <h3 class="modal-title">{{ title }}</h3>
          <p class="modal-message">{{ message }}</p>
          
          <div class="modal-actions">
            <button class="btn-cancel" @click="handleCancel">
              {{ cancelText }}
            </button>
            <button class="btn-confirm" :class="type" @click="handleConfirm">
              {{ confirmText }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref } from 'vue'
import { AlertTriangle, AlertCircle, Info } from 'lucide-vue-next'

const isOpen = ref(false)
const resolvePromise = ref(null)

const title = ref('')
const message = ref('')
const type = ref('warning')
const confirmText = ref('Confirmar')
const cancelText = ref('Cancelar')

function show(opts = {}) {
  title.value = opts.title || '¿Confirmar acción?'
  message.value = opts.message || '¿Estás seguro?'
  type.value = opts.type || 'warning'
  confirmText.value = opts.confirmText || 'Confirmar'
  cancelText.value = opts.cancelText || 'Cancelar'
  
  isOpen.value = true
  
  return new Promise((resolve) => {
    resolvePromise.value = resolve
  })
}

function handleConfirm() {
  isOpen.value = false
  if (resolvePromise.value) {
    resolvePromise.value(true)
  }
}

function handleCancel() {
  isOpen.value = false
  if (resolvePromise.value) {
    resolvePromise.value(false)
  }
}

defineExpose({ show })
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}

.modal-content {
  background: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 12px;
  padding: 32px;
  max-width: 400px;
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.modal-icon {
  display: flex;
  padding: 12px;
  border-radius: 50%;
}

.modal-icon.warning {
  background: rgba(251, 191, 36, 0.15);
  color: var(--color-warning);
}

.modal-icon.danger {
  background: rgba(239, 68, 68, 0.15);
  color: var(--color-critical);
}

.modal-icon.info {
  background: rgba(59, 130, 246, 0.15);
  color: var(--color-accent);
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-dark);
  margin: 0;
  text-align: center;
}

.modal-message {
  font-size: 14px;
  color: var(--color-text-muted);
  margin: 0;
  text-align: center;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 12px;
  width: 100%;
  margin-top: 8px;
}

.btn-cancel,
.btn-confirm {
  flex: 1;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
  border: none;
}

.btn-cancel {
  background: var(--color-surface2);
  color: var(--color-text);
}

.btn-cancel:hover {
  background: var(--color-surface);
}

.btn-confirm {
  background: var(--color-accent);
  color: var(--color-text);
}

.btn-confirm.danger {
  background: var(--color-critical);
}

.btn-confirm.warning {
  background: var(--color-warning);
}

.btn-confirm:hover {
  opacity: 0.85;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.2s;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9);
}
</style>