import axios from 'axios';

export interface Provider {
  name: string;
  auth_url: string;
  callback_url: string;
  logo?: string;
}

export async function getEnabledProviders(): Promise<Provider[]> {
  try {
    const res = await axios.get<Provider[]>('/api/auth/providers/');
    const providers = res.data.providers.map((p) => ({
      name: p.name,
      url: p.auth_url,
      logo: `/assets/icons/${p.name.toLowerCase()}-logo.svg`,
    }));
    return providers;
  } catch (error) {
    console.error('Failed to fetch providers', error);
    return [];
  }
}
