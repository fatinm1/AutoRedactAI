import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

console.log('main.tsx: Starting React app...');

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