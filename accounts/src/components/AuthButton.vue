<template>
  <button
    v-if="provider.enabled"
    @click="login"
    class="auth-btn"
  >
    <img :src="`/assets/${providerName}.svg`" :alt="providerName" class="icon" />
    Login with {{ providerName }}
  </button>
</template>

<script setup>
const props = defineProps({
  providerName: String,
  provider: Object,
})

const login = () => {
  window.location.href = props.provider.auth_url
}
</script>

<style scoped>
.auth-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0.8em 1.2em;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  background: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.icon {
  width: 20px;
  height: 20px;
}
</style>
