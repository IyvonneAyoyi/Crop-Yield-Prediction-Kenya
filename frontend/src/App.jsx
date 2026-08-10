import React from 'react';
import { BrowserRouter as Router, Routes, Route, Outlet, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import TopNav from './components/TopNav';
import Dashboard from './components/Dashboard';
import Home from './pages/Home';
import { 
  Overview, 
  PredictProduction, 
  CropAnalytics, 
  EnvironmentalData, 
  ModelPerformance, 
  PredictionHistory, 
  About 
} from './pages/DashboardPages';

const DashboardLayout = () => {
  return (
    <div className="min-h-screen bg-background flex">
      <Sidebar />
      <div className="ml-[var(--spacing-sidebar-width)] flex-1 flex flex-col min-h-screen">
        <TopNav />
        <main className="flex-1 overflow-auto bg-surface-container-low">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        
        <Route element={<DashboardLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/overview" element={<Overview />} />
          <Route path="/predict-yield" element={<PredictProduction />} />
          <Route path="/analytics" element={<CropAnalytics />} />
          <Route path="/environmental-data" element={<EnvironmentalData />} />
          <Route path="/model-performance" element={<ModelPerformance />} />
          <Route path="/history" element={<PredictionHistory />} />
          <Route path="/about" element={<About />} />
          
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;