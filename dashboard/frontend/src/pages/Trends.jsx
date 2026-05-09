import { useState } from "react";
import { useApi } from "../hooks/useApi";
import Loader from "../components/Loader";
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend,
} from "recharts";

const COLORS = ["#6366f1", "#06b6d4", "#f59e0b", "#ef4444", "#10b981", "#8b5cf6"];

export default function Trends() {
  const [days, setDays] = useState(30);
  const { data, loading } = useApi(`/trends?days=${days}`);

  if (loading) return <Loader />;

  const sources = [...new Set(data.map((d) => d.source))];
  const dates = [...new Set(data.map((d) => d.date))].sort();

  const chartData = dates.map((date) => {
    const row = { date };
    sources.forEach((src) => {
      const match = data.find((d) => d.date === date && d.source === src);
      row[src] = match ? match.count : 0;
    });
    return row;
  });

  return (
    <div className="page">
      <div className="page-header">
        <h1>Trends</h1>
        <div className="filter-group">
          {[7, 14, 30, 90].map((d) => (
            <button key={d} className={days === d ? "btn active" : "btn"} onClick={() => setDays(d)}>
              {d}d
            </button>
          ))}
        </div>
      </div>

      <div className="chart-card full">
        <h2>Articles per Day by Source</h2>
        <ResponsiveContainer width="100%" height={400}>
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis dataKey="date" stroke="#aaa" />
            <YAxis stroke="#aaa" />
            <Tooltip contentStyle={{ background: "#1e1e2e", border: "1px solid #333" }} />
            <Legend />
            {sources.map((src, i) => (
              <Area
                key={src}
                type="monotone"
                dataKey={src}
                stackId="1"
                stroke={COLORS[i % COLORS.length]}
                fill={COLORS[i % COLORS.length]}
                fillOpacity={0.6}
              />
            ))}
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
