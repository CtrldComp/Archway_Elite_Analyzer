const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // App information
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  
  // File operations
  showSaveDialog: (options) => ipcRenderer.invoke('show-save-dialog', options),
  showOpenDialog: (options) => ipcRenderer.invoke('show-open-dialog', options),
  
  // Menu event listeners
  onMenuExportData: (callback) => ipcRenderer.on('menu-export-data', callback),
  onMenuImportConfig: (callback) => ipcRenderer.on('menu-import-config', callback),
  onMenuStartScan: (callback) => ipcRenderer.on('menu-start-scan', callback),
  onMenuStopScan: (callback) => ipcRenderer.on('menu-stop-scan', callback),
  onMenuRefreshNetworks: (callback) => ipcRenderer.on('menu-refresh-networks', callback),
  
  // Remove listeners
  removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel),
  
  // Platform information
  platform: process.platform,
  
  // Environment
  isDevelopment: process.env.NODE_ENV === 'development'
});

// Expose a limited API for desktop-specific features
contextBridge.exposeInMainWorld('desktopAPI', {
  // Desktop-specific functionality
  isDesktop: true,
  platform: process.platform,
  
  // Notification support
  showNotification: (title, body) => {
    if (Notification.permission === 'granted') {
      new Notification(title, { body });
    }
  },
  
  // Request notification permission
  requestNotificationPermission: async () => {
    return await Notification.requestPermission();
  }
});

