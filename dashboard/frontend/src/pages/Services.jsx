const services = [
  {
    name: "Dashboard API",
    description: "FastAPI backend powering this dashboard",
    url: "http://localhost:8001",
    logo: "https://cdn.simpleicons.org/fastapi/009688",
  },
  {
    name: "Airflow",
    description: "Workflow orchestration & DAG scheduling",
    url: "http://localhost:8081",
    logo: "https://cdn.simpleicons.org/apacheairflow/017CEE",
  },
  {
    name: "Grafana",
    description: "Metrics dashboards & alerting",
    url: "http://localhost:3005",
    logo: "https://cdn.simpleicons.org/grafana/F46800",
  },
  {
    name: "Prometheus",
    description: "Time-series metrics collection",
    url: "http://localhost:9091",
    logo: "https://cdn.simpleicons.org/prometheus/E6522C",
  },
  {
    name: "MinIO",
    description: "S3-compatible object storage (data lake)",
    url: "http://localhost:9003",
    logo: "https://cdn.simpleicons.org/minio/C72C48",
  },
  {
    name: "Metabase",
    description: "Business intelligence & SQL analytics",
    url: "http://localhost:3004",
    logo: "https://cdn.simpleicons.org/metabase/509EE3",
  },
  {
    name: "Kafka",
    description: "Event streaming platform",
    url: "http://localhost:9093",
    logo: "https://cdn.simpleicons.org/apachekafka/ffffff",
  },
  {
    name: "PostgreSQL",
    description: "Data warehouse & relational storage",
    url: "http://localhost:5433",
    logo: "https://cdn.simpleicons.org/postgresql/336791",
  },
];

export default function Services() {
  return (
    <div className="page">
      <h1>Services</h1>
      <div className="services-grid">
        {services.map((s) => (
          <a
            key={s.name}
            href={s.url}
            target="_blank"
            rel="noopener noreferrer"
            className="service-card"
            data-desc={s.description}
          >
            <img src={s.logo} alt={s.name} className="service-logo" />
            <span className="service-name">{s.name}</span>
          </a>
        ))}
      </div>
    </div>
  );
}
