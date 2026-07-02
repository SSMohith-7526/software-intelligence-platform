import React from 'react';

export default function RepositoryCard({ astData = {} }) {
  const files = Object.keys(astData);
  const totalFiles = files.length;

  if (totalFiles === 0) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 h-full flex flex-col items-center justify-center opacity-50 min-h-[300px]">
        <svg className="w-12 h-12 text-gray-600 mb-4 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
        <span className="text-gray-400 font-mono text-sm">Awaiting Sandbox Initialization...</span>
      </div>
    );
  }

  // Calculate some basic directory statistics based on file extensions
  const stats = files.reduce((acc, file) => {
    const ext = file.split('.').pop() || 'unknown';
    acc[ext] = (acc[ext] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 h-full flex flex-col shadow-lg overflow-hidden min-h-[400px]">
      
      {/* Header Widget */}
      <div className="p-4 border-b border-gray-700 bg-gray-850 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-gray-200 flex items-center gap-2">
            <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
            </svg>
            Active Workspace
          </h3>
          <p className="text-xs text-gray-500 font-mono mt-1">Files injected into OS RAM</p>
        </div>
        
        <div className="bg-green-900/40 border border-green-500 text-green-400 text-xs px-2 py-1 rounded font-mono font-bold">
          {totalFiles} Files Active
        </div>
      </div>

      {/* Extension Statistics Bar */}
      <div className="px-4 py-2 bg-gray-900 border-b border-gray-800 flex gap-3 overflow-x-auto custom-scrollbar">
        {Object.entries(stats).map(([ext, count]) => (
          <span key={ext} className="text-xs font-mono bg-gray-800 text-gray-400 px-2 py-1 rounded border border-gray-700 whitespace-nowrap">
            .{ext}: <span className="text-blue-400 font-bold">{count}</span>
          </span>
        ))}
      </div>

      {/* File List */}
      <div className="p-4 overflow-y-auto custom-scrollbar flex-grow bg-gray-900">
        <ul className="space-y-1">
          {files.map((file, idx) => {
            const isPython = file.endsWith('.py');
            return (
              <li key={idx} className="flex items-center gap-2 py-1.5 px-2 hover:bg-gray-800 rounded group transition-colors">
                <svg className={`w-4 h-4 flex-shrink-0 ${isPython ? 'text-blue-400' : 'text-gray-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
                <span className={`font-mono text-sm truncate ${isPython ? 'text-gray-300' : 'text-gray-500 group-hover:text-gray-400'}`}>
                  {file}
                </span>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}