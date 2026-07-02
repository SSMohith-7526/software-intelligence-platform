import React, { useState, useRef } from 'react';

export default function UploadBox({ onUpload }) {
  const [isDragging, setIsDragging] = useState(false);
  const [localError, setLocalError] = useState(null);
  const fileInputRef = useRef(null);

  // Handle CSS state for drag events
  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  // Process the dropped file
  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    setLocalError(null);

    const droppedFiles = e.dataTransfer.files;
    validateAndUpload(droppedFiles);
  };

  // Process the clicked file
  const handleFileSelect = (e) => {
    setLocalError(null);
    const selectedFiles = e.target.files;
    validateAndUpload(selectedFiles);
  };

  const validateAndUpload = (files) => {
    if (files.length === 0) return;
    if (files.length > 1) {
      setLocalError("Please upload a single compressed .zip repository.");
      return;
    }

    const file = files[0];
    
    // Strict validation matching the backend's expectations
    if (!file.name.endsWith('.zip') && file.type !== 'application/zip') {
      setLocalError("Invalid format. The AI OS strictly requires a .zip archive.");
      return;
    }

    // Pass the validated file up to Dashboard.jsx to trigger the REST API
    onUpload(file);
  };

  return (
    <div className="flex flex-col items-center justify-center h-full min-h-[400px] w-full bg-gray-800 p-6 rounded-lg border-2 border-dashed border-gray-600 transition-all duration-300">
      
      <div 
        className={`flex flex-col items-center justify-center w-full h-full rounded border-2 border-transparent p-12 transition-all duration-300 cursor-pointer
          ${isDragging ? 'bg-gray-700 border-blue-500 shadow-[0_0_20px_rgba(59,130,246,0.3)]' : 'hover:bg-gray-750'}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current.click()}
      >
        {/* Upload Icon */}
        <div className={`mb-4 transition-transform duration-300 ${isDragging ? 'scale-110' : ''}`}>
          <svg className="w-16 h-16 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        
        <h3 className="text-xl font-bold text-gray-200 mb-2">Initialize Sandbox Environment</h3>
        <p className="text-sm text-gray-400 text-center mb-6">
          Drag and drop your repository <span className="font-mono text-blue-300">.zip</span> here, or click to browse.
        </p>

        {localError && (
          <div className="bg-red-900/50 border border-red-500 text-red-300 px-4 py-2 rounded text-sm mb-4 font-mono">
            Error: {localError}
          </div>
        )}

        <button 
          className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded font-medium transition-colors shadow-lg shadow-blue-500/20"
          onClick={(e) => {
            e.stopPropagation(); // Prevent double-triggering the parent div click
            fileInputRef.current.click();
          }}
        >
          Select Repository
        </button>

        <input 
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept=".zip,application/zip"
          className="hidden" 
        />
      </div>
      
      <div className="mt-4 text-xs text-gray-500 flex items-center gap-2 font-mono">
        <svg className="w-4 h-4 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        Files are extracted securely in RAM. Max size: 15MB.
      </div>
    </div>
  );
}