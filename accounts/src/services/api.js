import axios from "axios"

const api = axios.create({
  baseURL: "http://localhost:8000", // Django backend URL
  withCredentials: true,             // send cookies for session
})

// Get current logged-in user
export const getCurrentUser = async () => {
  try {
    const res = await api.get("/api/auth/user/")
    return res.data
  } catch (err) {
    console.error(err)
    return null
  }
}

export default api
