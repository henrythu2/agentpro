import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useEffect, useState } from "react";
import { api, ModelInfo } from "@/lib/api";

interface ModelSelectorProps {
  onModelSelect: (modelId: string) => void;
}

export function ModelSelector({ onModelSelect }: ModelSelectorProps) {
  const [models, setModels] = useState<ModelInfo[]>([]);

  useEffect(() => {
    const loadModels = async () => {
      try {
        const availableModels = await api.getModels();
        setModels(availableModels);
      } catch (error) {
        console.error('Failed to load models:', error);
      }
    };
    loadModels();
  }, []);

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>选择聚类模型</CardTitle>
        <CardDescription>选择合适的聚类算法来分析文本</CardDescription>
      </CardHeader>
      <CardContent>
        <Select onValueChange={onModelSelect}>
          <SelectTrigger>
            <SelectValue placeholder="选择模型" />
          </SelectTrigger>
          <SelectContent>
            {models.map((model) => (
              <SelectItem key={model.id} value={model.id}>
                {model.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </CardContent>
    </Card>
  );
}
