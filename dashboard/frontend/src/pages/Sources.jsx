import { useApi } from "../hooks/useApi";
import Loader from "../components/Loader";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell,
} from "recharts";

const COLORS = ["#6366f1", "#06b6d4", "#f59e0b", "#ef4444", "#10b981", "#8b5cf6", "#ec4899", "#14b8a6"];

export default function Sources() {
  const { data, loading } = useApi("/sources");

  if (loading) return <Loader />;

  return (
    <div className="page">
      <h1>Sources</h1>

      <div className="chart-card full">
        <h2>Articles per Source</h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={data} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis type="number" stroke="#aaa" />
            <YAxis type="category" dataKey="source" stroke="#aaa" width={100} />
            <Tooltip contentStyle={{ background: "#1e1e2e", border: "1px solid #333" }} />
            <Bar dataKey="count" radius={[0, 6, 6, 0]}>
              {data.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="table-card">
        <h2>Source Details</h2>
        <table>
          <thead>
            <tr>
              <th>Source</th>
              <th>Articles</th>
              <th>Latest Article</th>
            </tr>
          </thead>
          <tbody>
            {data.map((s) => (
              <tr key={s.source}>
                <td className="source-name">{s.source}</td>
                <td>{s.count}</td>
                <td>{s.latest ? new Date(s.latest).toLocaleString() : "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
