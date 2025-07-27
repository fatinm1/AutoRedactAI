import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
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

export interface Document {
  id: string;
  filename: string;
  file_size: number;
  status: string;
  created_at: string;
  redactions_count: number;
}

export interface DocumentResponse {
  success: boolean;
  message: string;
  document: Document;
}

export interface DocumentListResponse {
  success: boolean;
  message: string;
  documents: Document[];
}

class DocumentService {
  async uploadDocument(file: File): Promise<DocumentResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/v1/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  async processDocument(documentId: string): Promise<DocumentResponse> {
    const response = await api.post(`/api/v1/documents/${documentId}/process`);
    return response.data;
  }

  async getDocuments(): Promise<DocumentListResponse> {
    const response = await api.get('/api/v1/documents/');
    return response.data;
  }

  async getDocument(documentId: string): Promise<DocumentResponse> {
    const response = await api.get(`/api/v1/documents/${documentId}`);
    return response.data;
  }

  async getDocumentRedactions(documentId: string): Promise<any> {
    const response = await api.get(`/api/v1/documents/${documentId}/redactions`);
    return response.data;
  }

  async validatePdfFile(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/v1/documents/validate-pdf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }
}

export const documentService = new DocumentService(); 