import { useState } from "react";
import { useApi } from "../hooks/useApi";
import Loader from "../components/Loader";

export default function Articles() {
  const [source, setSource] = useState("");
  const [page, setPage] = useState(0);
  const limit = 15;

  const query = `/articles?limit=${limit}&offset=${page * limit}${source ? `&source=${source}` : ""}`;
  const { data, loading } = useApi(query);
  const { data: sources } = useApi("/sources");

  if (loading || !data) return <Loader />;

  const totalPages = Math.ceil(data.total / limit);

  return (
    <div className="page">
      <div className="page-header">
        <h1>Articles ({data.total})</h1>
        <select className="filter-select" value={source} onChange={(e) => { setSource(e.target.value); setPage(0); }}>
          <option value="">All sources</option>
          {sources?.map((s) => (
            <option key={s.source} value={s.source}>{s.source}</option>
          ))}
        </select>
      </div>

      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Source</th>
              <th>Category</th>
              <th>Language</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {data.articles.map((a) => (
              <tr key={a.article_id}>
                <td>
                  <a href={a.url} target="_blank" rel="noopener noreferrer" className="article-link">
                    {a.title.length > 80 ? a.title.slice(0, 80) + "..." : a.title}
                  </a>
                </td>
                <td><span className="badge">{a.source}</span></td>
                <td>{a.category || "—"}</td>
                <td>{a.language || "—"}</td>
                <td>{a.published_at ? new Date(a.published_at).toLocaleDateString() : "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="pagination">
          <button className="btn" disabled={page === 0} onClick={() => setPage(page - 1)}>Previous</button>
          <span className="page-info">{page + 1} / {totalPages}</span>
          <button className="btn" disabled={page >= totalPages - 1} onClick={() => setPage(page + 1)}>Next</button>
        </div>
      </div>
    </div>
  );
}
