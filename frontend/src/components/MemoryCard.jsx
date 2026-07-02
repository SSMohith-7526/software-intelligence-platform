import React from 'react';

export default function MemoryCard({ tutorReport }) {
  const history = tutorReport?.historical_notes || [];

  if (history.length === 0) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 h-full flex flex-col items-center justify-center opacity-50 min-h-[300px]">
        <svg className="w-12 h-12 text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span className="text-gray-400 font-mono text-sm">Memory Ledger Empty...</span>
      </div>
    );
  }

  // Parse the historical context strings to categorize them
  const regressions = history.filter(note => note.includes('REGRESSION'));
  const resolutions = history.filter(note => note.includes('RESOLVED'));
  const active = history.filter(note => !note.includes('REGRESSION') && !note.includes('RESOLVED'));

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 h-full flex flex-col shadow-lg overflow-hidden min-h-[400px]">
      
      {/* Header Widget */}
      <div className="p-4 border-b border-gray-700 bg-gray-850 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-gray-200 flex items-center gap-2">
            <svg className="w-5 h-5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Cryptographic Memory Ledger
          </h3>
          <p className="text-xs text-gray-500 font-mono mt-1">Historical state tracking</p>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="p-4 overflow-y-auto custom-scrollbar flex-grow bg-gray-900 space-y-4">
        
        {/* New Regressions */}
        {regressions.length > 0 && (
          <div className="bg-red-900/10 border-l-4 border-red-500 p-3 rounded">
            <h4 className="text-xs font-bold text-red-400 uppercase tracking-wider mb-2">New Regressions</h4>
            <ul className="space-y-1">
              {regressions.map((note, idx) => (
                <li key={idx} className="text-xs font-mono text-gray-300">
                  {note.replace('REGRESSION DETECTED: ', '')}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Resolved Issues */}
        {resolutions.length > 0 && (
          <div className="bg-green-900/10 border-l-4 border-green-500 p-3 rounded">
            <h4 className="text-xs font-bold text-green-400 uppercase tracking-wider mb-2">Recently Resolved</h4>
            <ul className="space-y-1">
              {resolutions.map((note, idx) => (
                <li key={idx} className="text-xs font-mono text-gray-300 flex items-center gap-2">
                  <svg className="w-3 h-3 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="line-through opacity-70">
                    {note.replace('RESOLVED: ', '')}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Persisting Known Issues */}
        {active.length > 0 && (
          <div className="bg-gray-800 border-l-4 border-gray-600 p-3 rounded">
            <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Persistent Known Issues</h4>
            <ul className="space-y-1">
              {active.map((note, idx) => (
                <li key={idx} className="text-xs font-mono text-gray-400">
                  {note}
                </li>
              ))}
            </ul>
          </div>
        )}
        
      </div>
    </div>
  );
}