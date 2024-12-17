import { useState } from 'react';
import { ModelSelector } from './components/ModelSelector';
import { TextInput } from './components/TextInput';
import { ClusterResults } from './components/ClusterResults';
import { api, ClusteringResponse } from './lib/api';
import { Loader2 } from 'lucide-react';

function App() {
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [clusteringResults, setClusteringResults] = useState<ClusteringResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalyze = async (texts: string[]) => {
    if (!selectedModel) return;

    setIsLoading(true);
    try {
      const results = await api.performClustering(selectedModel, texts);
      setClusteringResults(results);
    } catch (error) {
      console.error('Clustering failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold text-center mb-8">客服文本聚类分析</h1>
        <div className="grid gap-8 md:grid-cols-2">
          <div className="space-y-6">
            <ModelSelector onModelSelect={setSelectedModel} />
            <TextInput onAnalyze={handleAnalyze} disabled={!selectedModel || isLoading} />
          </div>
          <div>
            {isLoading ? (
              <div className="flex items-center justify-center h-64">
                <Loader2 className="animate-spin h-8 w-8" />
              </div>
            ) : clusteringResults ? (
              <ClusterResults
                clusters={clusteringResults.clusters}
                totalTexts={clusteringResults.total_texts}
              />
            ) : (
              <div className="flex items-center justify-center h-64 text-gray-500">
                请选择模型并输入文本开始分析
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
