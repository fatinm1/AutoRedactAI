import React from 'react';
import { motion } from 'framer-motion';
import { 
  FileText, 
  Shield, 
  BarChart3, 
  Clock,
  TrendingUp,
  Users
} from 'lucide-react';

const Dashboard: React.FC = () => {
  const stats = [
    {
      title: 'Documents Processed',
      value: '1,234',
      change: '+12%',
      icon: FileText,
      color: 'primary'
    },
    {
      title: 'Redactions Applied',
      value: '5,678',
      change: '+8%',
      icon: Shield,
      color: 'success'
    },
    {
      title: 'Processing Time',
      value: '2.3s',
      change: '-15%',
      icon: Clock,
      color: 'warning'
    },
    {
      title: 'Accuracy Rate',
      value: '98.5%',
      change: '+2%',
      icon: TrendingUp,
      color: 'secondary'
    }
  ];

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
          Welcome back! Here's an overview of your document processing activity.
        </p>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {stats.map((stat, index) => (
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
                <p className="text-xs text-success-600 dark:text-success-400 mt-1">
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
            <button className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300">
              View all
            </button>
          </div>
          <div className="space-y-3">
            {[1, 2, 3].map((item) => (
              <div key={item} className="flex items-center space-x-3 p-3 rounded-lg hover:bg-neutral-50 dark:hover:bg-neutral-800/50 transition-colors">
                <div className="w-10 h-10 bg-primary-100 dark:bg-primary-900/20 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-primary-600 dark:text-primary-400" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-neutral-900 dark:text-white">
                    Document {item}.pdf
                  </p>
                  <p className="text-xs text-neutral-500 dark:text-neutral-400">
                    2 hours ago • 15 redactions applied
                  </p>
                </div>
                <div className="badge-success">Completed</div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h2 className="text-xl font-semibold text-neutral-900 dark:text-white mb-4">
            Quick Actions
          </h2>
          <div className="space-y-3">
            <button className="w-full btn-primary">
              <FileText className="w-4 h-4 mr-2" />
              Upload New Document
            </button>
            <button className="w-full btn-outline">
              <BarChart3 className="w-4 h-4 mr-2" />
              View Analytics
            </button>
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