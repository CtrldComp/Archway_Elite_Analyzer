# Archway Elite Analyzer - Desktop Application

Professional network analysis solution by **EVMG Technologies**

## Overview

Archway Elite Analyzer is a comprehensive desktop application designed for security professionals, network engineers, and IT administrators who demand the highest level of network analysis capabilities.

## Features

- **Advanced Network Discovery** - Comprehensive scanning and device identification
- **Elite Security Analysis** - Threat detection and security scoring
- **RF Spectrum Analysis** - Professional spectrum visualization
- **Client Device Monitoring** - Detailed client tracking and behavior analysis
- **Professional Reporting** - Executive summaries and compliance documentation
- **Cross-Platform Support** - Available for Windows, Linux, and macOS

## System Requirements

### Windows
- Windows 10 or later (64-bit recommended)
- 4 GB RAM minimum, 8 GB recommended
- 500 MB free disk space
- Network adapter with monitor mode support (for advanced features)

### Linux
- Ubuntu 18.04+ / Debian 10+ / CentOS 7+ / Fedora 30+
- 4 GB RAM minimum, 8 GB recommended
- 500 MB free disk space
- Network adapter with monitor mode support (for advanced features)

### macOS
- macOS 10.14 (Mojave) or later
- 4 GB RAM minimum, 8 GB recommended
- 500 MB free disk space
- Network adapter with monitor mode support (for advanced features)

## Installation

### Windows Installation

#### Option 1: NSIS Installer (Recommended)
1. Download `ArchwayEliteAnalyzer-Setup-1.0.0.exe`
2. Run the installer as Administrator
3. Follow the installation wizard
4. Desktop and Start Menu shortcuts will be created automatically
5. Launch from Desktop shortcut or Start Menu

#### Option 2: Portable Version
1. Download `ArchwayEliteAnalyzer-1.0.0-portable.exe`
2. Run the portable executable directly
3. No installation required - runs from any location

### Linux Installation

#### Option 1: AppImage (Universal)
1. Download `ArchwayEliteAnalyzer-1.0.0.AppImage`
2. Make it executable: `chmod +x ArchwayEliteAnalyzer-1.0.0.AppImage`
3. Run: `./ArchwayEliteAnalyzer-1.0.0.AppImage`
4. Optional: Integrate with desktop using AppImageLauncher

#### Option 2: Debian/Ubuntu (.deb)
1. Download `archway-elite-analyzer_1.0.0_amd64.deb`
2. Install: `sudo dpkg -i archway-elite-analyzer_1.0.0_amd64.deb`
3. Fix dependencies if needed: `sudo apt-get install -f`
4. Launch from Applications menu or run: `archway-elite-analyzer`

#### Option 3: Red Hat/CentOS/Fedora (.rpm)
1. Download `archway-elite-analyzer-1.0.0.x86_64.rpm`
2. Install: `sudo rpm -i archway-elite-analyzer-1.0.0.x86_64.rpm`
3. Or with yum/dnf: `sudo yum install archway-elite-analyzer-1.0.0.x86_64.rpm`
4. Launch from Applications menu or run: `archway-elite-analyzer`

#### Option 4: Tar.gz Archive
1. Download `archway-elite-analyzer-1.0.0.tar.gz`
2. Extract: `tar -xzf archway-elite-analyzer-1.0.0.tar.gz`
3. Run: `./archway-elite-analyzer-1.0.0/archway-elite-analyzer`

### macOS Installation

#### Option 1: DMG Installer (Recommended)
1. Download `ArchwayEliteAnalyzer-1.0.0.dmg`
2. Open the DMG file
3. Drag "Archway Elite Analyzer" to the Applications folder
4. Launch from Applications or Launchpad

#### Option 2: ZIP Archive
1. Download `ArchwayEliteAnalyzer-1.0.0-mac.zip`
2. Extract the ZIP file
3. Move "Archway Elite Analyzer.app" to Applications folder
4. Launch from Applications or Launchpad

## Desktop Integration

### Windows
- Desktop shortcut automatically created during installation
- Start Menu entry in "EVMG Technologies" folder
- File associations for .archway project files
- Windows notification support

### Linux
- Desktop entry automatically installed to `/usr/share/applications/`
- Application menu integration
- Icon installed to system icon theme
- MIME type registration for .archway files
- Native notification support

### macOS
- Dock integration
- Launchpad integration
- Spotlight search support
- macOS notification center integration
- File associations for .archway project files

## Usage

1. **Launch the Application**
   - Windows: Use Desktop shortcut or Start Menu
   - Linux: Use Applications menu or command line
   - macOS: Use Applications folder or Launchpad

2. **Initial Setup**
   - Select your network interface
   - Configure scanning preferences
   - Set up monitoring parameters

3. **Start Analysis**
   - Click "Start Scan" to begin network discovery
   - View real-time results in the dashboard
   - Access detailed analysis in specialized tabs

4. **Generate Reports**
   - Use the reporting features to create professional documentation
   - Export data in multiple formats (PDF, CSV, JSON)
   - Schedule automated reports

## Keyboard Shortcuts

- `Ctrl+S` / `Cmd+S` - Start Scan
- `Ctrl+Shift+S` / `Cmd+Shift+S` - Stop Scan
- `F5` - Refresh Networks
- `Ctrl+E` / `Cmd+E` - Export Data
- `Ctrl+I` / `Cmd+I` - Import Configuration
- `F11` / `Ctrl+Cmd+F` - Toggle Fullscreen
- `Ctrl+R` / `Cmd+R` - Reload
- `Ctrl+Shift+I` / `Alt+Cmd+I` - Developer Tools

## Troubleshooting

### Common Issues

#### Application Won't Start
- **Windows**: Run as Administrator, check Windows Defender exclusions
- **Linux**: Check permissions, install missing dependencies
- **macOS**: Allow in Security & Privacy settings, check Gatekeeper

#### Network Interface Not Detected
- Ensure network adapter supports monitor mode
- Run with elevated privileges (Administrator/sudo)
- Check driver compatibility

#### Performance Issues
- Close unnecessary applications
- Increase system RAM if possible
- Reduce scan frequency in settings

### Getting Help

- **Documentation**: Visit https://evmg.tech/archway/docs
- **Support**: Contact support@evmg.tech
- **Community**: Join our user community forums

## Uninstallation

### Windows
- Use "Add or Remove Programs" in Windows Settings
- Or run the uninstaller from Start Menu

### Linux
- **DEB**: `sudo apt remove archway-elite-analyzer`
- **RPM**: `sudo rpm -e archway-elite-analyzer`
- **AppImage**: Simply delete the AppImage file

### macOS
- Move "Archway Elite Analyzer.app" to Trash
- Empty Trash to complete removal

## License

Archway Elite Analyzer is proprietary software developed by EVMG Technologies.

© 2025 EVMG Technologies. All rights reserved.

## About EVMG Technologies

EVMG Technologies is a leading provider of elite network analysis solutions, specializing in cutting-edge tools for security professionals, network engineers, and IT administrators.

For more information, visit: https://evmg.tech

