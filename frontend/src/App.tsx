import React from 'react'
import './styles/globals.css'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md mx-4 text-center">
        <div className="text-6xl mb-6">🤖</div>
        <h1 className="text-3xl font-bold text-gray-800 mb-4">
          AutoRedactAI
        </h1>
        <p className="text-gray-600 mb-6">
          AI-Powered Document Privacy Assistant
        </p>
        
        <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4 mb-6">
          <p className="text-blue-800 font-medium">
            ✅ React App is Working!
          </p>
          <p className="text-blue-600 text-sm mt-1">
            Frontend is rendering successfully
          </p>
        </div>
        
        <div className="space-y-3 text-left">
          <h3 className="font-semibold text-gray-800">🚀 Features:</h3>
          <ul className="text-gray-600 space-y-1">
            <li>• AI-powered document redaction</li>
            <li>• Privacy and compliance tools</li>
            <li>• PDF and DOCX support</li>
            <li>• Advanced ML models</li>
          </ul>
        </div>
        
        <div className="mt-6 pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-500">
            React + TypeScript + Tailwind CSS
          </p>
        </div>
      </div>
    </div>
  )
}

export default App 