import { useApi } from "../hooks/useApi";
import KpiCard from "../components/KpiCard";
import Loader from "../components/Loader";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid,
  PieChart, Pie, Cell, Legend,
} from "recharts";

const COLORS = ["#6366f1", "#06b6d4", "#f59e0b", "#ef4444", "#10b981", "#8b5cf6", "#ec4899", "#14b8a6"];

export default function Overview() {
  const { data: stats, loading: l1 } = useApi("/stats");
  const { data: sources, loading: l2 } = useApi("/sources");
  const { data: categories, loading: l3 } = useApi("/trends/categories?days=30");

  if (l1 || l2 || l3) return <Loader />;

  return (
    <div className="page">
      <h1>Overview</h1>

      <div className="kpi-grid">
        <KpiCard title="Total Articles" value={stats.total_articles} />
        <KpiCard title="Sources" value={stats.total_sources} />
        <KpiCard title="Languages" value={stats.total_languages} />
        <KpiCard
          title="Latest Scrape"
          value={stats.latest_scrape ? new Date(stats.latest_scrape).toLocaleString() : "—"}
        />
      </div>

      <div className="charts-row">
        <div className="chart-card">
          <h2>Articles per Source</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sources}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="source" stroke="#aaa" />
              <YAxis stroke="#aaa" />
              <Tooltip contentStyle={{ background: "#1e1e2e", border: "1px solid #333" }} />
              <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                {sources.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h2>Top Categories</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={categories} dataKey="count" nameKey="category" cx="50%" cy="50%" outerRadius={100} label>
                {categories.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: "#1e1e2e", border: "1px solid #333" }} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
