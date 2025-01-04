import { useState } from 'react';
import { ChatPreview } from './ChatPreview';
import { Button } from './ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Textarea } from './ui/textarea';
import { Input } from './ui/input';
import { Label } from './ui/label';

interface TaskEditorProps {
  initialTask?: {
    name: string;
    description: string;
    strategy: string;
    tags: string[];
  };
}

export function TaskEditor({ initialTask }: TaskEditorProps) {
  const [task, setTask] = useState(initialTask || {
    name: '',
    description: '',
    strategy: '',
    tags: []
  });
  const [previewOpen, setPreviewOpen] = useState(false);

  const handleInputChange = (field: string, value: string) => {
    setTask(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-sm p-6 space-y-6">
        <h1 className="text-xl font-semibold text-gray-900">编辑任务</h1>
        
        <div className="space-y-4">
          <div>
            <Label className="text-sm font-medium text-gray-700">任务名称</Label>
            <Input
              value={task.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              className="mt-1"
            />
          </div>

          <div>
            <Label className="text-sm font-medium text-gray-700">任务描述</Label>
            <Textarea
              value={task.description}
              onChange={(e) => handleInputChange('description', e.target.value)}
              className="mt-1"
              rows={3}
            />
          </div>

          <div>
            <Label className="text-sm font-medium text-gray-700">任务策略</Label>
            <Textarea
              value={task.strategy}
              onChange={(e) => handleInputChange('strategy', e.target.value)}
              className="mt-1 font-mono"
              rows={7}
            />
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <Dialog open={previewOpen} onOpenChange={setPreviewOpen}>
              <DialogTrigger asChild>
                <Button variant="outline">预览</Button>
              </DialogTrigger>
              <DialogContent className="max-w-3xl">
                <DialogHeader>
                  <DialogTitle>任务预览</DialogTitle>
                </DialogHeader>
                <div className="mt-4">
                  <ChatPreview taskConfig={task} />
                </div>
              </DialogContent>
            </Dialog>
            <Button>更新任务</Button>
          </div>
        </div>
      </div>
    </div>
  );
}
