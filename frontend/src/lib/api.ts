import axios from 'axios';

const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8000';

export interface TaskConfig {
  name: string;
  description: string;
  strategy: string;
  tags: string[];
}

class ApiClient {
  private axios = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  async updateTask(taskConfig: TaskConfig): Promise<void> {
    await this.axios.post('/api/tasks', taskConfig);
  }

  async startClaudeChat(taskConfig: TaskConfig): Promise<{ chatId: string }> {
    const response = await this.axios.post('/api/chat/start', taskConfig);
    return response.data;
  }

  async sendMessage(chatId: string, message: string): Promise<any> {
    const response = await this.axios.post(`/api/chat/${chatId}/message`, {
      message,
    });
    return response.data;
  }
}

export const apiClient = new ApiClient();
