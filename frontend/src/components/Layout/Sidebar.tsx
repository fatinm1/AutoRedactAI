import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  LayoutDashboard, 
  Upload, 
  FileText, 
  History, 
  BarChart3, 
  Settings,
  Shield,
  Zap
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

const navigationItems = [
  {
    name: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
    description: 'Overview and quick actions'
  },
  {
    name: 'Upload',
    href: '/upload',
    icon: Upload,
    description: 'Upload and process documents'
  },
  {
    name: 'Review',
    href: '/review',
    icon: FileText,
    description: 'Review and edit redactions'
  },
  {
    name: 'History',
    href: '/history',
    icon: History,
    description: 'View processed documents'
  },
  {
    name: 'Analytics',
    href: '/analytics',
    icon: BarChart3,
    description: 'Compliance and usage reports'
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Settings,
    description: 'Account and system settings'
  }
];

const Sidebar: React.FC = () => {
  const location = useLocation();
  const { user } = useAuth();

  return (
    <div className="h-full flex flex-col">
      {/* Logo */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="p-6 border-b border-white/20 dark:border-neutral-700/50"
      >
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl flex items-center justify-center shadow-glow">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
              AutoRedactAI
            </h1>
            <p className="text-xs text-neutral-500 dark:text-neutral-400">
              Privacy Assistant
            </p>
          </div>
        </div>
      </motion.div>

      {/* User info */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="p-4 border-b border-white/20 dark:border-neutral-700/50"
      >
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full flex items-center justify-center">
            <span className="text-white font-semibold text-sm">
              {user?.full_name?.charAt(0) || user?.username?.charAt(0) || 'U'}
            </span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-neutral-900 dark:text-white truncate">
              {user?.full_name || user?.username}
            </p>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 capitalize">
              {user?.role}
            </p>
          </div>
        </div>
      </motion.div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navigationItems.map((item, index) => {
          const isActive = location.pathname === item.href || 
                          (item.href !== '/dashboard' && location.pathname.startsWith(item.href));
          
          return (
            <motion.div
              key={item.name}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: 0.1 + index * 0.05 }}
            >
              <NavLink
                to={item.href}
                className={({ isActive }) =>
                  `group relative flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200 ${
                    isActive
                      ? 'bg-gradient-to-r from-primary-500/20 to-secondary-500/20 text-primary-700 dark:text-primary-300 border border-primary-200/50 dark:border-primary-700/50 shadow-glow'
                      : 'text-neutral-700 dark:text-neutral-300 hover:bg-white/50 dark:hover:bg-neutral-800/50 hover:text-primary-600 dark:hover:text-primary-400'
                  }`
                }
              >
                <item.icon className="w-5 h-5 mr-3" />
                <span>{item.name}</span>
                
                {/* Active indicator */}
                {location.pathname === item.href && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute right-2 w-2 h-2 bg-primary-500 rounded-full"
                    initial={false}
                    transition={{ type: "spring", stiffness: 500, damping: 30 }}
                  />
                )}
              </NavLink>
            </motion.div>
          );
        })}
      </nav>

      {/* Footer */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="p-4 border-t border-white/20 dark:border-neutral-700/50"
      >
        <div className="bg-gradient-to-r from-success-500/10 to-primary-500/10 rounded-xl p-3 border border-success-200/50 dark:border-success-700/50">
          <div className="flex items-center space-x-2">
            <Zap className="w-4 h-4 text-success-500" />
            <span className="text-xs font-medium text-success-700 dark:text-success-300">
              AI Powered
            </span>
          </div>
          <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1">
            Advanced redaction engine
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default Sidebar; 