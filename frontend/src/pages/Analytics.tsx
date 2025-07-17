import React from 'react';
import { motion } from 'framer-motion';
import { BarChart3, TrendingUp, PieChart } from 'lucide-react';

const Analytics: React.FC = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold gradient-text">Analytics</h1>
        <p className="text-neutral-600 dark:text-neutral-400 mt-2">
          Comprehensive analytics and compliance reporting
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="card"
      >
        <div className="text-center">
          <BarChart3 className="w-16 h-16 text-neutral-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-neutral-900 dark:text-white mb-2">
            Analytics Dashboard
          </h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6">
            Detailed insights into your redaction activities
          </p>
          <div className="flex space-x-4 justify-center">
            <button className="btn-outline">
              <TrendingUp className="w-4 h-4 mr-2" />
              Performance Metrics
            </button>
            <button className="btn-primary">
              <PieChart className="w-4 h-4 mr-2" />
              Generate Report
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Analytics; 