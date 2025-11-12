<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50">
    <h1 class="text-2xl font-semibold mb-6">ログイン</h1>

    <div v-if="loading" class="text-gray-500">読み込み中...</div>

    <div v-else>
      <div
        v-for="(provider, name) in providers"
        :key="name"
        class="mb-3"
      >
        <button
          @click="login(name, provider.auth_url)"
          class="px-5 py-2 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600 transition"
        >
          {{ name.toUpperCase() }} でログイン
        </button>
      </div>
    </div>

    <div v-if="error" class="text-red-500 mt-4">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { getEnabledProviders, redirectToProvider } from "../services/authService.ts";

const providers = ref({});
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const data = await getEnabledProviders();
    providers.value = data;
  } catch (err) {
    error.value = "ログイン情報の取得に失敗しました";
  } finally {
    loading.value = false;
  }
});

function login(name, authUrl) {
  redirectToProvider(name, authUrl);
}
</script>
