import React from 'react'

function App() {
  console.log('App component rendering...');
  
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      <div style={{
        background: 'white',
        padding: '40px',
        borderRadius: '16px',
        boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
        textAlign: 'center',
        maxWidth: '500px',
        margin: '20px'
      }}>
        <div style={{ fontSize: '3rem', marginBottom: '20px' }}>🤖</div>
        <h1 style={{
          color: '#1e293b',
          marginBottom: '20px',
          fontSize: '2.5rem',
          fontWeight: '700'
        }}>
          AutoRedactAI
        </h1>
        <p style={{ color: '#64748b', fontSize: '1.1rem', marginBottom: '30px' }}>
          AI-Powered Document Privacy Assistant
        </p>
        
        <div style={{
          padding: '16px',
          background: '#f0f9ff',
          border: '2px solid #0ea5e9',
          borderRadius: '8px',
          margin: '20px 0',
          color: '#0c4a6e'
        }}>
          <strong>✅ React App is Working!</strong><br/>
          <small>Frontend is rendering successfully</small>
        </div>
        
        <div style={{ marginTop: '20px' }}>
          <h3 style={{ color: '#1e293b', marginBottom: '10px' }}>🚀 Features:</h3>
          <ul style={{ color: '#64748b', textAlign: 'left', lineHeight: '1.6' }}>
            <li>• AI-powered document redaction</li>
            <li>• Privacy and compliance tools</li>
            <li>• PDF and DOCX support</li>
            <li>• Advanced ML models</li>
          </ul>
        </div>
        
        <div style={{ marginTop: '30px', fontSize: '0.9rem', color: '#94a3b8' }}>
          <p><strong>React + TypeScript</strong></p>
        </div>
      </div>
    </div>
  )
}

export default App 