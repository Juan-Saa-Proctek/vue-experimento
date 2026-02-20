<template>
  <div class="toast-container">
    <transition-group name="toast">
      <div 
        v-for="toast in toasts" 
        :key="toast.id"
        class="toast"
        :class="toast.type"
        @click="remove(toast.id)"
      >
        <div class="toast-icon">
          <CheckCircle v-if="toast.type === 'success'" :size="20" />
          <XCircle v-if="toast.type === 'error'" :size="20" />
          <AlertCircle v-if="toast.type === 'warning'" :size="20" />
          <Info v-if="toast.type === 'info'" :size="20" />
        </div>
        <div class="toast-message">{{ toast.message }}</div>
        <button class="toast-close" @click.stop="remove(toast.id)">
          <XCircle :size="16" />
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-vue-next'
import { useToast } from '../../composables/useToast'

const { toasts, remove } = useToast()
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 12px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 300px;
  max-width: 400px;
  padding: 12px 16px;
  background: var(--color-surface4);
  border: 1px solid var(--color-surface);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  pointer-events: auto;
  cursor: pointer;
}

.toast.success { border-left: 4px solid var(--color-normal); }
.toast.error { border-left: 4px solid var(--color-critical); }
.toast.warning { border-left: 4px solid var(--color-warning); }
.toast.info { border-left: 4px solid var(--color-accent); }

.toast-icon { display: flex; flex-shrink: 0; }
.toast.success .toast-icon { color: var(--color-normal); }
.toast.error .toast-icon { color: var(--color-critical); }
.toast.warning .toast-icon { color: var(--color-warning); }
.toast.info .toast-icon { color: var(--color-accent); }

.toast-message {
  flex: 1;
  font-size: 14px;
  color: var(--color-text-dark);
}

.toast-close {
  display: flex;
  padding: 4px;
  background: transparent;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.2s;
}

.toast-close:hover { background: var(--color-surface4); }

.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from { opacity: 0; transform: translateX(100px); }
.toast-leave-to { opacity: 0; transform: translateX(100px); }
</style>