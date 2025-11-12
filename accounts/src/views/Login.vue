<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    <h1 class="text-2xl font-bold mb-6">Sign in with</h1>

    <div class="space-y-3">
      <button
        v-for="provider in providers"
        :key="provider.name"
        class="flex items-center px-4 py-2 bg-white rounded shadow hover:bg-gray-100"
        @click="login(provider)"
      >
        <img
          v-if="provider.name === 'google'"
          src="/assets/google-logo.svg"
          alt="Google"
          class="w-5 h-5 mr-2"
        />
        <span class="capitalize">{{ provider.name }}</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { fetchProviders } from "@/services/api";

const providers = ref([]);

onMounted(async () => {
  providers.value = await fetchProviders();
});

const login = (provider) => {
  const redirectUrl = `${provider.auth_url}?client_id=...`; // ← ここは後でOAuthフローで生成
  window.location.href = redirectUrl;
};
</script>
