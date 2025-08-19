const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface ContentRequest {
    title: string;
    content_type: string;
    description: string;
    target_audience: string;
    tone: string;
    word_count: number;
    keywords?: string[];
    preferred_model?: string; // Add this field
}

export interface ContentResponse {
    id: string;
    title: string;
    content: string;
    content_type: string;
    user_id: string;
    status: string;
    word_count: number;
    content_metadata: Record<string, any>;
    created_at: string;
    updated_at?: string;
}

export const contentApi = {
    async generateContent(request: ContentRequest): Promise<ContentResponse> {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No authentication token found');
        }

        const response = await fetch(`${API_BASE_URL}/content/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`  // Make sure this is included
            },
            body: JSON.stringify(request)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate content');
        }

        return response.json();
    },

    async getProjects(): Promise<ContentResponse[]> {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No authentication token found');
        }

        const response = await fetch(`${API_BASE_URL}/content/projects`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch projects');
        }

        return response.json();
    },

    async getContent(id: string): Promise<ContentResponse> {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No authentication token found');
        }

        const response = await fetch(`${API_BASE_URL}/content/${id}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch content');
        }

        return response.json();
    },

    async updateContent(id: string, updates: Partial<ContentRequest>): Promise<ContentResponse> {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No authentication token found');
        }

        const response = await fetch(`${API_BASE_URL}/content/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(updates)
        });

        if (!response.ok) {
            throw new Error('Failed to update content');
        }

        return response.json();
    },

    async deleteContent(id: string): Promise<void> {
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No authentication token found');
        }

        const response = await fetch(`${API_BASE_URL}/content/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to delete content');
        }
    }
};
