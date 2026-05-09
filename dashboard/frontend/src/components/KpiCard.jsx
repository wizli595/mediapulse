export default function KpiCard({ title, value, subtitle }) {
  return (
    <div className="kpi-card">
      <span className="kpi-title">{title}</span>
      <span className="kpi-value">{value ?? "—"}</span>
      {subtitle && <span className="kpi-subtitle">{subtitle}</span>}
    </div>
  );
}
