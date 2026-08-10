import React from 'react';
import { ArrowLeft, Search, Bell, Settings, User } from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';

const TopNav = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleBack = () => {
    navigate(-1);
  };

  return (
    <div className="h-16 border-b border-surface-variant flex items-center justify-between px-6 bg-surface">
      <div className="flex items-center space-x-4 flex-1">
        <button 
          onClick={handleBack} 
          className="text-on-surface-variant hover:text-primary transition-colors p-1"
          title="Go Back"
        >
          <ArrowLeft size={20} />
        </button>
        
        {/* Search Bar matching design */}
        <div className="flex items-center space-x-2 text-on-surface-variant bg-surface-container rounded-md px-3 py-1.5 w-64">
          <Search size={16} />
          <input 
            type="text" 
            placeholder="Search data, counties..." 
            className="bg-transparent border-none outline-none text-sm w-full text-on-surface placeholder:text-on-surface-variant/50"
          />
        </div>
      </div>
      
      <div className="flex items-center space-x-4 text-on-surface-variant">
        <button className="hover:text-primary transition-colors"><Bell size={18} /></button>
        <button className="hover:text-primary transition-colors"><Settings size={18} /></button>
        <button className="bg-surface-variant rounded-full p-1 hover:bg-surface-container-highest transition-colors">
          <User size={18} />
        </button>
      </div>
    </div>
  );
};

export default TopNav;
