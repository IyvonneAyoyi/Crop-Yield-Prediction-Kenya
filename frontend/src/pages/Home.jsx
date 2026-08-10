import React from 'react';
import { Link } from 'react-router-dom';
import { Leaf, ArrowRight, Map } from 'lucide-react';

const Home = () => {
  return (
    <div className="min-h-screen bg-surface flex flex-col font-manrope">
      {/* Header */}
      <header className="w-full px-8 py-6 flex justify-between items-center bg-surface border-b border-surface-variant">
        <div className="flex items-center space-x-2">
          <div className="text-primary">
            <Leaf size={28} className="fill-current text-primary" />
          </div>
          <span className="text-xl font-extrabold text-on-surface tracking-tight">CropYield Kenya</span>
        </div>
        
        <nav className="hidden md:flex space-x-8 text-on-surface-variant font-medium">
          <a href="#" className="hover:text-primary transition-colors">How it Works</a>
          <a href="#" className="hover:text-primary transition-colors">Data Sources</a>
          <a href="#" className="text-on-surface border-b-2 border-primary pb-1 font-semibold">Overview</a>
        </nav>
        
        <button className="p-2 text-on-surface md:hidden">
          <div className="w-6 h-0.5 bg-current mb-1.5"></div>
          <div className="w-6 h-0.5 bg-current mb-1.5"></div>
          <div className="w-6 h-0.5 bg-current"></div>
        </button>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col lg:flex-row items-center justify-between px-8 lg:px-24 py-12 gap-12 max-w-[var(--spacing-container-max)] mx-auto w-full">
        {/* Left Text */}
        <div className="lg:w-1/2 space-y-6">
          <h1 className="text-5xl lg:text-6xl font-extrabold text-primary leading-tight tracking-tight">
            Predict Kenya's<br/>Harvest<br/>With Data.
          </h1>
          <p className="text-lg text-on-surface-variant max-w-lg leading-relaxed">
            Empowering agricultural resilience through high-precision predictive intelligence. We synthesize decades of environmental statistics, real-time satellite telemetry, and advanced machine learning models to forecast crop yields across Kenya's diverse counties.
          </p>
          <div className="flex flex-wrap gap-4 pt-4">
            <Link to="/dashboard" className="bg-primary text-on-primary px-6 py-3 rounded-md font-semibold flex items-center space-x-2 hover:bg-primary-container transition-colors">
              <span>START PREDICTION</span>
              <ArrowRight size={18} />
            </Link>
            <Link to="/dashboard" className="bg-surface-container-low text-on-surface border border-outline-variant px-6 py-3 rounded-md font-semibold flex items-center space-x-2 hover:bg-surface-container transition-colors">
              <span>EXPLORE KENYA</span>
              <Map size={18} />
            </Link>
          </div>
        </div>

        {/* Right Graphic Placeholder */}
        <div className="lg:w-1/2 w-full flex justify-center">
          <div className="w-full max-w-lg aspect-[4/3] bg-white rounded-2xl shadow-xl border border-surface-variant relative overflow-hidden flex items-center justify-center p-6">
             <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(#14532d 1px, transparent 1px)', backgroundSize: '20px 20px' }}></div>
             
             {/* Mock Map element */}
             <div className="absolute right-6 top-8 bg-white shadow-lg rounded-xl p-4 border border-surface-variant z-10 w-64">
               <div className="flex items-center space-x-2 text-xs font-inter text-outline font-semibold mb-2 uppercase">
                 <span className="w-4 h-4 text-primary"><Leaf size={14} /></span>
                 <span>Maize Prediction</span>
               </div>
               <h3 className="text-lg font-bold text-on-surface mb-1">Uasin Gishu</h3>
               <div className="flex justify-between items-end">
                 <div>
                   <p className="text-2xl font-extrabold text-on-surface">182,430</p>
                   <p className="text-sm text-on-surface-variant">tonnes</p>
                 </div>
                 <div className="bg-primary-fixed-dim text-on-primary-fixed px-2 py-1 rounded text-xs font-bold">
                   +8.4% outlook
                 </div>
               </div>
             </div>

             <div className="absolute left-6 bottom-8 bg-white shadow-lg rounded-xl p-4 border border-surface-variant z-10 w-64">
               <div className="flex items-center space-x-2 text-xs font-inter text-outline font-semibold mb-2 uppercase">
                 <span className="w-4 h-4 text-secondary"><Map size={14} /></span>
                 <span>Current Status</span>
               </div>
               <h3 className="text-lg font-bold text-on-surface mb-3">Trans Nzoia</h3>
               <div className="flex justify-between items-center text-sm border-b border-surface-variant pb-2 mb-2">
                 <span className="text-on-surface-variant">Precipitation</span>
                 <span className="font-semibold">Adequate</span>
               </div>
               <div className="flex justify-between items-center text-sm">
                 <span className="text-on-surface-variant">Soil Moisture</span>
                 <span className="font-semibold">Optimal</span>
               </div>
             </div>
          </div>
        </div>
      </main>

      {/* Stats Footer */}
      <footer className="bg-primary text-on-primary w-full py-12 mt-auto">
        <div className="max-w-[var(--spacing-container-max)] mx-auto px-8 grid grid-cols-2 md:grid-cols-4 gap-8 text-center divide-x divide-primary-container">
          <div>
            <p className="text-4xl md:text-5xl font-extrabold mb-2 text-secondary-fixed">42</p>
            <p className="text-xs font-inter tracking-widest uppercase text-on-primary-container">Counties Analyzed</p>
          </div>
          <div>
            <p className="text-4xl md:text-5xl font-extrabold mb-2 text-secondary-fixed">8</p>
            <p className="text-xs font-inter tracking-widest uppercase text-on-primary-container">Key Crops</p>
          </div>
          <div>
            <p className="text-4xl md:text-5xl font-extrabold mb-2 text-secondary-fixed">765</p>
            <p className="text-xs font-inter tracking-widest uppercase text-on-primary-container">Data Records</p>
          </div>
          <div>
            <p className="text-4xl md:text-5xl font-extrabold mb-2 text-secondary-fixed">4</p>
            <p className="text-xs font-inter tracking-widest uppercase text-on-primary-container">ML Models Deployed</p>
          </div>
        </div>
      </footer>
      
      {/* Copyright */}
      <div className="bg-surface py-4 text-center text-sm text-on-surface-variant">
        &copy; 2024 CropYield Kenya. Agricultural Intelligence.
      </div>
    </div>
  );
};

export default Home;