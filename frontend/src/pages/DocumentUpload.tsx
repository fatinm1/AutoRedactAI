import React from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, Shield } from 'lucide-react';

const DocumentUpload: React.FC = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold gradient-text">Upload Documents</h1>
        <p className="text-neutral-600 dark:text-neutral-400 mt-2">
          Upload your documents for AI-powered redaction
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="card"
      >
        <div className="text-center">
          <Upload className="w-16 h-16 text-neutral-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-neutral-900 dark:text-white mb-2">
            Drag & Drop Files Here
          </h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6">
            Support for PDF, DOCX, and TXT files up to 50MB
          </p>
          <button className="btn-primary">
            <FileText className="w-4 h-4 mr-2" />
            Choose Files
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default DocumentUpload; 