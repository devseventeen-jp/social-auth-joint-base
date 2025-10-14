<template>
  <div class="dashboard">
    <h2>Dashboard</h2>
    <div v-if="user">
      <p>Welcome, {{ user.username }}!</p>
      <p>Email: {{ user.email }}</p>
    </div>
    <div v-else>
      <p>Loading user info...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { getCurrentUser } from "@/services/api.js"

const user = ref(null)

onMounted(async () => {
  user.value = await getCurrentUser()
})
</script>

<style scoped>
.dashboard {
  margin: 5vh auto;
  text-align: center;
}
</style>
