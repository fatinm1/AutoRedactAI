import React from 'react';
import { motion } from 'framer-motion';
import { FileText, Edit, Download } from 'lucide-react';

const DocumentReview: React.FC = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold gradient-text">Document Review</h1>
        <p className="text-neutral-600 dark:text-neutral-400 mt-2">
          Review and edit redactions before export
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="card"
      >
        <div className="text-center">
          <FileText className="w-16 h-16 text-neutral-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-neutral-900 dark:text-white mb-2">
            Document Review Interface
          </h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6">
            Interactive redaction editing and preview
          </p>
          <div className="flex space-x-4 justify-center">
            <button className="btn-outline">
              <Edit className="w-4 h-4 mr-2" />
              Edit Redactions
            </button>
            <button className="btn-primary">
              <Download className="w-4 h-4 mr-2" />
              Export Document
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default DocumentReview; 