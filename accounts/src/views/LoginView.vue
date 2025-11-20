<template>
  <div class="login-container">
    <h1>Login</h1>

    <div v-if="loading" class="loading">Loading providers...</div>

    <div v-else class="provider-buttons">
      <ProviderButton
        v-for="provider in providers"
        :key="provider.name"
        :provider="provider"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
// import axios from 'axios';
import { getEnabledProviders, Provider } from '@/services/auth';
import ProviderButton from '@/components/ProviderButton.vue';

interface Provider {
  name: string;
  label?: string;
  auth_url: string;
  callback_url: string;
  logo?: string;
}

export default defineComponent({
  name: 'LoginView',
  components: { ProviderButton },
  setup() {
    const providers = ref<Provider[]>([]);
    const loading = ref(true);

    onMounted(async () => {
      providers.value = await getEnabledProviders();
      loading.value = false;
    });

    const login = (url: string) => {
      window.location.href = url;
    };

    return { providers, loading, login };
  },
});
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 40px auto;
  text-align: center;
}

.loading {
  margin-top: 20px;
  font-style: italic;
}

.provider-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 20px;
}
</style>
