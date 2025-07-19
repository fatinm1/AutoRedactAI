import { authService } from './auth';

export interface Document {
  id: string;
  filename: string;
  file_size?: number;
  user_id: string;
  status: string;
  created_at: string;
  redactions_count?: number;
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

export interface Redaction {
  id: string;
  entity_type: string;
  entity_text: string;
  confidence_score: number;
  start_char: number;
  end_char: number;
  page_number: number;
  line_number?: number;
}

export interface RedactionsResponse {
  success: boolean;
  message: string;
  redactions: Redaction[];
  total_count: number;
}

class DocumentService {
  private baseURL = 'http://localhost:8000/api/v1/documents';

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = authService.getToken();
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, config);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  }

  async uploadDocument(file: File): Promise<DocumentResponse> {
    const token = authService.getToken();
    
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseURL}/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.status}`);
    }

    return response.json();
  }

  async processDocument(documentId: string): Promise<DocumentResponse> {
    return this.request<DocumentResponse>(`/${documentId}/process`, {
      method: 'POST',
    });
  }

  async getDocumentRedactions(documentId: string): Promise<RedactionsResponse> {
    return this.request<RedactionsResponse>(`/${documentId}/redactions`);
  }

  async getDocuments(): Promise<DocumentListResponse> {
    return this.request<DocumentListResponse>('');
  }

  async getDocument(documentId: string): Promise<DocumentResponse> {
    return this.request<DocumentResponse>(`/${documentId}`);
  }
}

export const documentService = new DocumentService(); 