const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface ContentRequest {
  title: string;
  content_type: string;
  description: string;
  target_audience: string;
  tone: string;
  word_count: number;
  keywords?: string[];
}

export interface ContentResponse {
  id: string;
  title: string;
  content: string;
  content_type: string;
  status: string;
  word_count: number;
  created_at: string;
  updated_at: string;
}

export const contentApi = {
  // Generate new content using AI
  async generateContent(request: ContentRequest): Promise<ContentResponse> {
    const token = localStorage.getItem('authToken');
    
    const response = await fetch(`${API_BASE_URL}/content/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to generate content');
    }

    return response.json();
  },

  // Get user's content projects
  async getProjects(): Promise<ContentResponse[]> {
    const token = localStorage.getItem('authToken');
    
    const response = await fetch(`${API_BASE_URL}/content/projects`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch projects');
    }

    return response.json();
  },

  // Get specific content by ID
  async getContent(id: string): Promise<ContentResponse> {
    const token = localStorage.getItem('authToken');
    
    const response = await fetch(`${API_BASE_URL}/content/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to fetch content');
    }

    return response.json();
  },

  // Update content
  async updateContent(id: string, updates: Partial<ContentRequest>): Promise<ContentResponse> {
    const token = localStorage.getItem('authToken');
    
    const response = await fetch(`${API_BASE_URL}/content/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(updates),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to update content');
    }

    return response.json();
  },

  // Delete content
  async deleteContent(id: string): Promise<void> {
    const token = localStorage.getItem('authToken');
    
    const response = await fetch(`${API_BASE_URL}/content/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to delete content');
    }
  },
};



