import React, { useState } from 'react';

export default function TutorCard({ report }) {
  const [copiedIndex, setCopiedIndex] = useState(null);

  // Standby state before the Tutor Agent completes synthesis
  if (!report || !report.executive_summary) {
    return (
      <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 h-full flex flex-col items-center justify-center opacity-50 min-h-[300px]">
        <svg className="w-12 h-12 text-gray-600 mb-4 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        <span className="text-gray-400 font-mono text-sm">Awaiting Intelligence Synthesis...</span>
      </div>
    );
  }

  const handleCopy = (code, index) => {
    navigator.clipboard.writeText(code);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const isOptimal = report.system_health === 'OPTIMAL';

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 h-full flex flex-col shadow-lg overflow-hidden min-h-[400px]">
      
      {/* Header Widget */}
      <div className="p-4 border-b border-gray-700 bg-gray-850 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-gray-200 flex items-center gap-2">
            <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            Final Intelligence Report
          </h3>
          <p className="text-xs text-gray-500 font-mono mt-1">AI OS Synthesis & Resolution</p>
        </div>
        
        {/* Health Status Indicator */}
        <div className={`px-3 py-1 rounded font-mono font-bold text-xs uppercase border ${
          isOptimal 
            ? 'bg-green-900/40 text-green-400 border-green-500 shadow-[0_0_8px_rgba(34,197,94,0.3)]' 
            : 'bg-red-900/40 text-red-400 border-red-500 shadow-[0_0_8px_rgba(239,68,68,0.3)]'
        }`}>
          {report.system_health}
        </div>
      </div>

      {/* Main Content Area */}
      <div className="p-4 overflow-y-auto custom-scrollbar flex-grow bg-gray-900">
        
        {/* Executive Summary */}
        <div className="mb-6 bg-gray-800 p-4 rounded border-l-4 border-purple-500">
          <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider mb-2">Executive Summary</h4>
          <p className="text-sm text-gray-300 leading-relaxed">
            {report.executive_summary}
          </p>
        </div>

        {/* Actionable Patches List */}
        {report.actionable_patches && report.actionable_patches.length > 0 && (
          <div>
            <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Recommended Actions</h4>
            <div className="space-y-4">
              {report.actionable_patches.map((patch, idx) => (
                <div key={idx} className="bg-black/40 border border-gray-700 rounded overflow-hidden">
                  
                  {/* Patch Meta Information */}
                  <div className="p-3 bg-gray-850 border-b border-gray-700">
                    <span className="font-mono text-xs text-blue-400 block mb-1">Target: {patch.file}</span>
                    <p className="text-sm text-gray-300">{patch.explanation}</p>
                  </div>

                  {/* Code Snippet with Copy Button */}
                  {patch.code_snippet && (
                    <div className="relative group">
                      <div className="absolute right-2 top-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button 
                          onClick={() => handleCopy(patch.code_snippet, idx)}
                          className="bg-gray-700 hover:bg-gray-600 text-gray-200 text-xs px-2 py-1 rounded transition-colors"
                        >
                          {copiedIndex === idx ? 'Copied!' : 'Copy'}
                        </button>
                      </div>
                      <pre className="p-4 text-sm font-mono text-green-400 overflow-x-auto whitespace-pre-wrap">
                        <code>{patch.code_snippet}</code>
                      </pre>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Historical Context (Optional from Memory Agent) */}
        {report.historical_notes && report.historical_notes.length > 0 && (
          <div className="mt-6 border-t border-gray-700 pt-4">
            <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2 flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Memory Ledger Notes
            </h4>
            <ul className="space-y-1">
              {report.historical_notes.map((note, idx) => (
                <li key={idx} className="text-xs font-mono text-gray-400">
                  <span className="text-blue-500 mr-2">»</span>
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