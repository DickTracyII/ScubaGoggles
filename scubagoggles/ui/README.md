# ScubaGoggles Configuration UI

This directory contains a Streamlit-based configuration interface for ScubaGoggles, inspired by ScubaGear's ScubaConfigApp but built with Python and web technologies.

## Overview

The ScubaGoggles UI provides a user-friendly web interface for:

- **Configuration Management**: Visual forms for all ScubaGoggles settings
- **Real-time Validation**: Immediate feedback on configuration errors
- **YAML/JSON Generation**: Export configurations for reuse
- **Assessment Execution**: Run ScubaGoggles directly from the interface
- **Results Viewing**: Display assessment results and reports

## Features

### 🔐 Authentication
- Service account credentials file upload/selection
- Access token support (advanced users)
- Real-time credential validation

### 📋 Baseline Selection
- Google Workspace (GWS) baseline selection
- Microsoft 365 baseline selection (when available)
- Bulk select/deselect options
- Baseline descriptions and help text

### 📁 Output Configuration
- Output directory selection and validation
- Report format options (HTML, JSON)
- Dark mode toggle for reports
- Directory creation assistance

### ⚙️ Advanced Options
- Break glass account configuration
- Custom OPA executable paths
- Tenant domain specification
- Advanced parameter support

### 🔍 Validation
- configuration validation
- Real-time field-level feedback
- Configuration preview and summary
- Error highlighting and suggestions

### 📄 Configuration Generation
- YAML and JSON export formats
- Commented configuration files
- Sample configurations for different use cases
- Download and save functionality

### 🚀 Assessment Execution
- Direct ScubaGoggles execution from UI
- Progress monitoring and status updates
- Real-time output capture
- Results display and file management

## Files

- `enhanced_app.py` - Main enhanced UI application with full feature set
- `config_app.py` - Basic configuration application
- `validation.py` - Configuration validation utilities
- `config_generator.py` - YAML/JSON configuration generation
- `runner.py` - ScubaGoggles execution and results management
- `launch.py` - Simple launcher script
- `__init__.py` - Package initialization

## Installation

### Prerequisites

1. **ScubaGoggles** must be installed and available
2. **Python 3.8+** is required
3. **Streamlit** and UI dependencies

### Install UI Dependencies

```bash
# Install UI-specific requirements
pip install -r requirements-ui.txt

# Or install streamlit directly
pip install streamlit
```

## Usage

### Method 1: Direct Launch (Recommended)

```bash
# From the ScubaGoggles directory
python -m scubagoggles.ui.launch
```

### Method 2: Streamlit Command

```bash
# Enhanced UI (full features)
streamlit run scubagoggles/ui/enhanced_app.py

# Basic UI
streamlit run scubagoggles/ui/config_app.py
```

### Method 3: Python Script

```python
# From Python
from scubagoggles.ui.enhanced_app import main
main()
```

## Interface Overview

### Navigation Tabs

1. **🔐 Authentication** - Configure credentials and access tokens
2. **📋 Baselines** - Select which services to assess  
3. **📁 Output** - Set report output location and options
4. **⚙️ Advanced** - Configure advanced options (break glass accounts, etc.)
5. **🔍 Validation** - Review configuration and check for errors
6. **📄 Generate Config** - Export YAML/JSON configuration files
7. **🚀 Run Assessment** - Execute ScubaGoggles assessment

### Sidebar Features

- **System Status**: Python version, ScubaGoggles availability
- **Quick Start Guide**: Step-by-step instructions
- **External Links**: Documentation and support resources
- **Configuration Reset**: Clear all settings

## Configuration Workflow

1. **Start the UI**: Launch using one of the methods above
2. **Configure Authentication**: Upload credentials or enter access token
3. **Select Baselines**: Choose which services to assess (Gmail, Drive, etc.)
4. **Set Output Options**: Specify where reports should be saved
5. **Advanced Settings**: Configure optional advanced parameters
6. **Validate**: Review configuration for errors
7. **Generate or Run**: Export config file or run assessment directly

## Comparison with ScubaGear ScubaConfigApp

| Feature | ScubaGear ScubaConfigApp | ScubaGoggles UI |
|---------|-------------------------|-----------------|
| **Platform** | Windows (WPF/XAML) | Cross-platform (Web) |
| **Technology** | PowerShell + XAML | Python + Streamlit |
| **Authentication** | M365 OAuth | Google Service Accounts |
| **Baselines** | M365 Products | Google Workspace |
| **Validation** | Real-time | Real-time |
| **Configuration Export** | YAML/JSON | YAML/JSON |
| **Direct Execution** | Yes | Yes |
| **Results Viewing** | Integrated | Integrated |
| **Theming** | Light/Dark | Streamlit themes |

## Architecture

```
ScubaGoggles UI Architecture
┌─────────────────────────────────┐
│        Streamlit Frontend       │
├─────────────────────────────────┤
│     UI Components & Forms       │
├─────────────────────────────────┤
│    Validation & Config Gen      │
├─────────────────────────────────┤
│      ScubaGoggles Runner        │
├─────────────────────────────────┤
│     ScubaGoggles Core API       │
└─────────────────────────────────┘
```

## Development

### Adding New Features

1. **UI Components**: Add to respective tab rendering methods
2. **Validation**: Extend `validation.py` with new validators
3. **Configuration**: Update `config_generator.py` for new options
4. **Execution**: Modify `runner.py` for new execution features

### Customization

The UI is designed to be easily customizable:

- **Styling**: Modify CSS in the enhanced app
- **Branding**: Update headers and logos
- **Features**: Add new tabs or modify existing ones
- **Validation**: Extend validation rules as needed

## Troubleshooting

### Common Issues

1. **ScubaGoggles Not Found**
   - Ensure ScubaGoggles is installed: `pip install scubagoggles`
   - Check Python path includes ScubaGoggles

2. **Streamlit Not Available**
   - Install UI requirements: `pip install -r requirements-ui.txt`
   - Or install directly: `pip install streamlit`

3. **Port Already in Use**
   - Streamlit default port (8501) may be in use
   - Specify different port: `streamlit run app.py --server.port 8502`

4. **File Upload Issues**
   - Check file permissions
   - Ensure adequate disk space for temporary files

### Getting Help

- [ScubaGoggles Documentation](https://github.com/cisagov/ScubaGoggles)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Report Issues](https://github.com/cisagov/ScubaGoggles/issues)

## License

This code is part of ScubaGoggles and follows the same license terms.

## Contributing

Contributions are welcome! Please see the main ScubaGoggles repository for contribution guidelines.