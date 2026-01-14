# ScubaGoggles Web Interface

🤿 **Professional ScubaGoggles Configuration Interface** - Now available as a web application!

## 🌐 Live Web Interface

Access the ScubaGoggles configuration interface directly in your browser:

**👉 [https://dicktracyii.github.io/ScubaGoggles/](https://dicktracyii.github.io/ScubaGoggles/)**

## ✨ Features

### 🎯 Professional Configuration Interface
- **Interactive Setup Wizard** - Step-by-step guidance through ScubaGoggles configuration
- **Google Workspace Product Selection** - Choose from 8 different GWS products to assess
- **Credentials Management** - Secure handling of service account configurations
- **Output Customization** - Configure report generation and output directories
- **Configuration Export** - Download ready-to-use configuration files

### 🔧 Web-Based Streamlit Application
- **Powered by stlite** - Streamlit running entirely in your browser
- **No Installation Required** - Works without local Python or dependencies
- **Real-time Configuration** - Instant feedback and validation
- **Professional UI** - Clean, modern interface matching ScubaGear branding

### 📊 Assessment Planning
- **Product Overview** - Detailed information about each GWS security assessment
- **Readiness Validation** - Pre-flight checks before running assessments
- **Command Generation** - Automatic creation of local execution commands
- **Configuration Templates** - Preset configurations for different assessment types

## 🚀 How It Works

### 1. **Web Configuration** (Browser-based)
Use the GitHub Pages interface to:
- Configure your assessment parameters
- Upload or specify Google Workspace credentials
- Select products to assess (Gmail, Drive, Calendar, Meet, etc.)
- Set output preferences and organization details
- Download your complete configuration

### 2. **Local Execution** (Command-line)
After configuring via the web interface:
```bash
# Install ScubaGoggles locally
pip install scubagoggles

# Run assessment with your downloaded configuration
python -m scubagoggles --config your_downloaded_config.yaml
```

## 🛠️ Technical Architecture

### Frontend (GitHub Pages)
- **HTML5** with modern responsive design
- **stlite** - Streamlit compiled to WebAssembly
- **CDN Delivery** - Fast loading via jsdelivr CDN
- **Progressive Enhancement** - Graceful fallbacks for compatibility

### Backend Integration
- **Configuration Generation** - Creates valid ScubaGoggles config files
- **Local Tool Integration** - Seamless handoff to local ScubaGoggles installation
- **YAML Export** - Standard configuration format support

### CI/CD Pipeline
- **GitHub Actions** - Automatic deployment on code changes
- **Build Optimization** - Minified assets and performance optimization
- **Deployment Verification** - Post-deployment health checks

## 📋 Configuration Sections

### 🔐 Authentication
- Service account credential upload
- Domain-wide delegation setup guidance
- OAuth scope configuration help

### 📊 Products Assessment
Choose from 8 Google Workspace products:
- **Gmail** - Email security settings, DLP policies
- **Google Drive** - File sharing policies, external access controls
- **Google Calendar** - Calendar sharing, privacy settings  
- **Google Meet** - Meeting security, participant controls
- **Google Groups** - Group management, external member policies
- **Google Chat** - Chat security, external chat policies
- **Google Sites** - Site sharing policies, publishing settings
- **Google Classroom** - Classroom security, privacy controls

### 📁 Output Configuration
- Custom output directory paths
- Report format selection (HTML, JSON, CSV, PDF)
- File organization preferences
- Compression and archiving options

### 🎯 Assessment Details
- Organization information
- Custom report titles
- Assessment metadata
- Advanced scanning options

## 🔄 Development Workflow

### Making Changes
1. **Edit the Interface** - Modify `index.html` or UI components
2. **Automatic Deployment** - GitHub Actions builds and deploys changes
3. **Live Updates** - Changes appear at the GitHub Pages URL

### Local Development
```bash
# For local Streamlit development
cd scubagoggles/ui
pip install -r requirements-ui.txt
streamlit run scubaconfigapp.py
```

### GitHub Pages Deployment
- **Trigger**: Push to main/master branch or manual dispatch
- **Build**: Validates Streamlit components and optimizes assets
- **Deploy**: Updates GitHub Pages with new version
- **Verify**: Automated post-deployment checks

## 🔗 Links & Resources

- **🌐 Live Interface**: [https://dicktracyii.github.io/ScubaGoggles/](https://dicktracyii.github.io/ScubaGoggles/)
- **📖 ScubaGoggles Documentation**: [Main Repository](https://github.com/cisagov/ScubaGoggles)
- **🐛 Report Issues**: [GitHub Issues](https://github.com/dicktracyii/ScubaGoggles/issues)
- **💡 Feature Requests**: [Discussions](https://github.com/dicktracyii/ScubaGoggles/discussions)

## 🛡️ Security Considerations

### Data Handling
- **Client-side Processing** - All configuration happens in your browser
- **No Data Storage** - Credentials and configurations are not stored on servers
- **Local Download** - Configuration files are generated and downloaded locally
- **HTTPS Delivery** - Secure delivery via GitHub Pages HTTPS

### Credential Safety
- **Upload Validation** - JSON credential files are validated locally
- **No Server Upload** - Credentials never leave your browser
- **Secure Handoff** - Downloaded configs work directly with local ScubaGoggles

## 📈 Future Enhancements

### Planned Features
- **Real-time Assessment** - Browser-based security scanning (limitations apply)
- **Enhanced Reporting** - Advanced visualization and charts
- **Template Library** - Pre-built configuration templates for different scenarios
- **Integration APIs** - Direct integration with other security tools

### Community Contributions
- **UI Improvements** - Enhanced styling and user experience
- **Feature Additions** - New configuration options and capabilities  
- **Documentation** - Improved guides and tutorials
- **Testing** - Browser compatibility and performance testing

---

🤿 **ScubaGoggles** - Professional Google Workspace Security Assessment Tool  
🌐 **Web Interface** - Powered by Streamlit + stlite + GitHub Pages