import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

console.log('main.tsx: Starting React app...');
console.log('main.tsx: Document ready state:', document.readyState);
console.log('main.tsx: Document body:', document.body);
console.log('main.tsx: All elements with id="root":', document.querySelectorAll('#root'));

// Wait for DOM to be ready
const initializeApp = () => {
  console.log('main.tsx: DOM ready, looking for root element...');
  
  const rootElement = document.getElementById('root');
  console.log('main.tsx: Root element found:', rootElement);
  console.log('main.tsx: Root element HTML:', rootElement?.outerHTML);
  
  if (rootElement) {
    console.log('main.tsx: Creating React root...');
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
    console.error('main.tsx: Document body HTML:', document.body.innerHTML);
    document.body.innerHTML = '<div style="padding: 2rem; color: red; font-family: Arial, sans-serif; text-align: center; background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 2rem;">Error: Root element not found!<br><small>Check console for details.</small></div>';
  }
};

// If DOM is already ready, initialize immediately
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp);
} else {
  // DOM is already ready
  initializeApp();
} 