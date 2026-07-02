import React from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';

export default function App() {
  return (
    <div className="flex h-screen bg-gray-900 text-gray-100 overflow-hidden font-sans">
      {/* Fixed Sidebar for OS Navigation */}
      <Sidebar />
      
      {/* Main Content Area - Scrollable */}
      <main className="flex-1 overflow-y-auto custom-scrollbar">
        <Dashboard />
      </main>
    </div>
  );
}