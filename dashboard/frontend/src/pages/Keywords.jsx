import { useApi } from "../hooks/useApi";
import Loader from "../components/Loader";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell,
} from "recharts";

const COLORS = ["#6366f1", "#06b6d4", "#f59e0b", "#ef4444", "#10b981", "#8b5cf6", "#ec4899", "#14b8a6"];

export default function Keywords() {
  const { data, loading } = useApi("/topics?limit=25");

  if (loading) return <Loader />;

  return (
    <div className="page">
      <h1>Top Keywords</h1>

      <div className="chart-card full">
        <h2>Most Frequent Keywords</h2>
        <ResponsiveContainer width="100%" height={500}>
          <BarChart data={data} layout="vertical" margin={{ left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis type="number" stroke="#aaa" />
            <YAxis type="category" dataKey="keyword" stroke="#aaa" width={120} tick={{ fontSize: 12 }} />
            <Tooltip contentStyle={{ background: "#1e1e2e", border: "1px solid #333" }} />
            <Bar dataKey="frequency" radius={[0, 6, 6, 0]}>
              {data.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
