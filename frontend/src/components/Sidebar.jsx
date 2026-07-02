import React, { useState } from 'react';

export default function Sidebar() {
  const [isExpanded, setIsExpanded] = useState(false);

  const navItems = [
    { id: 'dashboard', label: 'Live Pipeline', icon: 'M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z' },
    { id: 'memory', label: 'Memory Ledger', icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' },
    { id: 'settings', label: 'OS Settings', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }
  ];

  return (
    <aside 
      className={`${isExpanded ? 'w-64' : 'w-20'} transition-all duration-300 ease-in-out bg-gray-950 border-r border-gray-800 flex flex-col`}
      onMouseEnter={() => setIsExpanded(true)}
      onMouseLeave={() => setIsExpanded(false)}
    >
      {/* Branding Header */}
      <div className="h-16 flex items-center justify-center border-b border-gray-800 px-4">
        <div className="flex items-center gap-3 w-full">
          <div className="w-8 h-8 rounded bg-blue-600 flex items-center justify-center flex-shrink-0 shadow-[0_0_15px_rgba(37,99,235,0.5)]">
            <span className="font-bold text-white font-mono text-sm">AI</span>
          </div>
          <span className={`font-bold text-gray-200 whitespace-nowrap transition-opacity duration-300 ${isExpanded ? 'opacity-100' : 'opacity-0 hidden'}`}>
            System OS
          </span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 py-6 flex flex-col gap-2 px-3">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`flex items-center gap-4 px-3 py-3 rounded-lg transition-all duration-200 group
              ${item.id === 'dashboard' ? 'bg-gray-800 text-blue-400' : 'text-gray-500 hover:bg-gray-900 hover:text-gray-300'}`}
          >
            <svg className="w-6 h-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={item.icon} />
            </svg>
            <span className={`font-medium whitespace-nowrap transition-opacity duration-300 ${isExpanded ? 'opacity-100' : 'opacity-0 hidden'}`}>
              {item.label}
            </span>
          </button>
        ))}
      </nav>

      {/* Footer / Status Indicator */}
      <div className="p-4 border-t border-gray-800">
        <div className="flex items-center gap-3 w-full justify-center lg:justify-start">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
          </span>
          <span className={`text-xs text-gray-500 font-mono whitespace-nowrap transition-opacity duration-300 ${isExpanded ? 'opacity-100' : 'opacity-0 hidden'}`}>
            Engine Online
          </span>
        </div>
      </div>
    </aside>
  );
}