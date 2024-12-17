import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { ClusterResult } from "@/lib/api";

interface ClusterResultsProps {
  clusters: ClusterResult[];
  totalTexts: number;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

export function ClusterResults({ clusters, totalTexts }: ClusterResultsProps) {
  const pieData = clusters.map((cluster) => ({
    name: `Cluster ${cluster.id}`,
    value: cluster.size,
  }));

  return (
    <div className="grid grid-cols-1 gap-4">
      <Card>
        <CardHeader>
          <CardTitle>聚类分布 (共{totalTexts}条文本)</CardTitle>
        </CardHeader>
        <CardContent className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label={({ name, percent }) => `${name} (${(percent * 100).toFixed(1)}%)`}
              >
                {pieData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>聚类结果详情</CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-96">
            <div className="space-y-6">
              {clusters.map((cluster) => (
                <div key={cluster.id} className="p-4 border rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-lg font-semibold">Cluster {cluster.id}</h3>
                    <Badge variant="secondary">
                      {cluster.size} texts ({cluster.percentage.toFixed(1)}%)
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mb-2">{cluster.summary}</p>
                  <div className="flex flex-wrap gap-2">
                    {cluster.keywords.map((keyword, idx) => (
                      <Badge key={idx} variant="outline">{keyword}</Badge>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}
