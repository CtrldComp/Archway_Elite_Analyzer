# Archway Elite Analyzer

<div align="center">
  <img src="desktop/assets/icons/icon-256x256.png" alt="Archway Elite Analyzer" width="128" height="128">
  
  **Professional Network Analysis Solution**
  
  *Developed by EVMG Technologies*  
  *A Controlled Compromise LTD subsidiary*

  [![License](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
  [![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)](#installation)
  [![Version](https://img.shields.io/badge/Version-1.0.0-green.svg)](https://github.com/CtrldComp/Archway_Elite_Analyzer/releases)
  [![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](#)
</div>

## 🎯 Overview

Archway Elite Analyzer is a comprehensive, cross-platform network analysis solution designed for security professionals, network engineers, and IT administrators who demand the highest level of network visibility and analysis capabilities.

### ✨ Key Features

- **🔍 Advanced Network Discovery** - Comprehensive scanning and device identification
- **🛡️ Elite Security Analysis** - Threat detection, rogue AP identification, and security scoring
- **📡 RF Spectrum Analysis** - Professional spectrum visualization and interference detection
- **👥 Client Device Monitoring** - Detailed client tracking and behavior analysis
- **📊 Professional Reporting** - Executive summaries and compliance documentation
- **🖥️ Cross-Platform Desktop** - Native applications for Windows, Linux, and macOS
- **🌐 Web Interface** - Modern, responsive web application
- **⚡ Real-time Monitoring** - Live network analysis and alerts

## 🏗️ Architecture

Archway Elite Analyzer consists of three main components:

### 🎨 Frontend (`/frontend`)
- **Framework**: React 18 with Vite
- **UI Library**: Tailwind CSS + Shadcn/UI
- **Features**: Responsive design, dark/light themes, real-time updates
- **Technology**: TypeScript, modern ES modules

### ⚙️ Backend (`/backend`)
- **Framework**: Flask with Python 3.11
- **Features**: Advanced network analysis, threat detection, data processing
- **APIs**: RESTful API with comprehensive endpoints
- **Database**: SQLite with extensible schema

### 🖥️ Desktop (`/desktop`)
- **Framework**: Electron with Node.js
- **Features**: Native desktop integration, auto-updates, system notifications
- **Platforms**: Windows (NSIS + Portable), Linux (AppImage, .deb, .rpm), macOS (DMG)
- **Integration**: Desktop shortcuts, file associations, system menus

## 🚀 Quick Start

### Prerequisites
- **Node.js** 20.x or later
- **Python** 3.11 or later
- **Git** for version control

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/CtrldComp/Archway_Elite_Analyzer.git
   cd Archway_Elite_Analyzer
   ```

2. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python src/main.py
   ```

4. **Setup Desktop App**
   ```bash
   cd desktop
   npm install
   npm run dev
   ```

## 📦 Installation

### Desktop Applications

#### Windows
- **Installer**: Download `ArchwayEliteAnalyzer-Setup-1.0.0.exe`
- **Portable**: Download `ArchwayEliteAnalyzer-1.0.0-portable.exe`

#### Linux
- **AppImage**: `ArchwayEliteAnalyzer-1.0.0.AppImage` (Universal)
- **Debian/Ubuntu**: `archway-elite-analyzer_1.0.0_amd64.deb`
- **Red Hat/Fedora**: `archway-elite-analyzer-1.0.0.x86_64.rpm`

#### macOS
- **DMG Installer**: `ArchwayEliteAnalyzer-1.0.0.dmg`
- **ZIP Archive**: `ArchwayEliteAnalyzer-1.0.0-mac.zip`

### Web Application
Access the web interface at `http://localhost:5173` after starting the development servers.

## 🛠️ Development

### Building for Production

#### Frontend
```bash
cd frontend
npm run build
```

#### Backend
```bash
cd backend
# Backend runs directly from source
```

#### Desktop Applications
```bash
cd desktop
npm run build        # Build for current platform
npm run build:win    # Windows packages
npm run build:linux  # Linux packages
npm run build:mac    # macOS packages
```

### Project Structure
```
Archway_Elite_Analyzer/
├── frontend/                 # React web application
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/                  # Flask API server
│   ├── src/
│   ├── requirements.txt
│   └── README.md
├── desktop/                  # Electron desktop app
│   ├── main.js
│   ├── preload.js
│   ├── assets/
│   └── package.json
├── docs/                     # Documentation
├── scripts/                  # Build and deployment scripts
├── .github/                  # GitHub workflows
└── README.md
```

## 🔧 Configuration

### Environment Variables
Create `.env` files in each component directory:

#### Frontend (`.env`)
```env
VITE_API_BASE_URL=http://localhost:5000
VITE_APP_NAME=Archway Elite Analyzer
```

#### Backend (`.env`)
```env
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///archway.db
```

## 📖 Documentation

- **[Installation Guide](docs/installation.md)** - Detailed installation instructions
- **[User Guide](docs/user-guide.md)** - Complete user documentation
- **[API Documentation](docs/api.md)** - Backend API reference
- **[Developer Guide](docs/development.md)** - Development setup and guidelines

## 🤝 Contributing

We welcome contributions from the community! Please read our contributing guidelines before submitting pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Bug Reports & Feature Requests

Please use the [GitHub Issues](https://github.com/CtrldComp/Archway_Elite_Analyzer/issues) page to report bugs or request features.

## 📄 License

This project is proprietary software developed by EVMG Technologies, a Controlled Compromise LTD subsidiary. All rights reserved.

For licensing inquiries, please contact: [licensing@evmg.tech](mailto:licensing@evmg.tech)

## 🏢 About EVMG Technologies

EVMG Technologies is a leading provider of elite network analysis solutions, specializing in cutting-edge tools for security professionals, network engineers, and IT administrators.

**Parent Company**: Controlled Compromise LTD  
**Website**: [https://evmg.tech](https://evmg.tech)  
**Support**: [support@evmg.tech](mailto:support@evmg.tech)

## 🔗 Links

- **Documentation**: [https://docs.evmg.tech/archway](https://docs.evmg.tech/archway)
- **Support Portal**: [https://support.evmg.tech](https://support.evmg.tech)
- **Release Notes**: [CHANGELOG.md](CHANGELOG.md)

---

<div align="center">
  <strong>© 2025 EVMG Technologies, a Controlled Compromise LTD subsidiary. All rights reserved.</strong>
</div>


<!-- Workflow trigger: Updated GitHub Actions to v4 - Testing automated builds -->


<!-- Workflow trigger: Testing pnpm-lock.yaml fix - Should resolve ERR_PNPM_NO_LOCKFILE error -->


<!-- Workflow trigger: Testing --no-frozen-lockfile fix - Should bypass ERR_PNPM_NO_LOCKFILE error -->


<!-- Workflow trigger: Testing Windows build debugging - Enhanced logging to identify electron-builder config issue -->

