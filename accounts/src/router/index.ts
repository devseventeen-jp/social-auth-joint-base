import { createRouter, createWebHistory } from "vue-router"
import Login from "@/pages/Login.vue"
import Register from "@/pages/Register.vue"
import Dashboard from "@/pages/Dashboard.vue"
// import { getCurrentUser } from "@/services/api.ts"

import LoginView from '@/views/LoginView.vue';
import CallbackView from '@/views/CallbackView.vue';
import DashboardView from '@/views/DashboardView.vue';

const routes: Array<RouteRecordRaw> = [
//  { path: "/", name: "Login", component: Login },
//  { path: "/register", name: "Register", component: Register },
//  { path: "/dashboard", name: "Dashboard", component: Dashboard, meta: { requiresAuth: true } }
  { path: '/', name: 'login', component: LoginView, },
  { path: '/auth/callback', name: 'callback', component: CallbackView, },
  { path: '/dashboard', name: 'dashboard', component: DashboardView, }
]

const router = createRouter({
  history: createWebHistory(),
  routes: [
//    { path: '/', component: Dashboard },
//    { path: '/login', component: Login },
    { path: '/', component: DashboardView },
    { path: '/login', component: LoginView },
] })

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
