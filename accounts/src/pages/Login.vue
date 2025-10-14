<template>
  <div class="login-container">
    <h2>Sign in to Continue</h2>
    <div class="buttons">
      <AuthButton
        v-for="(provider, name) in enabledProviders"
        :key="name"
        :providerName="name"
        :provider="provider"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import AuthButton from "@/components/AuthButton.vue"

const providers = ref({})

onMounted(async () => {
  const res = await fetch("/env/config.json")
  providers.value = await res.json()
})

const enabledProviders = computed(() =>
  Object.fromEntries(
    Object.entries(providers.value).filter(([_, v]) => v.enabled)
  )
)
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10vh;
}
.buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
