<template>
  <div class="login-container">
    <h1>Login</h1>
    <div v-if="loading" class="loading">Loading providers...</div>
    <div v-else class="provider-buttons">
      <button
        v-for="provider in providers"
        :key="provider.name"
        @click="login(provider.auth_url)"
        class="login-btn"
        :class="{
          'logo-text': !!provider.logo,
          'text-only': !provider.logo
        }"
      >
        <template v-if="provider.logo">
          <img :src="provider.logo" :alt="provider.name" width="24" />
          {{ provider.name }}
        </template>
        <template v-else>
          {{ provider.name }}
        </template>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { getEnabledProviders, Provider } from '@/services/auth';

export default defineComponent({
  name: 'LoginView',
  setup() {
    const providers = ref<Provider[]>([]);
    const loading = ref(true);

    const majorProviders = ['google', 'facebook', 'github', 'apple'];

    onMounted(async () => {
      const fetched = await getEnabledProviders();

      // #ToDo: Sort in API 
      const sorted = [
        ...fetched.filter(p => majorProviders.includes(p.name.toLowerCase())),
        ...fetched.filter(p => !majorProviders.includes(p.name.toLowerCase())),
      ];

      providers.value = sorted;
      loading.value = false;
    });

    const login = (url: string) => {
      window.location.href = url;
    };

    return { providers, loading, login };
  }
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

.login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
  background: #fff;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.2s ease;
}

.login-btn img {
  margin-right: 8px;
}

.login-btn:hover {
  background: #f0f0f0;
}

.login-btn.logo-text {
  justify-content: flex-start;
}

.login-btn.text-only {
  justify-content: center;
}
</style>
