import { createRouter, createWebHistory } from "vue-router"
import Login from "@/pages/Login.vue"
import Register from "@/pages/Register.vue"
import Dashboard from "@/pages/Dashboard.vue"
import { getCurrentUser } from "@/services/api.js"

const routes = [
  { path: "/", name: "Login", component: Login },
  { path: "/register", name: "Register", component: Register },
  { path: "/dashboard", name: "Dashboard", component: Dashboard, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard },
    { path: '/login', component: Login },
})

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    const user = await getCurrentUser()
    if (user) {
      next()
    } else {
      next({ path: "/" })
    }
  } else {
    next()
  }
})

export default router
