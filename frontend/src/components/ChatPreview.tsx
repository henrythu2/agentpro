import { useState, useRef, useEffect } from 'react';
import { Button } from './ui/button';
import { ScrollArea } from './ui/scroll-area';
import { Input } from './ui/input';
import { apiClient } from '../lib/api';

interface Message {
  role: 'assistant' | 'user';
  content: string;
}

interface ChatPreviewProps {
  taskConfig: {
    name: string;
    description: string;
    strategy: string;
    tags: string[];
  };
}

export function ChatPreview({ taskConfig }: ChatPreviewProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [chatId, setChatId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    initializeChat();
  }, []);

  const initializeChat = async () => {
    try {
      setIsLoading(true);
      const response = await apiClient.startClaudeChat(taskConfig);
      setChatId(response.chatId);
      setMessages([
        {
          role: 'assistant',
          content: 'Hello! I am configured with your task settings. How can I help you today?'
        }
      ]);
    } catch (error) {
      console.error('Failed to initialize chat:', error);
      setMessages([
        {
          role: 'assistant',
          content: 'Failed to initialize chat. Please check your configuration and try again.'
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !chatId || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    
    try {
      setIsLoading(true);
      const response = await apiClient.sendMessage(chatId, userMessage);
      setMessages(prev => [...prev, { role: 'assistant', content: response.content }]);
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your message. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[500px]">
      <ScrollArea className="flex-1 p-4 border rounded-lg mb-4" ref={scrollAreaRef}>
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === 'assistant' ? 'justify-start' : 'justify-end'
              }`}
            >
              <div
                className={`max-w-[80%] p-3 rounded-lg ${
                  message.role === 'assistant'
                    ? 'bg-gray-100'
                    : 'bg-blue-500 text-white'
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="max-w-[80%] p-3 rounded-lg bg-gray-100">
                <span className="animate-pulse">...</span>
              </div>
            </div>
          )}
        </div>
      </ScrollArea>
      <div className="flex gap-2">
        <Input
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type your message..."
          disabled={isLoading || !chatId}
        />
        <Button
          onClick={sendMessage}
          disabled={isLoading || !chatId || !inputMessage.trim()}
        >
          Send
        </Button>
      </div>
    </div>
  );
}
