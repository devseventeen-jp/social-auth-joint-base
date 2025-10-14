<template>
  <div class="register">
    <h2>Complete Your Registration</h2>
    <p>Provider: {{ providerName }}</p>
    
    <form @submit.prevent="submit">
      <label>
        Display Name:
        <input v-model="displayName" required />
      </label>
      <label>
        Accept Terms:
        <input type="checkbox" v-model="acceptTerms" required />
      </label>
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import api from "@/services/api.js"  // axios instance with withCredentials=true

const router = useRouter()
const route = useRoute()
const providerName = ref("")

const displayName = ref("")
const acceptTerms = ref(false)

onMounted(() => {
  // OAuth リダイレクト後に ?provider=google などで渡される想定
  providerName.value = route.query.provider || "Unknown"
})

function getCookie(name) {
  const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')
  return v ? v.pop() : ''
}

const submit = async () => {
  // get CSRF token from cookie
  const csrftoken = getCookie("csrftoken")

  try {
    await api.post(
      "/api/auth/register/",
      {
        display_name: displayName.value,
        accept_terms: acceptTerms.value
      },
      {
        headers: {
          "X-CSRFToken": csrftoken
        }
      }
    )
    router.push("/dashboard")
  } catch (err) {
    console.error(err)
    alert("Registration failed")
  }
}
</script>

<style scoped>
.register {
  margin: 5vh auto;
  max-width: 400px;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
