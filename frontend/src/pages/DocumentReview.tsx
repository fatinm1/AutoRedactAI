import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  FileText, 
  Shield, 
  Eye, 
  Download, 
  ArrowLeft,
  CheckCircle,
  AlertCircle,
  Clock,
  Zap
} from 'lucide-react';
import { documentService, Document, Redaction } from '@/services/documents';
import toast from 'react-hot-toast';

const DocumentReview: React.FC = () => {
  const { documentId } = useParams<{ documentId: string }>();
  const navigate = useNavigate();
  const [document, setDocument] = useState<Document | null>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [redactions, setRedactions] = useState<Redaction[]>([]);

  useEffect(() => {
    if (documentId) {
      loadDocument();
    }
  }, [documentId]);

  const loadDocument = async () => {
    try {
      setLoading(true);
      const response = await documentService.getDocument(documentId!);
      setDocument(response.document);
      
      // Load redactions if document is completed
      if (response.document.status === 'completed') {
        await loadRedactions();
      }
    } catch (error) {
      console.error('Failed to load document:', error);
      toast.error('Failed to load document');
    } finally {
      setLoading(false);
    }
  };

  const loadRedactions = async () => {
    try {
      const response = await documentService.getDocumentRedactions(documentId!);
      setRedactions(response.redactions);
    } catch (error) {
      console.error('Failed to load redactions:', error);
      toast.error('Failed to load redactions');
    }
  };

  const processDocument = async () => {
    try {
      setProcessing(true);
      
      // First update status to processing
      setDocument(prev => prev ? { ...prev, status: 'processing' } : null);
      
      // Add a small delay to show processing state
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Call the backend processing endpoint
      const response = await documentService.processDocument(documentId!);
      
      // Update the document with the processed data
      setDocument(response.document);
      
      // Load the real redactions
      await loadRedactions();
      
      toast.success('Document processed successfully!');
    } catch (error) {
      console.error('Processing failed:', error);
      toast.error('Processing failed');
      // Reset status on error
      setDocument(prev => prev ? { ...prev, status: 'uploaded' } : null);
    } finally {
      setProcessing(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-success-600" />;
      case 'processing':
        return <Clock className="w-5 h-5 text-warning-600" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-error-600" />;
      default:
        return <FileText className="w-5 h-5 text-primary-600" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-success-600 bg-success-50 dark:bg-success-900/20';
      case 'processing':
        return 'text-warning-600 bg-warning-50 dark:bg-warning-900/20';
      case 'error':
        return 'text-error-600 bg-error-50 dark:bg-error-900/20';
      default:
        return 'text-primary-600 bg-primary-50 dark:bg-primary-900/20';
    }
  };

  const getEntityTypeColor = (entityType: string) => {
    switch (entityType) {
      case 'PERSON':
        return 'bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400';
      case 'EMAIL':
        return 'bg-green-100 dark:bg-green-900/20 text-green-600 dark:text-green-400';
      case 'PHONE':
        return 'bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400';
      case 'SSN':
        return 'bg-red-100 dark:bg-red-900/20 text-red-600 dark:text-red-400';
      case 'CREDIT_CARD':
        return 'bg-orange-100 dark:bg-orange-900/20 text-orange-600 dark:text-orange-400';
      case 'IP_ADDRESS':
        return 'bg-indigo-100 dark:bg-indigo-900/20 text-indigo-600 dark:text-indigo-400';
      case 'URL':
        return 'bg-teal-100 dark:bg-teal-900/20 text-teal-600 dark:text-teal-400';
      case 'DATE':
        return 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400';
      case 'ZIP_CODE':
        return 'bg-pink-100 dark:bg-pink-900/20 text-pink-600 dark:text-pink-400';
      case 'CURRENCY':
        return 'bg-emerald-100 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400';
      default:
        return 'bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400';
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/history')}
            className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-800 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div className="animate-pulse">
            <div className="h-6 bg-neutral-200 dark:bg-neutral-700 rounded w-48"></div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="spinner w-8 h-8 mx-auto mb-4"></div>
              <p className="text-neutral-600 dark:text-neutral-400">Loading document...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!document) {
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/history')}
            className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-800 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <h1 className="text-2xl font-bold">Document Not Found</h1>
        </div>
        
        <div className="card">
          <div className="text-center py-12">
            <FileText className="w-16 h-16 text-neutral-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Document not found</h3>
            <p className="text-neutral-600 dark:text-neutral-400 mb-6">
              The document you're looking for doesn't exist or you don't have permission to view it.
            </p>
            <button
              onClick={() => navigate('/history')}
              className="btn-primary"
            >
              Back to Documents
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/history')}
            className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-800 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-2xl font-bold gradient-text">Document Review</h1>
            <p className="text-neutral-600 dark:text-neutral-400">
              Review and process your uploaded document
            </p>
          </div>
        </div>
        
        <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${getStatusColor(document.status)}`}>
          {getStatusIcon(document.status)}
          <span className="text-sm font-medium capitalize">{document.status}</span>
        </div>
      </div>

      {/* Document Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-primary-100 dark:bg-primary-900/20 rounded-xl flex items-center justify-center">
              <FileText className="w-6 h-6 text-primary-600 dark:text-primary-400" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">
                {document.filename}
              </h3>
              <p className="text-sm text-neutral-500 dark:text-neutral-400">
                Uploaded on {new Date(document.created_at).toLocaleDateString()}
                {document.file_size && ` • ${(document.file_size / 1024 / 1024).toFixed(2)} MB`}
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => window.open(`/preview/${document.id}`, '_blank')}
              className="btn-outline"
            >
              <Eye className="w-4 h-4 mr-2" />
              Preview
            </button>
            
            {document.status === 'completed' && (
              <button
                onClick={() => toast.success('Download started')}
                className="btn-primary"
              >
                <Download className="w-4 h-4 mr-2" />
                Download
              </button>
            )}
          </div>
        </div>
      </motion.div>

      {/* Processing Section */}
      {document.status === 'uploaded' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <div className="text-center py-8">
            <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Zap className="w-8 h-8 text-primary-600 dark:text-primary-400" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Ready to Process</h3>
            <p className="text-neutral-600 dark:text-neutral-400 mb-6">
              Click the button below to start AI-powered redaction processing
            </p>
            <button
              onClick={processDocument}
              disabled={processing}
              className="btn-primary"
            >
              {processing ? (
                <div className="flex items-center space-x-2">
                  <div className="spinner w-4 h-4"></div>
                  <span>Processing...</span>
                </div>
              ) : (
                <>
                  <Shield className="w-4 h-4 mr-2" />
                  Start Redaction
                </>
              )}
            </button>
          </div>
        </motion.div>
      )}

      {/* Processing Status */}
      {document.status === 'processing' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <div className="text-center py-8">
            <div className="w-16 h-16 bg-warning-100 dark:bg-warning-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <Clock className="w-8 h-8 text-warning-600 dark:text-warning-400" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Processing Document</h3>
            <p className="text-neutral-600 dark:text-neutral-400 mb-4">
              AI is analyzing your document and identifying sensitive information...
            </p>
            <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
              <div className="bg-primary-600 h-2 rounded-full animate-pulse" style={{ width: '60%' }}></div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Redactions List */}
      {document.status === 'completed' && redactions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Redactions Applied</h3>
            <span className="text-sm text-neutral-500 dark:text-neutral-400">
              {redactions.length} items found
            </span>
          </div>
          
          <div className="space-y-3">
            {redactions.map((redaction) => (
              <div
                key={redaction.id}
                className="flex items-center justify-between p-3 bg-neutral-50 dark:bg-neutral-800/50 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${getEntityTypeColor(redaction.entity_type)}`}>
                    <Shield className="w-4 h-4" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-neutral-900 dark:text-white">
                      {redaction.entity_type}
                    </p>
                    <p className="text-xs text-neutral-500 dark:text-neutral-400">
                      {redaction.entity_text} • Page {redaction.page_number}
                      {redaction.line_number && ` • Line ${redaction.line_number}`}
                    </p>
                  </div>
                </div>
                
                <div className="text-right">
                  <p className="text-sm font-medium text-neutral-900 dark:text-white">
                    {(redaction.confidence_score * 100).toFixed(0)}%
                  </p>
                  <p className="text-xs text-neutral-500 dark:text-neutral-400">
                    Confidence
                  </p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default DocumentReview; 