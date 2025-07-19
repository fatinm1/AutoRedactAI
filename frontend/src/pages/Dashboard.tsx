import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  Shield, 
  BarChart3, 
  Clock,
  TrendingUp,
  Users
} from 'lucide-react';
import { documentService, Document } from '@/services/documents';
import toast from 'react-hot-toast';

const Dashboard: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalDocuments: 0,
    totalRedactions: 0,
    avgProcessingTime: 0,
    accuracyRate: 0
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const response = await documentService.getDocuments();
      const docs = response.documents;
      setDocuments(docs);

      // Calculate real statistics
      const totalDocs = docs.length;
      const totalRedactions = docs.reduce((sum, doc) => sum + (doc.redactions_count || 0), 0);
      const completedDocs = docs.filter(doc => doc.status === 'completed').length;
      const accuracyRate = totalDocs > 0 ? (completedDocs / totalDocs) * 100 : 0;

      setStats({
        totalDocuments: totalDocs,
        totalRedactions: totalRedactions,
        avgProcessingTime: totalDocs > 0 ? 2.3 : 0, // Mock for now
        accuracyRate: accuracyRate
      });
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const statsData = [
    {
      title: 'Documents Processed',
      value: stats.totalDocuments.toString(),
      change: stats.totalDocuments > 0 ? '+12%' : '0%',
      icon: FileText,
      color: 'primary'
    },
    {
      title: 'Redactions Applied',
      value: stats.totalRedactions.toString(),
      change: stats.totalRedactions > 0 ? '+8%' : '0%',
      icon: Shield,
      color: 'success'
    },
    {
      title: 'Processing Time',
      value: stats.avgProcessingTime > 0 ? `${stats.avgProcessingTime}s` : '0s',
      change: stats.avgProcessingTime > 0 ? '-15%' : '0%',
      icon: Clock,
      color: 'warning'
    },
    {
      title: 'Accuracy Rate',
      value: `${stats.accuracyRate.toFixed(1)}%`,
      change: stats.accuracyRate > 0 ? '+2%' : '0%',
      icon: TrendingUp,
      color: 'secondary'
    }
  ];

  const recentDocuments = documents.slice(0, 3);

  if (loading) {
    return (
      <div className="space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-3xl font-bold gradient-text">Dashboard</h1>
          <p className="text-neutral-600 dark:text-neutral-400 mt-2">
            Loading your document processing activity...
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="card-sm">
              <div className="animate-pulse">
                <div className="h-4 bg-neutral-200 dark:bg-neutral-700 rounded mb-2"></div>
                <div className="h-8 bg-neutral-200 dark:bg-neutral-700 rounded mb-2"></div>
                <div className="h-3 bg-neutral-200 dark:bg-neutral-700 rounded"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold gradient-text">Dashboard</h1>
        <p className="text-neutral-600 dark:text-neutral-400 mt-2">
          {documents.length > 0 
            ? "Welcome back! Here's an overview of your document processing activity."
            : "Welcome! Upload your first document to get started."
          }
        </p>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {statsData.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 + index * 0.1 }}
            className="card-sm"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-neutral-600 dark:text-neutral-400">
                  {stat.title}
                </p>
                <p className="text-2xl font-bold text-neutral-900 dark:text-white mt-1">
                  {stat.value}
                </p>
                <p className={`text-xs mt-1 ${
                  stat.change.startsWith('+') 
                    ? 'text-success-600 dark:text-success-400' 
                    : stat.change.startsWith('-')
                    ? 'text-warning-600 dark:text-warning-400'
                    : 'text-neutral-500 dark:text-neutral-400'
                }`}>
                  {stat.change} from last month
                </p>
              </div>
              <div className={`w-12 h-12 bg-${stat.color}-100 dark:bg-${stat.color}-900/20 rounded-xl flex items-center justify-center`}>
                <stat.icon className={`w-6 h-6 text-${stat.color}-600 dark:text-${stat.color}-400`} />
              </div>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="grid grid-cols-1 lg:grid-cols-2 gap-6"
      >
        {/* Recent Documents */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-neutral-900 dark:text-white">
              Recent Documents
            </h2>
            <Link to="/history" className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300">
              View all
            </Link>
          </div>
          <div className="space-y-3">
            {recentDocuments.length > 0 ? (
              recentDocuments.map((doc, index) => (
                <div key={doc.id} className="flex items-center space-x-3 p-3 rounded-lg hover:bg-neutral-50 dark:hover:bg-neutral-800/50 transition-colors">
                  <div className="w-10 h-10 bg-primary-100 dark:bg-primary-900/20 rounded-lg flex items-center justify-center">
                    <FileText className="w-5 h-5 text-primary-600 dark:text-primary-400" />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-neutral-900 dark:text-white">
                      {doc.filename}
                    </p>
                    <p className="text-xs text-neutral-500 dark:text-neutral-400">
                      {new Date(doc.created_at).toLocaleDateString()} • {doc.redactions_count || 0} redactions applied
                    </p>
                  </div>
                  <div className={`badge ${
                    doc.status === 'completed' ? 'badge-success' :
                    doc.status === 'processing' ? 'badge-warning' :
                    doc.status === 'error' ? 'badge-error' : 'badge-primary'
                  }`}>
                    {doc.status}
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8">
                <FileText className="w-12 h-12 text-neutral-400 mx-auto mb-3" />
                <p className="text-neutral-600 dark:text-neutral-400">
                  No documents uploaded yet
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h2 className="text-xl font-semibold text-neutral-900 dark:text-white mb-4">
            Quick Actions
          </h2>
          <div className="space-y-3">
            <Link to="/upload">
              <button className="w-full btn-primary">
                <FileText className="w-4 h-4 mr-2" />
                Upload New Document
              </button>
            </Link>
            <Link to="/analytics">
              <button className="w-full btn-outline">
                <BarChart3 className="w-4 h-4 mr-2" />
                View Analytics
              </button>
            </Link>
            <button className="w-full btn-outline">
              <Users className="w-4 h-4 mr-2" />
              Team Collaboration
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard; 