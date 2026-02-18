<template>
  <div class="app-layout">
    <AppSidebar />
    <div class="main-area">
      <AppHeader />
      <main class="content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import AppSidebar from './components/common/AppSidebar.vue'
import AppHeader from './components/common/AppHeader.vue'
</script>

<style scoped>
.app-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
}

.main-area {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background-color: var(--color-bg);
}
</style>