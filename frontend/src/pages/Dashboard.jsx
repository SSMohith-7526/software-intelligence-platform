import React, { useState, useEffect, useRef, useCallback } from 'react';
import UploadBox from '../components/UploadBox';
import AgentPipeline from '../components/AgentPipeline';
// Note: You will import the individual cards (RepositoryCard, CompilerCard, etc.) here later.

export default function Dashboard() {
  // 1. Centralized OS State
  const [osState, setOsState] = useState({
    status: 'IDLE', // IDLE, UPLOADING, ANALYZING, COMPLETED, ERROR
    currentAgent: null,
    logs: [],
    astMetadata: {},
    securityVulnerabilities: [],
    performanceBottlenecks: [],
    tutorReport: null,
  });

  const [wsError, setWsError] = useState(null);
  const wsRef = useRef(null);
  const logsEndRef = useRef(null);

  // Auto-scroll logs to bottom as they stream in
  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [osState.logs]);

  // 2. The WebSocket Connection Manager
  const connectToContextBus = useCallback((repositoryPayload) => {
    // Connect to the FastAPI WebSocket endpoint we built in main.py
    const wsUrl = `ws://localhost:8000/api/ws/analyze`;
    const socket = new WebSocket(wsUrl);
    wsRef.current = socket;

    socket.onopen = () => {
      setOsState((prev) => ({ ...prev, status: 'ANALYZING', logs: ['System Boot: Connected to Context Bus...'] }));
      // Send the initial file payload to kick off the LangGraph pipeline
      socket.send(JSON.stringify(repositoryPayload));
    };

    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        
        // Dynamically merge the incoming state from LangGraph into the React State
        setOsState((prevState) => ({
          ...prevState,
          currentAgent: payload.current_agent || prevState.currentAgent,
          status: payload.execution_status === 'COMPLETED' ? 'COMPLETED' : 'ANALYZING',
          // Append new logs safely
          logs: payload.logs ? [...prevState.logs, ...payload.logs] : prevState.logs,
          // Update structural data if the backend provided it in this tick
          astMetadata: payload.ast_metadata || prevState.astMetadata,
          securityVulnerabilities: payload.security_vulnerabilities || prevState.securityVulnerabilities,
          performanceBottlenecks: payload.performance_bottlenecks || prevState.performanceBottlenecks,
          tutorReport: payload.final_intelligence_report || prevState.tutorReport,
        }));
      } catch (err) {
        console.error("Failed to parse OS Context Bus stream:", err);
      }
    };

    socket.onerror = (error) => {
      setWsError("Connection to AI OS Master Control lost. Ensure backend is running.");
      setOsState((prev) => ({ ...prev, status: 'ERROR' }));
    };

    socket.onclose = () => {
      if (osState.status !== 'COMPLETED') {
        console.warn("WebSocket closed prematurely.");
      }
    };
  }, [osState.status]);

  // 3. The Upload Handler (Bridges REST to WebSocket)
  const handleFileUpload = async (file) => {
    setOsState((prev) => ({ ...prev, status: 'UPLOADING', logs: ['Uploading payload to OS Sandbox...'] }));
    setWsError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Upload failed');
      }

      const { payload } = await response.json();
      
      // Once upload REST call succeeds, immediately open the WebSocket and pass the payload
      connectToContextBus(payload);

    } catch (error) {
      setWsError(`Ingestion Error: ${error.message}`);
      setOsState((prev) => ({ ...prev, status: 'ERROR' }));
    }
  };

  // Cleanup WebSocket on unmount
  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col p-6 font-sans">
      <header className="mb-8 border-b border-gray-700 pb-4">
        <h1 className="text-3xl font-bold text-blue-400">AI OS Master Control</h1>
        <p className="text-gray-400 text-sm mt-1">Multi-Agent System Pipeline Simulator</p>
      </header>

      {wsError && (
        <div className="bg-red-900 border-l-4 border-red-500 p-4 mb-6">
          <p className="text-red-200">{wsError}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-grow">
        
        {/* Left Column: Input and Pipeline Visualizer */}
        <div className="lg:col-span-1 flex flex-col gap-6">
          {osState.status === 'IDLE' || osState.status === 'ERROR' ? (
            <UploadBox onUpload={handleFileUpload} />
          ) : (
            <div className="bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-700 h-full">
              <h2 className="text-xl font-semibold mb-4 text-green-400">Live Execution Pipeline</h2>
              {/* This component will visually show which agent is active */}
              <AgentPipeline currentAgent={osState.currentAgent} status={osState.status} />
              
              <div className="mt-6 bg-black p-3 rounded font-mono text-xs h-64 overflow-y-auto text-green-500">
                {osState.logs.map((log, idx) => (
                  <div key={idx} className="mb-1">{`> ${log}`}</div>
                ))}
                <div ref={logsEndRef} />
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Agent Dashboards (Data Rendering) */}
        <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Placeholder for Agent Cards. We will build these next to consume the osState.
            Example:
            <RepositoryCard fileCount={Object.keys(osState.astMetadata).length} />
            <CompilerCard astData={osState.astMetadata} />
            <RuntimeCard 
               bottlenecks={osState.performanceBottlenecks} 
               vulns={osState.securityVulnerabilities} 
            />
            <TutorCard report={osState.tutorReport} />
          */}
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700 flex items-center justify-center text-gray-500">
            {osState.status === 'IDLE' ? 'Awaiting Repository Ingestion...' : 'Agents actively analyzing Context Bus...'}
          </div>
        </div>

      </div>
    </div>
  );
}