import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useState } from "react";

interface TextInputProps {
  onAnalyze: (texts: string[]) => void;
  disabled?: boolean;
}

export function TextInput({ onAnalyze, disabled }: TextInputProps) {
  const [input, setInput] = useState("");

  const handleAnalyze = () => {
    const texts = input
      .split("\n")
      .map((text) => text.trim())
      .filter((text) => text.length > 0);

    if (texts.length > 0) {
      onAnalyze(texts);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>输入文本</CardTitle>
        <CardDescription>每行输入一条客服对话文本</CardDescription>
      </CardHeader>
      <CardContent>
        <Textarea
          placeholder="输入文本，每行一条..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="min-h-[8rem] mb-4"
        />
        <Button
          onClick={handleAnalyze}
          disabled={disabled || !input.trim()}
          className="w-full"
        >
          开始分析
        </Button>
      </CardContent>
    </Card>
  );
}
