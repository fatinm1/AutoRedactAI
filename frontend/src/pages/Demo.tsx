import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  FileText, 
  Shield, 
  CheckCircle, 
  AlertCircle,
  Download,
  Upload,
  Eye,
  EyeOff,
  Clock,
  BarChart3,
  Users,
  CreditCard,
  Mail,
  Phone,
  User
} from 'lucide-react';
import { Link } from 'react-router-dom';

const Demo: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [showOriginal, setShowOriginal] = useState(false);
  const [processingProgress, setProcessingProgress] = useState(0);

  // Sample document content
  const originalDocument = `CONFIDENTIAL - EMPLOYEE RECORDS

Employee Information:
Name: John Smith
Email: john.smith@company.com
Phone: (555) 123-4567
SSN: 123-45-6789

Financial Information:
Credit Card: 4111-1111-1111-1111
Bank Account: 1234567890
Salary: $75,000

Emergency Contact:
Name: Jane Smith
Phone: (555) 987-6543
Email: jane.smith@email.com

Medical Information:
Insurance ID: INS-123456
Policy Number: POL-789012

This document contains sensitive personal information that must be protected according to company policy and federal regulations.`;

  const redactedDocument = `CONFIDENTIAL - EMPLOYEE RECORDS

Employee Information:
Name: █████████
Email: █████████████████████████████
Phone: █████████████████████████████
SSN: █████████████████████████████

Financial Information:
Credit Card: █████████████████████████████
Bank Account: █████████████████████████████
Salary: $75,000

Emergency Contact:
Name: █████████
Phone: █████████████████████████████
Email: █████████████████████████████

Medical Information:
Insurance ID: █████████████████████████████
Policy Number: █████████████████████████████

This document contains sensitive personal information that must be protected according to company policy and federal regulations.`;

  const detectedEntities = [
    { type: 'PERSON', text: 'John Smith', confidence: 0.98, method: 'AI Detection' },
    { type: 'EMAIL', text: 'john.smith@company.com', confidence: 0.99, method: 'Pattern Matching' },
    { type: 'PHONE', text: '(555) 123-4567', confidence: 0.97, method: 'Pattern Matching' },
    { type: 'SSN', text: '123-45-6789', confidence: 0.99, method: 'Pattern Matching' },
    { type: 'CREDIT_CARD', text: '4111-1111-1111-1111', confidence: 0.99, method: 'Luhn Validation' },
    { type: 'BANK_ACCOUNT', text: '1234567890', confidence: 0.95, method: 'AI Detection' },
    { type: 'PERSON', text: 'Jane Smith', confidence: 0.98, method: 'AI Detection' },
    { type: 'PHONE', text: '(555) 987-6543', confidence: 0.97, method: 'Pattern Matching' },
    { type: 'EMAIL', text: 'jane.smith@email.com', confidence: 0.99, method: 'Pattern Matching' },
    { type: 'INSURANCE_ID', text: 'INS-123456', confidence: 0.92, method: 'AI Detection' },
    { type: 'POLICY_NUMBER', text: 'POL-789012', confidence: 0.91, method: 'AI Detection' }
  ];

  const processingStats = {
    totalEntities: 11,
    processingTime: '2.3 seconds',
    accuracy: '96.4%',
    confidence: '94.2%',
    methodsUsed: ['Pattern Matching', 'AI Detection', 'Luhn Validation']
  };

  const demoSteps = [
    {
      title: 'Document Upload',
      description: 'User uploads a document containing sensitive information',
      icon: Upload,
      status: 'completed'
    },
    {
      title: 'AI Processing',
      description: 'Multi-model AI analyzes the document for sensitive entities',
      icon: Shield,
      status: 'completed'
    },
    {
      title: 'Entity Detection',
      description: '11 sensitive entities detected with 96.4% accuracy',
      icon: CheckCircle,
      status: 'completed'
    },
    {
      title: 'Redaction Applied',
      description: 'Sensitive information replaced with secure placeholders',
      icon: EyeOff,
      status: 'completed'
    }
  ];

  const entityTypeStats = [
    { type: 'PERSON', count: 2, color: 'primary' },
    { type: 'EMAIL', count: 2, color: 'secondary' },
    { type: 'PHONE', count: 2, color: 'warning' },
    { type: 'SSN', count: 1, color: 'error' },
    { type: 'CREDIT_CARD', count: 1, color: 'success' },
    { type: 'OTHER', count: 3, color: 'neutral' }
  ];

  const simulateProcessing = () => {
    setProcessingProgress(0);
    const interval = setInterval(() => {
      setProcessingProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10;
      });
    }, 200);
  };

  React.useEffect(() => {
    if (currentStep === 1) {
      simulateProcessing();
    }
  }, [currentStep]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-50 via-blue-50 to-purple-50 dark:from-neutral-900 dark:via-neutral-800 dark:to-neutral-900">
      {/* Navigation */}
      <nav className="glass-sm border-b border-white/20 dark:border-neutral-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                AutoRedactAI Demo
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/" className="btn-ghost">
                Back to Landing
              </Link>
              <Link to="/register" className="btn-primary">
                Try It Yourself
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-neutral-900 dark:text-white mb-4">
            See AutoRedactAI in Action
          </h1>
          <p className="text-xl text-neutral-600 dark:text-neutral-400 max-w-3xl mx-auto">
            Watch how our intelligent AI automatically detects and redacts sensitive information from documents in real-time.
          </p>
        </motion.div>

        {/* Demo Steps */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12"
        >
          {demoSteps.map((step, index) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 + index * 0.1 }}
              className="card text-center"
            >
              <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center mx-auto mb-4">
                <step.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-2">
                {step.title}
              </h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                {step.description}
              </p>
            </motion.div>
          ))}
        </motion.div>

        {/* Processing Demo */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12"
        >
          {/* Document Comparison */}
          <div className="card">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-neutral-900 dark:text-white">
                Document Redaction
              </h2>
              <button
                onClick={() => setShowOriginal(!showOriginal)}
                className="btn-outline"
              >
                {showOriginal ? <EyeOff className="w-4 h-4 mr-2" /> : <Eye className="w-4 h-4 mr-2" />}
                {showOriginal ? 'Show Redacted' : 'Show Original'}
              </button>
            </div>
            
            <div className="bg-neutral-100 dark:bg-neutral-800 rounded-lg p-4 max-h-96 overflow-y-auto">
              <pre className="text-sm font-mono text-neutral-800 dark:text-neutral-200 whitespace-pre-wrap">
                {showOriginal ? originalDocument : redactedDocument}
              </pre>
            </div>
            
            <div className="mt-4 flex items-center justify-between text-sm text-neutral-600 dark:text-neutral-400">
              <span>Document Type: Employee Records</span>
              <span>File Size: 2.3 KB</span>
            </div>
          </div>

          {/* Processing Stats */}
          <div className="card">
            <h2 className="text-2xl font-bold text-neutral-900 dark:text-white mb-6">
              Processing Results
            </h2>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-neutral-600 dark:text-neutral-400">Processing Time</span>
                <span className="font-semibold text-neutral-900 dark:text-white">{processingStats.processingTime}</span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-neutral-600 dark:text-neutral-400">Entities Detected</span>
                <span className="font-semibold text-neutral-900 dark:text-white">{processingStats.totalEntities}</span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-neutral-600 dark:text-neutral-400">Accuracy</span>
                <span className="font-semibold text-success-600 dark:text-success-400">{processingStats.accuracy}</span>
              </div>
              
              <div className="flex items-center justify-between">
                <span className="text-neutral-600 dark:text-neutral-400">Confidence</span>
                <span className="font-semibold text-primary-600 dark:text-primary-400">{processingStats.confidence}</span>
              </div>
            </div>

            <div className="mt-6">
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-3">
                Detection Methods Used
              </h3>
              <div className="flex flex-wrap gap-2">
                {processingStats.methodsUsed.map((method, index) => (
                  <span key={index} className="badge badge-primary">
                    {method}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Entity Breakdown */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12"
        >
          {/* Entity Types */}
          <div className="card">
            <h2 className="text-2xl font-bold text-neutral-900 dark:text-white mb-6">
              Entity Types Detected
            </h2>
            
            <div className="space-y-3">
              {entityTypeStats.map((stat, index) => (
                <div key={stat.type} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`w-4 h-4 bg-${stat.color}-500 rounded-full`}></div>
                    <span className="text-neutral-700 dark:text-neutral-300">{stat.type}</span>
                  </div>
                  <span className="font-semibold text-neutral-900 dark:text-white">{stat.count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Detected Entities List */}
          <div className="card">
            <h2 className="text-2xl font-bold text-neutral-900 dark:text-white mb-6">
              Detected Entities
            </h2>
            
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {detectedEntities.map((entity, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-primary-100 dark:bg-primary-900/20 rounded-lg flex items-center justify-center">
                      {entity.type === 'PERSON' && <User className="w-4 h-4 text-primary-600" />}
                      {entity.type === 'EMAIL' && <Mail className="w-4 h-4 text-primary-600" />}
                      {entity.type === 'PHONE' && <Phone className="w-4 h-4 text-primary-600" />}
                      {entity.type === 'CREDIT_CARD' && <CreditCard className="w-4 h-4 text-primary-600" />}
                      {!['PERSON', 'EMAIL', 'PHONE', 'CREDIT_CARD'].includes(entity.type) && <Shield className="w-4 h-4 text-primary-600" />}
                    </div>
                    <div>
                      <p className="text-sm font-medium text-neutral-900 dark:text-white">{entity.type}</p>
                      <p className="text-xs text-neutral-500 dark:text-neutral-400">{entity.text}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-neutral-900 dark:text-white">
                      {(entity.confidence * 100).toFixed(0)}%
                    </p>
                    <p className="text-xs text-neutral-500 dark:text-neutral-400">{entity.method}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="text-center"
        >
          <div className="card max-w-2xl mx-auto">
            <h2 className="text-2xl font-bold text-neutral-900 dark:text-white mb-4">
              Ready to Try AutoRedactAI?
            </h2>
            <p className="text-neutral-600 dark:text-neutral-400 mb-6">
              Upload your own documents and see how our AI automatically detects and redacts sensitive information.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/register" className="btn-primary">
                Start Free Trial
              </Link>
              <Link to="/" className="btn-outline">
                Learn More
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Demo; 