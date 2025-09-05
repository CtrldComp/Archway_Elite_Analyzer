# Installation Guide

This guide provides detailed installation instructions for Archway Elite Analyzer across all supported platforms.

## System Requirements

### Minimum Requirements
- **RAM**: 4 GB (8 GB recommended)
- **Storage**: 500 MB free disk space
- **Network**: Network adapter with monitor mode support (for advanced features)

### Platform-Specific Requirements

#### Windows
- Windows 10 or later (64-bit recommended)
- .NET Framework 4.7.2 or later (usually pre-installed)
- Administrator privileges for installation

#### Linux
- Ubuntu 18.04+ / Debian 10+ / CentOS 7+ / Fedora 30+
- glibc 2.17 or later
- X11 or Wayland display server

#### macOS
- macOS 10.14 (Mojave) or later
- Intel or Apple Silicon processor

## Desktop Application Installation

### Windows Installation

#### Option 1: NSIS Installer (Recommended)
1. Download `ArchwayEliteAnalyzer-Setup-1.0.0.exe` from the [releases page](https://github.com/CtrldComp/Archway_Elite_Analyzer/releases)
2. Right-click the installer and select "Run as administrator"
3. Follow the installation wizard:
   - Accept the license agreement
   - Choose installation directory (default: `C:\Program Files\Archway Elite Analyzer`)
   - Select additional tasks (desktop shortcut, start menu entry)
4. Click "Install" to begin installation
5. Launch from Desktop shortcut or Start Menu

**Features:**
- ✅ Desktop shortcut automatically created
- ✅ Start Menu entry in "EVMG Technologies" folder
- ✅ File associations for .archway project files
- ✅ Automatic uninstaller
- ✅ Windows notification support

#### Option 2: Portable Version
1. Download `ArchwayEliteAnalyzer-1.0.0-portable.exe`
2. Create a folder for the application (e.g., `C:\Tools\Archway`)
3. Move the portable executable to this folder
4. Run the executable directly - no installation required
5. Optionally create a desktop shortcut manually

**Features:**
- ✅ No installation required
- ✅ Runs from any location
- ✅ Portable settings and data
- ❌ No automatic file associations
- ❌ No system integration

### Linux Installation

#### Option 1: AppImage (Universal - Recommended)
1. Download `ArchwayEliteAnalyzer-1.0.0.AppImage`
2. Make it executable:
   ```bash
   chmod +x ArchwayEliteAnalyzer-1.0.0.AppImage
   ```
3. Run the application:
   ```bash
   ./ArchwayEliteAnalyzer-1.0.0.AppImage
   ```
4. Optional: Install AppImageLauncher for better desktop integration

**Features:**
- ✅ Works on all Linux distributions
- ✅ No installation required
- ✅ Self-contained with all dependencies
- ✅ Desktop integration with AppImageLauncher

#### Option 2: Debian/Ubuntu (.deb)
1. Download `archway-elite-analyzer_1.0.0_amd64.deb`
2. Install using dpkg:
   ```bash
   sudo dpkg -i archway-elite-analyzer_1.0.0_amd64.deb
   ```
3. Fix dependencies if needed:
   ```bash
   sudo apt-get install -f
   ```
4. Launch from Applications menu or command line:
   ```bash
   archway-elite-analyzer
   ```

**Features:**
- ✅ System package manager integration
- ✅ Automatic dependency resolution
- ✅ Desktop entry and icon
- ✅ Easy removal with `apt remove`

#### Option 3: Red Hat/CentOS/Fedora (.rpm)
1. Download `archway-elite-analyzer-1.0.0.x86_64.rpm`
2. Install using rpm:
   ```bash
   sudo rpm -i archway-elite-analyzer-1.0.0.x86_64.rpm
   ```
   Or with yum/dnf:
   ```bash
   sudo yum install archway-elite-analyzer-1.0.0.x86_64.rpm
   # or
   sudo dnf install archway-elite-analyzer-1.0.0.x86_64.rpm
   ```
3. Launch from Applications menu or command line:
   ```bash
   archway-elite-analyzer
   ```

#### Option 4: Tar.gz Archive
1. Download `archway-elite-analyzer-1.0.0.tar.gz`
2. Extract the archive:
   ```bash
   tar -xzf archway-elite-analyzer-1.0.0.tar.gz
   ```
3. Run the application:
   ```bash
   cd archway-elite-analyzer-1.0.0
   ./archway-elite-analyzer
   ```

### macOS Installation

#### Option 1: DMG Installer (Recommended)
1. Download `ArchwayEliteAnalyzer-1.0.0.dmg`
2. Double-click the DMG file to mount it
3. Drag "Archway Elite Analyzer" to the Applications folder
4. Eject the DMG file
5. Launch from Applications folder or Launchpad

**First Launch on macOS:**
- macOS may show a security warning for unsigned applications
- Go to System Preferences > Security & Privacy > General
- Click "Open Anyway" next to the Archway Elite Analyzer warning

#### Option 2: ZIP Archive
1. Download `ArchwayEliteAnalyzer-1.0.0-mac.zip`
2. Double-click to extract the ZIP file
3. Move "Archway Elite Analyzer.app" to Applications folder
4. Launch from Applications folder or Launchpad

## Web Application Setup

For development or custom deployment:

### Prerequisites
- Node.js 20.x or later
- Python 3.11 or later
- Git

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/CtrldComp/Archway_Elite_Analyzer.git
   cd Archway_Elite_Analyzer
   ```

2. **Setup Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Setup Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python src/main.py
   ```

4. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000

## Post-Installation Setup

### Network Interface Configuration

1. **Identify Network Interfaces:**
   - Launch Archway Elite Analyzer
   - Go to Settings > Network Interfaces
   - Select your primary network interface

2. **Enable Monitor Mode (Advanced Features):**
   - Ensure your network adapter supports monitor mode
   - On Linux: May require additional drivers or configuration
   - On Windows: May require specific adapter drivers
   - On macOS: Limited monitor mode support

3. **Permissions Setup:**
   - **Linux**: May require running with sudo for advanced features
   - **Windows**: Run as Administrator for full functionality
   - **macOS**: Grant network access permissions when prompted

### Initial Configuration

1. **First Launch:**
   - Complete the welcome wizard
   - Configure basic settings
   - Test network connectivity

2. **License Activation:**
   - Enter your EVMG Technologies license key
   - Activate professional features
   - Configure update preferences

## Troubleshooting

### Common Issues

#### Application Won't Start
- **Windows**: Check Windows Defender exclusions, run as Administrator
- **Linux**: Verify permissions, install missing dependencies
- **macOS**: Allow in Security & Privacy settings

#### Network Interface Not Detected
- Ensure network adapter supports monitor mode
- Update network adapter drivers
- Run with elevated privileges

#### Performance Issues
- Close unnecessary applications
- Increase available RAM
- Reduce scan frequency in settings

### Getting Help

- **Documentation**: [https://docs.evmg.tech/archway](https://docs.evmg.tech/archway)
- **Support**: [support@evmg.tech](mailto:support@evmg.tech)
- **GitHub Issues**: [Report bugs and request features](https://github.com/CtrldComp/Archway_Elite_Analyzer/issues)

## Uninstallation

### Windows
- Use "Add or Remove Programs" in Windows Settings
- Or run the uninstaller from Start Menu > EVMG Technologies

### Linux
- **DEB**: `sudo apt remove archway-elite-analyzer`
- **RPM**: `sudo rpm -e archway-elite-analyzer`
- **AppImage**: Simply delete the AppImage file

### macOS
- Move "Archway Elite Analyzer.app" to Trash
- Empty Trash to complete removal

---

**EVMG Technologies** - *A Controlled Compromise LTD subsidiary*  
© 2025 EVMG Technologies. All rights reserved.

