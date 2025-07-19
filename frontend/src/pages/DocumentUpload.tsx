import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, Shield, X, CheckCircle, AlertCircle, Loader } from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import toast from 'react-hot-toast';
import { documentService, Document } from '@/services/documents';

interface UploadedFile {
  id: string;
  file: File;
  status: 'uploading' | 'success' | 'error';
  progress: number;
  error?: string;
  document?: Document;
}

const DocumentUpload: React.FC = () => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles: UploadedFile[] = acceptedFiles.map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      file,
      status: 'uploading',
      progress: 0
    }));

    setUploadedFiles(prev => [...prev, ...newFiles]);
    handleUpload(newFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    multiple: true
  });

  const handleUpload = async (files: UploadedFile[]) => {
    setIsUploading(true);
    
    for (const fileInfo of files) {
      try {
        // Update progress to show upload starting
        setUploadedFiles(prev => 
          prev.map(f => 
            f.id === fileInfo.id 
              ? { ...f, progress: 10 }
              : f
          )
        );

        // Upload file to backend
        const response = await documentService.uploadDocument(fileInfo.file);
        
        // Update progress to show upload complete
        setUploadedFiles(prev => 
          prev.map(f => 
            f.id === fileInfo.id 
              ? { 
                  ...f, 
                  status: 'success', 
                  progress: 100,
                  document: response.document
                }
              : f
          )
        );

        toast.success(`${fileInfo.file.name} uploaded successfully!`);
      } catch (error: any) {
        console.error('Upload error:', error);
        setUploadedFiles(prev => 
          prev.map(f => 
            f.id === fileInfo.id 
              ? { 
                  ...f, 
                  status: 'error', 
                  error: error.response?.data?.detail || 'Upload failed'
                }
              : f
          )
        );
        toast.error(`Failed to upload ${fileInfo.file.name}: ${error.response?.data?.detail || 'Unknown error'}`);
      }
    }
    
    setIsUploading(false);
  };

  const removeFile = (fileId: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== fileId));
  };

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'pdf':
        return '📄';
      case 'docx':
        return '📝';
      case 'txt':
        return '📄';
      default:
        return '📁';
    }
  };

  const getStatusIcon = (status: UploadedFile['status']) => {
    switch (status) {
      case 'uploading':
        return <Loader className="w-4 h-4 animate-spin text-blue-500" />;
      case 'success':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-500" />;
    }
  };

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
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 cursor-pointer ${
            isDragActive
              ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
              : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400 dark:hover:border-primary-500'
          }`}
        >
          <input {...getInputProps()} />
          
          <motion.div
            initial={{ scale: 0.8 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.2 }}
          >
            <Upload className={`w-16 h-16 mx-auto mb-4 ${
              isDragActive ? 'text-primary-500' : 'text-neutral-400'
            }`} />
          </motion.div>
          
          <h2 className="text-xl font-semibold text-neutral-900 dark:text-white mb-2">
            {isDragActive ? 'Drop files here' : 'Drag & Drop Files Here'}
          </h2>
          
          <p className="text-neutral-600 dark:text-neutral-400 mb-6">
            Support for PDF, DOCX, and TXT files up to 50MB
          </p>
          
          <button 
            type="button"
            className="btn-primary"
            onClick={(e) => e.stopPropagation()}
          >
            <FileText className="w-4 h-4 mr-2" />
            Choose Files
          </button>
        </div>
      </motion.div>

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4">
            Uploaded Files ({uploadedFiles.length})
          </h3>
          
          <div className="space-y-3">
            {uploadedFiles.map((fileInfo) => (
              <motion.div
                key={fileInfo.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex items-center justify-between p-3 bg-neutral-50 dark:bg-neutral-800/50 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getFileIcon(fileInfo.file.name)}</span>
                  <div>
                    <p className="text-sm font-medium text-neutral-900 dark:text-white">
                      {fileInfo.file.name}
                    </p>
                    <p className="text-xs text-neutral-500 dark:text-neutral-400">
                      {(fileInfo.file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                    {fileInfo.document && (
                      <p className="text-xs text-green-600 dark:text-green-400">
                        Document ID: {fileInfo.document.id}
                      </p>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  {getStatusIcon(fileInfo.status)}
                  
                  {fileInfo.status === 'uploading' && (
                    <div className="w-20 bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
                      <div 
                        className="bg-primary-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${fileInfo.progress}%` }}
                      />
                    </div>
                  )}
                  
                  <button
                    onClick={() => removeFile(fileInfo.id)}
                    className="p-1 hover:bg-neutral-200 dark:hover:bg-neutral-700 rounded transition-colors"
                  >
                    <X className="w-4 h-4 text-neutral-500" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Upload Progress */}
      {isUploading && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <div className="flex items-center space-x-3">
            <Loader className="w-5 h-5 animate-spin text-primary-500" />
            <span className="text-neutral-700 dark:text-neutral-300">
              Processing documents...
            </span>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default DocumentUpload; 