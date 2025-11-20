<template>
  <button
    class="login-btn"
    :class="{
      'logo-text': !!provider.logo,
      'text-only': !provider.logo
    }"
    @click="login(provider.auth_url)"
  >
    <template v-if="provider.logo">
      <img :src="provider.logo" :alt="provider.name" width="24" />
      <span>{{ provider.label ?? provider.name }}</span>
    </template>
    <template v-else>
      <span>{{ provider.label ?? provider.name }}</span>
    </template>
  </button>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

interface Provider {
  name: string;
  label?: string;
  auth_url: string;
  callback_url: string;
  logo?: string;
}

export default defineComponent({
  name: 'ProviderButton',
  props: {
    provider: {
      type: Object as PropType<Provider>,
      required: true
    }
  },
  setup(props) {
    const login = (url: string) => {
      window.location.href = url;
    };

    return { login };
  }
});
</script>

<style scoped>
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
