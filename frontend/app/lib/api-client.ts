
import axios from 'axios';

// IMPORTANT: Backend runs on port 8001 (NOT 8000)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

console.log('[API Client] Using backend URL:', API_BASE_URL);

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwt_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for better error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
      console.error('[API Error] Backend is not running or unreachable!');
      console.error(`[API Error] Tried to connect to: ${API_BASE_URL}`);
      console.error('[API Error] Make sure backend is running on port 8001');
    } else if (error.response) {
      console.error(`[API Error] ${error.response.status} ${error.response.statusText}`);
      console.error('[API Error] URL:', error.config?.url);
    } else {
      console.error('[API Error]', error.message);
    }
    return Promise.reject(error);
  }
);

// API methods
export const workflowAPI = {
  startCompliance: async (data: any) => {
    const response = await apiClient.post('/api/v1/workflows/compliance', data);
    return response.data;
  },
  
  getStatus: async (workflowId: string) => {
    const response = await apiClient.get(`/api/v1/workflows/${workflowId}/status`);
    return response.data;
  },
  
  getResults: async (workflowId: string) => {
    const response = await apiClient.get(`/api/v1/workflows/${workflowId}/results`);
    return response.data;
  },
};

export const agentAPI = {
  listAgents: async () => {
    const response = await apiClient.get('/api/v1/agents');
    return response.data;
  },
  
  getAgentStatus: async (agentId: string) => {
    const response = await apiClient.get(`/api/v1/agents/${agentId}/status`);
    return response.data;
  },
};
