import React, { useState } from 'react';

export default function RuntimeCard({ bottlenecks = [], vulns = [] }) {
  const [activeTab, setActiveTab] = useState('security'); // 'security' or 'performance'

  const totalIssues = bottlenecks.length + vulns.length;

  // Standby state before the Runtime Agent has populated the Context Bus
  if (totalIssues === 0) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 h-full flex flex-col items-center justify-center opacity-50 min-h-[300px]">
        <svg className="w-12 h-12 text-gray-600 mb-4 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <span className="text-gray-400 font-mono text-sm">Awaiting Runtime Simulation...</span>
      </div>
    );
  }

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 h-full flex flex-col shadow-lg overflow-hidden min-h-[400px]">
      
      {/* Header Widget */}
      <div className="p-4 border-b border-gray-700 bg-gray-850 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-gray-200 flex items-center gap-2">
            <svg className="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Runtime Analysis
          </h3>
          <p className="text-xs text-gray-500 font-mono mt-1">Simulated Execution Engine</p>
        </div>
        
        <div className="flex gap-2">
          {vulns.length > 0 && (
            <span className="bg-red-900/40 border border-red-500 text-red-400 text-xs px-2 py-1 rounded font-mono font-bold animate-pulse">
              {vulns.length} Security Risk{vulns.length > 1 ? 's' : ''}
            </span>
          )}
          {bottlenecks.length > 0 && (
            <span className="bg-yellow-900/40 border border-yellow-500 text-yellow-400 text-xs px-2 py-1 rounded font-mono font-bold">
              {bottlenecks.length} Bottleneck{bottlenecks.length > 1 ? 's' : ''}
            </span>
          )}
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="flex border-b border-gray-700 bg-gray-900/50">
        <button
          className={`flex-1 py-2 text-sm font-bold tracking-wider uppercase transition-colors ${
            activeTab === 'security' 
              ? 'text-red-400 border-b-2 border-red-500 bg-red-900/10' 
              : 'text-gray-500 hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('security')}
        >
          Security ({vulns.length})
        </button>
        <button
          className={`flex-1 py-2 text-sm font-bold tracking-wider uppercase transition-colors ${
            activeTab === 'performance' 
              ? 'text-yellow-400 border-b-2 border-yellow-500 bg-yellow-900/10' 
              : 'text-gray-500 hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('performance')}
        >
          Performance ({bottlenecks.length})
        </button>
      </div>

      {/* Interactive List View */}
      <div className="p-4 overflow-y-auto max-h-96 custom-scrollbar flex-grow bg-gray-900">
        
        {/* Security Tab Content */}
        {activeTab === 'security' && (
          <ul className="space-y-3">
            {vulns.length === 0 ? (
              <li className="text-gray-500 text-sm italic font-mono text-center mt-4">No severe security risks detected in simulated execution.</li>
            ) : (
              vulns.map((vuln, idx) => (
                <li key={idx} className="bg-gray-800 border-l-4 border-red-500 p-3 rounded shadow-md">
                  <div className="flex justify-between items-start mb-2">
                    <span className="font-mono text-sm text-gray-300 break-all">{vuln.file}</span>
                    <SeverityBadge severity={vuln.severity} />
                  </div>
                  <p className="text-sm text-red-200 mt-1">{vuln.risk}</p>
                </li>
              ))
            )}
          </ul>
        )}

        {/* Performance Tab Content */}
        {activeTab === 'performance' && (
          <ul className="space-y-3">
            {bottlenecks.length === 0 ? (
              <li className="text-gray-500 text-sm italic font-mono text-center mt-4">No critical performance bottlenecks detected.</li>
            ) : (
              bottlenecks.map((btnk, idx) => (
                <li key={idx} className="bg-gray-800 border-l-4 border-yellow-500 p-3 rounded shadow-md">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex flex-col">
                      <span className="font-mono text-sm text-gray-300">{btnk.file}</span>
                      {btnk.function && (
                        <span className="font-mono text-xs text-blue-400">ƒ {btnk.function}</span>
                      )}
                    </div>
                    {btnk.complexity && (
                      <span className="bg-yellow-900/50 border border-yellow-700 text-yellow-300 text-xs px-2 py-1 rounded font-mono font-bold">
                        {btnk.complexity}
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-yellow-200 mt-1">{btnk.issue || btnk.details}</p>
                </li>
              ))
            )}
          </ul>
        )}
      </div>
    </div>
  );
}

// Helper component for standardizing security badge colors
function SeverityBadge({ severity }) {
  const normalized = (severity || 'LOW').toUpperCase();
  
  let colorClasses = 'bg-gray-900 text-gray-400 border-gray-700'; // Fallback
  
  if (normalized === 'CRITICAL') {
    colorClasses = 'bg-red-900 text-red-100 border-red-500 shadow-[0_0_8px_rgba(239,68,68,0.8)] animate-pulse';
  } else if (normalized === 'HIGH') {
    colorClasses = 'bg-orange-900 text-orange-200 border-orange-500';
  } else if (normalized === 'MEDIUM') {
    colorClasses = 'bg-yellow-900 text-yellow-200 border-yellow-500';
  } else if (normalized === 'LOW') {
    colorClasses = 'bg-blue-900 text-blue-200 border-blue-500';
  }

  return (
    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border uppercase tracking-wider ${colorClasses}`}>
      {normalized}
    </span>
  );
}