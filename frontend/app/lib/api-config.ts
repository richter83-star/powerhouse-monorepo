
// Central API configuration
const API_PORT = process.env.NEXT_PUBLIC_API_PORT || '8001';
const API_HOST = process.env.NEXT_PUBLIC_API_HOST || 'localhost';

export const API_BASE_URL = `http://${API_HOST}:${API_PORT}`;
export const API_ENDPOINTS = {
  agents: `${API_BASE_URL}/api/v1/agents`,
  workflows: `${API_BASE_URL}/api/v1/workflows`,
  files: `${API_BASE_URL}/api/files`,
  learning: `${API_BASE_URL}/api/learning`,
  performance: `${API_BASE_URL}/api/performance`,
  config: `${API_BASE_URL}/api/config`,
};
