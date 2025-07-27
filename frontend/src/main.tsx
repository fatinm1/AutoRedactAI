import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './styles/globals.css'

// Add error handling
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error);
  // Display error on page
  const errorDiv = document.createElement('div');
  errorDiv.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: #ef4444;
    color: white;
    padding: 1rem;
    z-index: 9999;
    font-family: monospace;
  `;
  errorDiv.textContent = `Error: ${event.error?.message || 'Unknown error'}`;
  document.body.appendChild(errorDiv);
});

// Add unhandled promise rejection handling
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
  const errorDiv = document.createElement('div');
  errorDiv.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: #f59e0b;
    color: white;
    padding: 1rem;
    z-index: 9999;
    font-family: monospace;
  `;
  errorDiv.textContent = `Promise Error: ${event.reason}`;
  document.body.appendChild(errorDiv);
});

// Add debugging
console.log('main.tsx: Starting React app...');

try {
  const rootElement = document.getElementById('root');
  console.log('main.tsx: Root element found:', rootElement);
  
  if (rootElement) {
    const root = ReactDOM.createRoot(rootElement);
    console.log('main.tsx: React root created');
    
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
    console.log('main.tsx: React app rendered');
  } else {
    console.error('main.tsx: Root element not found!');
    document.body.innerHTML = '<div style="padding: 2rem; color: red;">Error: Root element not found!</div>';
  }
} catch (error) {
  console.error('main.tsx: Error rendering React app:', error);
  document.body.innerHTML = `<div style="padding: 2rem; color: red;">Error: ${error}</div>`;
} 