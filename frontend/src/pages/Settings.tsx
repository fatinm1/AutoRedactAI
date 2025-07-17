import React from 'react';
import { motion } from 'framer-motion';
import { Settings as SettingsIcon, User, Shield, Bell } from 'lucide-react';

const Settings: React.FC = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold gradient-text">Settings</h1>
        <p className="text-neutral-600 dark:text-neutral-400 mt-2">
          Manage your account and application preferences
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="card"
      >
        <div className="text-center">
          <SettingsIcon className="w-16 h-16 text-neutral-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-neutral-900 dark:text-white mb-2">
            Application Settings
          </h2>
          <p className="text-neutral-600 dark:text-neutral-400 mb-6">
            Configure your preferences and account settings
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="btn-outline">
              <User className="w-4 h-4 mr-2" />
              Profile
            </button>
            <button className="btn-outline">
              <Shield className="w-4 h-4 mr-2" />
              Security
            </button>
            <button className="btn-outline">
              <Bell className="w-4 h-4 mr-2" />
              Notifications
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Settings; 