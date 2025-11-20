<template>
  <div class="dashboard-page">
    <h1>Welcome, {{ user?.username }}</h1>
    <p>Email: {{ user?.email }}</p>
    <button @click="logout">Logout</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import axios from "axios";

interface User {
  username: string;
  email: string;
}

export default defineComponent({
  name: "DashboardView",
  setup() {
    const user = ref<User | null>(null);

    onMounted(async () => {
      try {
        const res = await axios.get<User>("/api/accounts/me/");
        user.value = res.data;
      } catch (err) {
        console.error("Failed to fetch user info", err);
      }
    });

    const logout = async () => {
      try {
        await axios.post("/api/auth/logout/");
        window.location.href = "/login";
      } catch (err) {
        console.error("Logout failed", err);
      }
    };

    return { user, logout };
  },
});
</script>

<style scoped>
.dashboard-page { padding: 20px; }
</style>
