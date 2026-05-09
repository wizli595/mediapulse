import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Overview from "./pages/Overview";
import Trends from "./pages/Trends";
import Sources from "./pages/Sources";
import Keywords from "./pages/Keywords";
import Articles from "./pages/Articles";

export default function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Sidebar />
        <main className="main">
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/trends" element={<Trends />} />
            <Route path="/sources" element={<Sources />} />
            <Route path="/keywords" element={<Keywords />} />
            <Route path="/articles" element={<Articles />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
