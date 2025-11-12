// src/services/authService.js
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getEnabledProviders() {
  try {
    const response = await axios.get(`${API_BASE_URL}/auth/providers/`);
    return response.data; // 例: { google: { auth_url: "...", callback_url: "..." }, ... }
  } catch (error) {
    console.error("Failed to load providers:", error);
    return {};
  }
}

export function redirectToProvider(providerName, authUrl) {
  window.location.href = authUrl;
}
