import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface ClusterResult {
  id: number;
  summary: string;
  texts: string[];
  size: number;
  percentage: number;
  keywords: string[];
  representative_text: string;
}

export interface ClusteringResponse {
  clusters: ClusterResult[];
  total_texts: number;
  model_used: string;
  created_at: string;
}

export interface ModelInfo {
  id: string;
  name: string;
  description: string;
}

export const api = {
  getModels: async (): Promise<ModelInfo[]> => {
    const response = await axios.get<ModelInfo[]>(`${API_URL}/models`);
    return response.data;
  },

  performClustering: async (modelId: string, texts: string[]): Promise<ClusteringResponse> => {
    const response = await axios.post<ClusteringResponse>(`${API_URL}/cluster`, {
      model_id: modelId,
      texts,
    });
    return response.data;
  },
};
