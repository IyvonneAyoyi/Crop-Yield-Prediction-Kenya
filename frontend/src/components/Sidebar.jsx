import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Target, BarChart2, Leaf, CloudRain, ShieldAlert, History, Info } from 'lucide-react';

const Sidebar = () => {
  const activeClassName = "flex items-center space-x-3 p-3 bg-white/10 rounded-md border-l-4 border-secondary-fixed text-white font-medium transition-colors";
  const inactiveClassName = "flex items-center space-x-3 p-3 hover:bg-white/5 rounded-md text-gray-300 font-medium transition-colors";

  return (
    <div className="w-[var(--spacing-sidebar-width)] h-screen bg-primary-container text-on-primary fixed left-0 top-0 p-4 flex flex-col">
      <div className="flex items-center space-x-2 mb-8 px-2 mt-4">
        <Leaf size={24} className="fill-current text-secondary-fixed" />
        <h1 className="text-xl font-bold font-manrope leading-tight">CropYield<br/>Kenya</h1>
      </div>
      
      <nav className="flex flex-col space-y-2 flex-1 overflow-y-auto">
        <NavLink to="/overview" className={({ isActive }) => isActive ? activeClassName : inactiveClassName}>
          <LayoutDashboard size={18} />
          <span>Overview</span>
        </NavLink>
        <NavLink to="/predict-yield" className={({ isActive }) => isActive ? activeClassName : inactiveClassName}>
          <Target size={18} />
          <span>Predict Production</span>
        </NavLink>
        <NavLink to="/dashboard" className={({ isActive }) => isActive ? activeClassName : inactiveClassName}>
          <BarChart2 size={18} />
          <span>County Insights</span>
        </NavLink>
        <NavLink to="/analytics" className={({ isActive }) => isActive ? activeClassName : inactiveClassName}>
          <BarChart2 size={18} />
          <span>Crop Analytics</span>
        </NavLink>
        <NavLink to="/environmental-data" className={({ isActive }) => isActive ? activeClassName : inactiveClassName}>
          <CloudRain size={18} />
          <span>Environmental Data</span>
        </NavLink>
        <NavLink to="/model-performance" className={({ isActive }) => isActive ? activeClassName : inactiveClassName}>
          <ShieldAlert size={18} />
          <span>Model Performance</span>
        </NavLink>
        <NavLink to="/history" className={({ isActive }) => isActive ? activeClassName : inactiveClassName}>
          <History size={18} />
          <span>Prediction History</span>
        </NavLink>
        <NavLink to="/about" className={({ isActive }) => isActive ? activeClassName : inactiveClassName}>
          <Info size={18} />
          <span>About</span>
        </NavLink>
      </nav>

      <div className="mt-auto pt-4 flex items-center space-x-2 px-2">
        <div className="w-2 h-2 bg-secondary-fixed rounded-full animate-pulse"></div>
        <span className="text-sm font-inter text-gray-300">API Online</span>
      </div>
    </div>
  );
};

export default Sidebar;
