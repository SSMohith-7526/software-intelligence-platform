import React from 'react';

// Define the exact order of the LangGraph pipeline matching workflow.py
const PIPELINE_STAGES = [
  { id: 'RepositoryAgent', label: '1. Ingestion & AST Map' },
  { id: 'GraphAgent', label: '2. Topological Graph' },
  { id: 'CompilerAgent', label: '3. Compiler & Syntax' },
  { id: 'RuntimeAgent', label: '4. Runtime Sim' },
  { id: 'MemoryAgent', label: '5. Memory Ledger' },
  { id: 'TutorAgent', label: '6. Intelligence Synthesis' }
];

export default function AgentPipeline({ currentAgent, status }) {
  // Determine the numerical index of the currently active agent
  const currentIndex = PIPELINE_STAGES.findIndex(stage => stage.id === currentAgent);

  return (
    <div className="w-full bg-gray-900 rounded-lg p-4 font-sans">
      <div className="flex flex-col space-y-2">
        {PIPELINE_STAGES.map((stage, index) => {
          // Determine the visual state of the specific agent node
          let stageStatus = 'PENDING'; // Default
          
          if (status === 'COMPLETED') {
            stageStatus = 'COMPLETED';
          } else if (status === 'ERROR') {
            stageStatus = index <= currentIndex ? 'ERROR' : 'PENDING';
          } else {
            if (index < currentIndex) stageStatus = 'COMPLETED';
            if (index === currentIndex) stageStatus = 'ACTIVE';
          }

          return (
            <div key={stage.id} className="flex items-center space-x-4">
              {/* Status Indicator Icon */}
              <div className="flex-shrink-0 mt-1">
                <StatusIcon status={stageStatus} />
              </div>

              {/* Agent Label & Line Connection */}
              <div className="flex-grow flex flex-col">
                <span className={`text-sm font-medium transition-colors duration-300 ${getTextColor(stageStatus)}`}>
                  {stage.label}
                </span>
                
                {/* Visual connecting line to the next agent (hide on the last item) */}
                {index < PIPELINE_STAGES.length - 1 && (
                  <div className={`h-4 w-0.5 ml-2 mt-1 rounded transition-colors duration-500 ${getLineColor(stageStatus)}`} />
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// --- Helper UI Functions ---

function StatusIcon({ status }) {
  switch (status) {
    case 'COMPLETED':
      return (
        <div className="h-5 w-5 rounded-full bg-green-500 flex items-center justify-center shadow-[0_0_8px_rgba(34,197,94,0.6)]">
          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
          </svg>
        </div>
      );
    case 'ACTIVE':
      return (
        <div className="relative flex h-5 w-5 items-center justify-center">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.9)]"></span>
        </div>
      );
    case 'ERROR':
      return (
        <div className="h-5 w-5 rounded-full bg-red-500 flex items-center justify-center shadow-[0_0_8px_rgba(239,68,68,0.6)]">
          <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
      );
    case 'PENDING':
    default:
      return (
        <div className="h-5 w-5 rounded-full border-2 border-gray-600 bg-gray-800"></div>
      );
  }
}

function getTextColor(status) {
  switch (status) {
    case 'COMPLETED': return 'text-green-400';
    case 'ACTIVE': return 'text-blue-300 font-bold';
    case 'ERROR': return 'text-red-400';
    case 'PENDING': return 'text-gray-500';
    default: return 'text-gray-500';
  }
}

function getLineColor(status) {
  switch (status) {
    case 'COMPLETED': return 'bg-green-500/50';
    case 'ACTIVE': return 'bg-blue-500/50 animate-pulse';
    case 'ERROR': return 'bg-red-500/50';
    case 'PENDING': return 'bg-gray-700';
    default: return 'bg-gray-700';
  }
}