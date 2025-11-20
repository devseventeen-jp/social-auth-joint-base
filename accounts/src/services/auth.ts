import axios from 'axios';

export interface Provider {
  name: string;
  auth_url: string;
  callback_url: string;
  logo?: string;
  label?: string;
  order?: number;
}

export async function getEnabledProviders(): Promise<Provider[]> {
  try {
    const res = await axios.get<Provider[]>('/api/auth/providers/');
    const backendProviders: Provider[] = res.data.providers;

    const uiRes = await fetch('/providers_ui.json');
    const uiConfig = await uiRes.json();

    const merged = backendProviders.map(p => {
      const ui = uiConfig[p.name] || {};
      return {
        ...p,
        logo: `/assets/icons/${p.name.toLowerCase()}-logo.svg`,
        label: ui.label ?? p.name,
        order: ui.order ?? 999
      };
    });

    return merged.sort((a, b) => (a.order! - b.order!));
//    const providers = res.data.providers.map((p) => ({
//      name: p.name,
//      url: p.auth_url,
//      logo: `/assets/icons/${p.name.toLowerCase()}-logo.svg`,
//    }));
//    return providers;
  } catch (error) {
    console.error('Failed to fetch providers', error);
    return [];
  }
}

export async function fetchProviders(): Promise<Provider[]> {
  const res = await axios.get("/api/auth/providers/");
  return res.data.providers;
}