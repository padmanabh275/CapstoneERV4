import axios, { AxiosInstance, AxiosResponse } from 'axios';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Types
interface LoginRequest {
  email: string;
  password: string;
}

interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  full_name: string;
}

interface LoginResponse {
  access_token: string;
  user: {
    id: number;
    email: string;
    username: string;
    full_name: string;
    is_active: boolean;
    is_verified: boolean;
  };
}

interface ContentGenerationRequest {
  prompt: string;
  content_type: string;
  tone?: string;
  target_audience?: string;
  word_count?: number;
}

interface ContentGenerationResponse {
  content: string;
  seo_score: number;
  suggestions: string[];
}

interface ContentRefinementRequest {
  content: string;
  tone: string;
  target_audience: string;
  word_count?: number;
}

interface ContentRefinementResponse {
  refined_content: string;
  changes_made: string[];
}

interface SEOOptimizationRequest {
  content: string;
  title: string;
  keywords: string[];
}

interface SEOOptimizationResponse {
  optimized_content: string;
  seo_score: number;
  suggestions: string[];
  meta_description: string;
}

interface PlagiarismCheckRequest {
  content: string;
}

interface PlagiarismCheckResponse {
  plagiarism_score: number;
  originality_score: number;
  issues: string[];
  recommendations: string[];
}

// Auth API
export const authAPI = {
  setAuthToken: (token: string) => {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  },

  removeAuthToken: () => {
    delete api.defaults.headers.common['Authorization'];
  },

  login: async (email: string, password: string): Promise<LoginResponse> => {
    const response: AxiosResponse<LoginResponse> = await api.post('/api/v1/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  register: async (userData: RegisterRequest): Promise<LoginResponse> => {
    const response: AxiosResponse<LoginResponse> = await api.post('/api/v1/auth/register', userData);
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/api/v1/auth/me');
    return response.data;
  },

  updateProfile: async (data: Partial<RegisterRequest>) => {
    const response = await api.put('/api/v1/auth/profile', data);
    return response.data;
  },
};

// Content API
export const contentAPI = {
  generateContent: async (request: ContentGenerationRequest): Promise<ContentGenerationResponse> => {
    const response: AxiosResponse<ContentGenerationResponse> = await api.post('/api/v1/generate-content', request);
    return response.data;
  },

  refineContent: async (request: ContentRefinementRequest): Promise<ContentRefinementResponse> => {
    const response: AxiosResponse<ContentRefinementResponse> = await api.post('/api/v1/refine-content', request);
    return response.data;
  },

  optimizeSEO: async (request: SEOOptimizationRequest): Promise<SEOOptimizationResponse> => {
    const response: AxiosResponse<SEOOptimizationResponse> = await api.post('/api/v1/optimize-seo', request);
    return response.data;
  },

  checkPlagiarism: async (request: PlagiarismCheckRequest): Promise<PlagiarismCheckResponse> => {
    const response: AxiosResponse<PlagiarismCheckResponse> = await api.post('/api/v1/check-plagiarism', request);
    return response.data;
  },
};

// Projects API
export const projectsAPI = {
  getProjects: async () => {
    const response = await api.get('/api/v1/projects');
    return response.data;
  },

  getProject: async (id: number) => {
    const response = await api.get(`/api/v1/projects/${id}`);
    return response.data;
  },

  createProject: async (data: { title: string; description?: string }) => {
    const response = await api.post('/api/v1/projects', data);
    return response.data;
  },

  updateProject: async (id: number, data: { title?: string; description?: string }) => {
    const response = await api.put(`/api/v1/projects/${id}`, data);
    return response.data;
  },

  deleteProject: async (id: number) => {
    const response = await api.delete(`/api/v1/projects/${id}`);
    return response.data;
  },
};

// Content Pieces API
export const contentPiecesAPI = {
  getContentPieces: async (projectId?: number) => {
    const url = projectId ? `/api/v1/content-pieces?project_id=${projectId}` : '/api/v1/content-pieces';
    const response = await api.get(url);
    return response.data;
  },

  getContentPiece: async (id: number) => {
    const response = await api.get(`/api/v1/content-pieces/${id}`);
    return response.data;
  },

  createContentPiece: async (data: {
    title: string;
    content: string;
    content_type: string;
    project_id?: number;
    tone?: string;
    target_audience?: string;
  }) => {
    const response = await api.post('/api/v1/content-pieces', data);
    return response.data;
  },

  updateContentPiece: async (id: number, data: {
    title?: string;
    content?: string;
    status?: string;
    seo_title?: string;
    seo_description?: string;
    keywords?: string[];
  }) => {
    const response = await api.put(`/api/v1/content-pieces/${id}`, data);
    return response.data;
  },

  deleteContentPiece: async (id: number) => {
    const response = await api.delete(`/api/v1/content-pieces/${id}`);
    return response.data;
  },
};

export default api; 