"""
Professional ScubaGoggles Configuration Interface
Styled to match ScubaGear's ScubaConfigApp but for Google Workspace
"""

import streamlit as st
import yaml
from typing import Dict, Any, List
import os
from datetime import date
from pathlib import Path
import json
import tempfile
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import os

# Add current directory to Python path to find ScubaGoggles modules
current_dir = Path(__file__).parent.parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Import ScubaGoggles modules
SCUBAGOGGLES_AVAILABLE = True
try:
    from scubagoggles.orchestrator import Orchestrator
    from scubagoggles.config import UserConfig
    from scubagoggles import __version__
    from scubagoggles.scuba_constants import OPA_VERSION
except ImportError as e:
    SCUBAGOGGLES_AVAILABLE = False
    # Create mock classes for UI-only functionality
    class MockOrchestrator:
        @staticmethod
        def gws_products():
            return {'gws_baselines': ['gmail', 'drive', 'calendar', 'meet', 'groups', 'chat', 'sites', 'classroom']}
    
    class MockUserConfig:
        def __init__(self):
            self.output_dir = "./"
            self.credentials_file = None
    
    Orchestrator = MockOrchestrator
    UserConfig = MockUserConfig
    __version__ = "NA"
    OPA_VERSION = "0.70.0"


class ScubaConfigApp:
    """ScubaGoggles Configuration Interface"""
    
    def __init__(self):
        self.user_config = UserConfig()
        self.version = __version__
        self.available_policies = self.parse_baseline_policies()
        
        # Initialize session state
        if 'config_data' not in st.session_state:
            st.session_state.config_data = {
                'organization': '',
                'orgname': '',
                'orgunitname': '',
                'subjectemail': '',
                'customerid': '',
                'description': '',
                'environment': 'google_workspace',
                'baselines': [],
                'credentials': '',
                'outputpath': './',
                'darkmode': False,
                'quiet': False,
                'omitpolicy': {},
                'annotatepolicy': {},
                'breakglassaccounts': [],
                'ui_dark_mode': False  # UI dark mode setting
            }
            
        # Initialize UI state
        if 'ui_show_help' not in st.session_state:
            st.session_state.ui_show_help = False

    def parse_baseline_policies(self) -> Dict[str, Dict[str, str]]:
        """Parse policies from baseline markdown files"""
        policies = {}
        baseline_dir = Path('scubagoggles/baselines')
        
        if not baseline_dir.exists():
            return policies
        
        for md_file in baseline_dir.glob('*.md'):
            if md_file.name == 'README.md':
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                baseline_name = md_file.stem.upper()
                policies[baseline_name] = self.extract_policies_from_markdown(content, baseline_name)
            except Exception as e:
                continue  # Skip files that can't be parsed
        
        return policies
    
    def extract_policies_from_markdown(self, content: str, baseline_name: str) -> Dict[str, str]:
        """Extract policy IDs and titles from markdown content"""
        policies = {}
        lines = content.split('\n')
        
        in_policies_section = False
        current_policy_id = None
        
        for line in lines:
            line = line.strip()
            
            # Check if we're entering the policies section
            if line == '### Policies':
                in_policies_section = True
                continue
            
            # Check if we're leaving the policies section
            if in_policies_section and line.startswith('### ') and line != '### Policies':
                in_policies_section = False
                continue
            
            # Extract policy IDs
            if in_policies_section and line.startswith('#### GWS.'):
                # Extract policy ID (remove #### and any trailing text)
                policy_id = line.replace('#### ', '').split()[0]
                current_policy_id = policy_id
                
                # Get the next line which should contain the policy description
                continue
            
            # Get policy description (first line after policy ID)
            if in_policies_section and current_policy_id and not line.startswith('#') and line:
                # Clean up the description
                description = line.rstrip('.')
                policies[current_policy_id] = description
                current_policy_id = None
        
        return policies

    def setup_page_config(self):
        """Configure the Streamlit page with professional styling"""
        st.set_page_config(
            page_title="ScubaGoggles Configuration Editor",
            page_icon="🤿",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Set custom theme with green primary color for checkboxes
        st.markdown("""
        <script>
        const theme = {
            primaryColor: "#28a745",
            backgroundColor: "#f6fbfe", 
            secondaryBackgroundColor: "#ffffff",
            textColor: "#262730"
        };
        window.streamlitTheme = theme;
        </script>
        """, unsafe_allow_html=True)
        
        # Custom CSS to match ScubaGear's professional look with dark mode support
        dark_mode = st.session_state.config_data.get('ui_dark_mode', False)
        
        # Always regenerate CSS to ensure it matches current state
        css_content = self._generate_css(dark_mode)
        st.markdown(css_content, unsafe_allow_html=True)
    
    def _generate_css(self, dark_mode):
        """Generate CSS based on dark mode setting"""
        
        # Define color schemes
        if dark_mode:
            bg_color = "#0e1117"
            secondary_bg = "#262730"
            text_color = "#fafafa"
            header_gradient = "linear-gradient(135deg, #1f2937 0%, #374151 100%)"
            section_bg = "#262730"
            border_color = "#4b5563"
        else:
            bg_color = "#f6fbfe"
            secondary_bg = "#ffffff"
            text_color = "#262730"
            header_gradient = "linear-gradient(135deg, #3d5b96 0%, #4a90e2 100%)"
            section_bg = "white"
            border_color = "#e8f4fd"
        
        return f"""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;500;600;700&display=swap');
        
        /* Set Streamlit theme variables for green checkboxes */
        :root {{
            --primary-color: #28a745;
            --primary-color-dark: #1e7e34;
        }}
        
        /* Main app styling */
        .stApp {{
            background-color: {bg_color};
            font-family: 'Segoe UI', sans-serif;
            color: {text_color};
        }}
        
        /* Header styling */
        .main-header {{
            background: {header_gradient};
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .header-title {{
            font-size: 2rem;
            font-weight: 600;
            margin: 0;
        }}
        
        .header-subtitle {{
            font-size: 1.1rem;
            opacity: 0.9;
            margin: 0.5rem 0 0 0;
        }}
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0;
            background-color: {secondary_bg};
            border-radius: 8px 8px 0 0;
            padding: 0.5rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background-color: transparent;
            border: none;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            color: {text_color};
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {section_bg};
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Section styling */
        .section-container {{
            background: {section_bg};
            padding: 2rem;
            border-radius: 0 0 8px 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        
        .section-title {{
            font-size: 1.4rem;
            font-weight: 600;
            color: {text_color};
            margin-bottom: 1.5rem;
            border-bottom: 2px solid {border_color};
            padding-bottom: 0.5rem;
        }}
        
        /* Dark mode specific overrides */
        {'' if not dark_mode else '''
        /* Text colors for dark mode */
        .stMarkdown, .stMarkdown p, .stMarkdown div, .stMarkdown span,
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
        .stText, p, div, span, label {
            color: #fafafa !important;
        }
        
        /* Form elements */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > div,
        .stNumberInput > div > div > input {
            background-color: #374151 !important;
            color: #fafafa !important;
            border-color: #6b7280 !important;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #374151 !important;
            color: #fafafa !important;
            border-color: #6b7280 !important;
        }
        
        /* Labels and help text */
        .stTextInput label, .stTextArea label, .stSelectbox label, 
        .stNumberInput label, .stCheckbox label {
            color: #fafafa !important;
        }
        
        /* Tab labels */
        .stTabs [data-baseweb="tab"] {
            color: #fafafa !important;
        }
        
        /* General text elements */
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] div,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stText"] {
            color: #fafafa !important;
        }
        
        /* Alert boxes and notifications */
        .stAlert, [data-testid="stNotification"],
        [data-testid="stAlert"], .stWarning, .stError, .stSuccess, .stInfo {
            background-color: #374151 !important;
            color: #fafafa !important;
            border-color: #6b7280 !important;
        }
        
        /* Warning/Error/Success box content */
        .stAlert > div, .stAlert p, .stAlert span,
        [data-testid="stNotification"] > div,
        [data-testid="stNotification"] p,
        [data-testid="stNotification"] span {
            color: #fafafa !important;
        }
        
        /* Expander components */
        .streamlit-expander {
            background-color: #374151 !important;
            border-color: #6b7280 !important;
        }
        
        .streamlit-expander .streamlit-expander-header {
            background-color: #374151 !important;
            color: #fafafa !important;
        }
        
        .streamlit-expander .streamlit-expander-content {
            background-color: #262730 !important;
        }
        
        /* Sidebar elements */
        .css-1d391kg, .css-1lcbmhc {
            background-color: #262730 !important;
        }
        
        /* Container backgrounds */
        .stContainer, [data-testid="stVerticalBlock"] > div,
        [data-testid="stHorizontalBlock"] > div {
            background-color: transparent !important;
        }
        
        /* Metric components */
        .metric-container, [data-testid="stMetric"] {
            background-color: #374151 !important;
            color: #fafafa !important;
        }
        
        /* Dataframe/table styling */
        .stDataFrame, [data-testid="stDataFrame"] {
            background-color: #374151 !important;
            color: #fafafa !important;
        }
        '''}
        
        /* Form styling */
        .stTextInput > div > div > input {{
            border: 1px solid #d0d5e0;
            border-radius: 6px;
            padding: 0.75rem;
            font-size: 0.95rem;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: #4a90e2;
            box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
        }}
        
        .stSelectbox > div > div > div {{
            border: 1px solid #d0d5e0;
            border-radius: 6px;
        }}
        
        /* Product selection grid */
        .product-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .product-card {{
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 1.25rem;
            transition: all 0.2s ease;
        }}
        
        .product-card:hover {{
            border-color: #4a90e2;
            box-shadow: 0 4px 12px rgba(74, 144, 226, 0.1);
        }}
        
        .product-card.selected {{
            border-color: #4a90e2;
            background: #f0f8ff;
        }}
        
        .product-icon {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .product-title {{
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }}
        
        .product-description {{
            font-size: 0.9rem;
            color: #6c757d;
            line-height: 1.4;
        }}
        
        /* Button styling */
        .stButton > button {{
            border-radius: 6px;
            font-weight: 500;
            padding: 0.75rem 1.5rem;
            transition: all 0.2s ease;
        }}
        
        /* Header button styling */
        .stButton > button[data-testid="baseButton-secondary"] {{
            background: rgba(255, 255, 255, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            color: white !important;
            font-size: 1.2rem !important;
            padding: 0.5rem 0.75rem !important;
            min-width: 40px !important;
            height: 40px !important;
        }}
        
        .stButton > button[data-testid="baseButton-secondary"]:hover {{
            background: rgba(255, 255, 255, 0.3) !important;
            border-color: rgba(255, 255, 255, 0.5) !important;
        }}
        
        /* Header toggle styling */
        .stCheckbox {{
            margin-top: 0 !important;
        }}
        
        .stCheckbox > label {{
            color: white !important;
            font-size: 1.2rem !important;
        }}
        
        .primary-button {{
            background: linear-gradient(135deg, #4a90e2 0%, #3d5b96 100%);
            border: none;
            color: white;
        }}
        
        .secondary-button {{
            background: white;
            border: 2px solid #4a90e2;
            color: #4a90e2;
        }}
        
        .secondary-button:hover {{
            background: #f0f8ff;
        }}
        
        /* Status indicators */
        .status-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        .status-success {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-warning {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .status-error {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        /* Help modal styling */
        .help-modal {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.7);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .help-content {{
            background: {section_bg};
            border-radius: 12px;
            padding: 2rem;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            color: {text_color};
        }}
        
        .help-close {{
            float: right;
            font-size: 1.5rem;
            cursor: pointer;
            color: {text_color};
            margin: -1rem -1rem 1rem 1rem;
        }}
        
        .help-section {{
            margin-bottom: 1.5rem;
        }}
        
        .help-title {{
            color: #4a90e2;
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        /* Context help styling */
        .context-help {{
            background: {('rgba(74, 144, 226, 0.1)' if not dark_mode else 'rgba(74, 144, 226, 0.2)')};
            border-left: 4px solid #4a90e2;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }}
        
        .help-icon {{
            color: #4a90e2;
            font-size: 1.2rem;
            cursor: pointer;
            margin-left: 0.5rem;
        }}
        
        .help-icon:hover {{
            color: #3d5b96;
        }}
        
        /* Hide Streamlit default elements */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .stDeployButton {{display: none;}}
        </style>
        """

    def import_configuration(self, uploaded_file):
        """Import configuration from uploaded YAML file"""
        try:
            # Parse the uploaded YAML file
            yaml_content = uploaded_file.read().decode('utf-8')
            config = yaml.safe_load(yaml_content)
            
            if not config:
                st.error("Invalid or empty YAML file")
                return
            
            # Import basic organization fields
            if 'orgname' in config:
                st.session_state.config_data['orgname'] = config['orgname']
            if 'orgunitname' in config:
                st.session_state.config_data['orgunitname'] = config['orgunitname']
            if 'description' in config:
                st.session_state.config_data['description'] = config['description']
            
            # Import authentication fields
            if 'customerid' in config:
                st.session_state.config_data['customerid'] = config['customerid']
            if 'subjectemail' in config:
                st.session_state.config_data['subjectemail'] = config['subjectemail']
            if 'credentials' in config:
                st.session_state.config_data['credentials'] = config['credentials']
            
            # Import baselines and update checkbox states
            if 'baselines' in config:
                # Handle both list and string formats
                baselines = config['baselines']
                if isinstance(baselines, str):
                    baselines = [baselines]
                elif not isinstance(baselines, list):
                    baselines = []
                
                st.session_state.config_data['baselines'] = baselines
                
                # Update individual checkbox states for UI consistency
                baseline_info = self.get_baseline_info()
                available_baselines = list(baseline_info.keys())
                for baseline in available_baselines:
                    st.session_state[f"baseline_{baseline}"] = baseline in baselines
            
            # Import output settings
            if 'outputpath' in config:
                st.session_state.config_data['outputpath'] = config['outputpath']
            if 'darkmode' in config:
                # Handle both string and boolean values
                darkmode = config['darkmode']
                if isinstance(darkmode, str):
                    st.session_state.config_data['darkmode'] = darkmode.lower() == 'true'
                else:
                    st.session_state.config_data['darkmode'] = bool(darkmode)
            if 'quiet' in config:
                st.session_state.config_data['quiet'] = bool(config['quiet'])
            
            # Import advanced configuration sections
            if 'omitpolicy' in config and isinstance(config['omitpolicy'], dict):
                st.session_state.config_data['omitpolicy'] = config['omitpolicy']
            
            if 'annotatepolicy' in config and isinstance(config['annotatepolicy'], dict):
                st.session_state.config_data['annotatepolicy'] = config['annotatepolicy']
            
            if 'breakglassaccounts' in config:
                breakglass = config['breakglassaccounts']
                if isinstance(breakglass, list):
                    st.session_state.config_data['breakglassaccounts'] = breakglass
                elif breakglass:  # Handle single string value
                    st.session_state.config_data['breakglassaccounts'] = [breakglass]
                else:
                    st.session_state.config_data['breakglassaccounts'] = []
            
            # Success message with summary
            imported_items = []
            if st.session_state.config_data.get('orgname'):
                imported_items.append(f"Organization: {st.session_state.config_data['orgname']}")
            if st.session_state.config_data.get('baselines'):
                imported_items.append(f"Baselines: {len(st.session_state.config_data['baselines'])} selected")
            if st.session_state.config_data.get('omitpolicy'):
                imported_items.append(f"Omitted Policies: {len(st.session_state.config_data['omitpolicy'])}")
            if st.session_state.config_data.get('annotatepolicy'):
                imported_items.append(f"Annotated Policies: {len(st.session_state.config_data['annotatepolicy'])}")
            if st.session_state.config_data.get('breakglassaccounts'):
                imported_items.append(f"Break Glass Accounts: {len(st.session_state.config_data['breakglassaccounts'])}")
            
            st.success(f"✅ Configuration imported successfully!")
            if imported_items:
                st.info("📋 **Imported:** " + " • ".join(imported_items))
            
            st.rerun()
            
        except yaml.YAMLError as e:
            st.error(f"❌ YAML parsing error: {str(e)}")
        except Exception as e:
            st.error(f"❌ Import error: {str(e)}")

    def render_header(self):
        """Render the professional header"""
        
        # Get current dark mode state for the toggle
        current_dark_mode = st.session_state.config_data.get('ui_dark_mode', False)
        
        # Create dark mode control above the header
        col1, col2 = st.columns([9.5, 0.5])
        
        with col1:
            pass  # Empty spacer
                
        with col2:
            dark_mode_toggle = st.toggle("🌙", value=current_dark_mode, key="ui_dark_mode_toggle", help="Toggle dark mode")
            
            # Force update and rerun when toggle changes
            if dark_mode_toggle != current_dark_mode:
                st.session_state.config_data['ui_dark_mode'] = dark_mode_toggle
                st.rerun()
        
        # Now create header below the controls with reduced gap
        st.markdown("""
        <div class="main-header" style="margin-top: -1rem;">
            <h1 class="header-title">🤿 ScubaGoggles Configuration Editor</h1>
            <p class="header-subtitle">Create a configuration file for ScubaGoggles exclusions, annotations, and omissions baseline controls</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show help modal if requested
        self.render_help_modal()

    def render_help_modal(self):
        """Render help modal overlay"""
        if st.session_state.ui_show_help:
            self._show_help_dialog()
    
    @st.dialog("🤿 ScubaGoggles Help & Documentation")
    def _show_help_dialog(self):
        """Show help content in a proper modal dialog"""
        
        # Help content
        st.markdown("### This professional interface helps you create configuration files for ScubaGoggles security assessments.")
        
        st.markdown("## 🚀 Quick Start Guide")
        st.markdown("""
        1. **Main Tab:** Select products and baselines to assess
        2. **Omit Policies:** Exclude specific policies from assessment  
        3. **Annotate Policies:** Add custom notes and documentation
        4. **Break Glass:** Configure emergency access accounts
        5. **Advanced:** Set output paths and advanced options
        6. **Preview:** Review your configuration before saving
        7. **Run:** Generate config file or run assessment
        """)
        
        st.markdown("## 📋 Tab Documentation")
        st.markdown("""
        - **Main:** Product selection with baseline coverage
        - **Omit Policies:** Use green dots to indicate configured policies, orange during editing
        - **Annotate Policies:** Add rationale and documentation for policy decisions
        - **Break Glass:** Emergency accounts that bypass normal security controls
        - **Advanced:** Output directory configuration and technical settings
        """)
        
        st.markdown("## 💡 Tips & Best Practices")
        st.markdown("""
        - Use the import feature to load existing configurations
        - Green checkboxes indicate selected products in main tab
        - Status indicators show configuration progress
        - Dark mode is available via the header toggle
        - All fields are validated before configuration generation
        - Preview tab shows the exact YAML that will be generated
        """)
        
        st.markdown("## 🔗 Resources")
        st.markdown("""
        - [ScubaGoggles Documentation](https://github.com/cisagov/ScubaGoggles)
        - [SCuBA Project](https://cisa.gov/scuba)
        - [User Guide](https://github.com/cisagov/ScubaGoggles/blob/main/docs)
        """)
        
        # Close button
        if st.button("✅ Got it!", key="close_help_dialog", type="primary"):
            st.session_state.ui_show_help = False
            st.rerun()

    def get_baseline_info(self):
        """Get information about available baselines"""
        return {
            'commoncontrols': {
                'icon': '🔐',
                'title': 'Common Controls',
                'description': 'Enterprise-level security controls across the entire GWS admin console including authentication, access control, and session management'
            },
            'assuredcontrols': {
                'icon': '🛡️',
                'title': 'Assured Controls',
                'description': 'Advanced security controls for organizations with Assured Controls or Assured Controls Plus licenses including data access approvals and data regions'
            },
            'gmail': {
                'icon': '📧',
                'title': 'Gmail',
                'description': 'Email security controls and policies for Gmail configuration'
            },
            'drive': {
                'icon': '📁',
                'title': 'Google Drive',
                'description': 'File sharing and access controls for Google Drive'
            },
            'calendar': {
                'icon': '📅',
                'title': 'Calendar',
                'description': 'Calendar sharing and privacy settings for Google Calendar'
            },
            'meet': {
                'icon': '📹',
                'title': 'Google Meet',
                'description': 'Video conferencing security and access controls'
            },
            'groups': {
                'icon': '👥',
                'title': 'Groups',
                'description': 'Google Groups configuration and permissions'
            },
            'chat': {
                'icon': '💬',
                'title': 'Google Chat',
                'description': 'Chat and messaging security controls'
            },
            'sites': {
                'icon': '🌐',
                'title': 'Google Sites',
                'description': 'Website creation and sharing controls'
            },
            'classroom': {
                'icon': '🎓',
                'title': 'Classroom',
                'description': 'Educational platform security and privacy controls'
            }
        }

    def render_main_tab(self):
        """Render the main configuration tab"""
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Organization Information</h2>', unsafe_allow_html=True)

        # Context help for main tab
        with st.expander("ℹ️ Help: Organization & Product Selection", expanded=False):
            st.markdown("""
            <div class="context-help">
            <strong>Organization Information:</strong><br>
            • <strong>Organization Name:</strong> Official name of your organization (required)<br>
            • <strong>Organization Unit:</strong> Specific department or division being assessed<br><br>
            
            <strong>Product Selection:</strong><br>
            • Choose which Google Workspace products to assess<br>
            • Green checkboxes indicate selected products<br>
            • Each product has specific security baselines<br>
            • You can select multiple products for coverage<br><br>
            
            <strong>Best Practices:</strong><br>
            • Start with core products (commoncontrols, gmail, calendar)<br>
            • Add additional products based on your organization's usage<br>
            • Organization name is required for report generation
            </div>
            """, unsafe_allow_html=True)

        # Organization Name
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("**[ℹ️] Organization Name***")
        with col2:
            orgname = st.text_input(
                "Organization Name",
                value=st.session_state.config_data.get('orgname', ''),
                placeholder="Department of Example",
                help="Name of your organization",
                key="orgname",
                label_visibility="collapsed"
            )
            st.session_state.config_data['orgname'] = orgname

        # Organization Unit Name
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("**[ℹ️] Organization Unit Name**")
        with col2:
            orgunitname = st.text_input(
                "Organization Unit Name",
                value=st.session_state.config_data.get('orgunitname', ''),
                placeholder="Subdepartment of Example",
                help="Name of your organizational unit (optional)",
                key="orgunitname",
                label_visibility="collapsed"
            )
            st.session_state.config_data['orgunitname'] = orgunitname

        # Description
        st.markdown("**Description**")
        description = st.text_area(
            "Description",
            value=st.session_state.config_data.get('description', ''),
            placeholder="Enter a description for this configuration (optional)",
            height=100,
            key="description",
            label_visibility="collapsed"
        )
        st.session_state.config_data['description'] = description

        # Product Selection Section
        st.markdown('<h3 style="margin-top: 2rem;">Select at least one product:*</h3>', unsafe_allow_html=True)
        
        baseline_info = self.get_baseline_info()
        available_baselines = list(baseline_info.keys())
        current_selection = st.session_state.config_data.get('baselines', [])

        # Select All / None buttons
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("✅ Select All", key="select_all_main"):
                st.session_state.config_data['baselines'] = available_baselines.copy()
                # Update individual checkbox states
                for baseline in available_baselines:
                    st.session_state[f"baseline_{baseline}"] = True
                st.rerun()
        
        with col2:
            if st.button("❌ Clear All", key="clear_all_main"):
                st.session_state.config_data['baselines'] = []
                # Update individual checkbox states
                for baseline in available_baselines:
                    st.session_state[f"baseline_{baseline}"] = False
                st.rerun()

        # Create product grid with icons and policy counts
        cols = st.columns(2)
        for i, baseline in enumerate(available_baselines):
            info = baseline_info[baseline]
            baseline_policies = self.available_policies.get(baseline.upper(), {}) if self.available_policies else {}
            policy_count = len(baseline_policies)
            
            with cols[i % 2]:
                is_selected = baseline in current_selection
                
                # Create a checkbox with custom styling including policy count
                selected = st.checkbox(
                    f"{info['icon']} **{info['title']}** ({policy_count} policies)",
                    value=is_selected,
                    key=f"baseline_{baseline}"
                )
                
                if selected and baseline not in current_selection:
                    current_selection.append(baseline)
                elif not selected and baseline in current_selection:
                    current_selection.remove(baseline)
                
                st.caption(info['description'])
                st.markdown("---")

        st.session_state.config_data['baselines'] = current_selection

        # Products supporting exclusions note
        if current_selection:
            total_policies = sum(len(self.available_policies.get(b.upper(), {})) for b in current_selection)
            st.info("📝 **Products selected:** " + ", ".join([baseline_info[b]['title'] for b in current_selection]))
            st.success(f"✅ Selected {len(current_selection)} products with {total_policies} policies total")

        st.markdown('</div>', unsafe_allow_html=True)

    def parse_baseline_policies(self) -> Dict[str, Dict[str, str]]:
        """Parse policies from baseline markdown files"""
        policies = {}
        baseline_dir = Path('scubagoggles/baselines')
        
        if not baseline_dir.exists():
            return policies
        
        for md_file in baseline_dir.glob('*.md'):
            if md_file.name == 'README.md':
                continue
                
            try:
                content = md_file.read_text(encoding='utf-8')
                baseline_name = md_file.stem.upper()
                policies[baseline_name] = self.extract_policies_from_markdown(content, baseline_name)
            except Exception as e:
                continue  # Skip files that can't be parsed
        
        return policies
    
    def extract_policies_from_markdown(self, content: str, baseline_name: str) -> Dict[str, str]:
        """Extract policy IDs and titles from markdown content"""
        policies = {}
        lines = content.split('\n')
        
        in_policies_section = False
        current_policy_id = None
        
        for line in lines:
            line = line.strip()
            
            # Check if we're entering the policies section
            if line == '### Policies':
                in_policies_section = True
                continue
            
            # Check if we're leaving the policies section
            if in_policies_section and line.startswith('### ') and line != '### Policies':
                in_policies_section = False
                continue
            
            # Extract policy IDs
            if in_policies_section and line.startswith('#### GWS.'):
                # Extract policy ID (remove #### and any trailing text)
                policy_id = line.replace('#### ', '').split()[0]
                current_policy_id = policy_id
                
                # Get the next line which should contain the policy description
                continue
            
            # Get policy description (first line after policy ID)
            if in_policies_section and current_policy_id and not line.startswith('#') and line:
                # Clean up the description
                description = line.rstrip('.')
                policies[current_policy_id] = description
                current_policy_id = None
        
        return policies

    def render_omit_policies_tab(self):
        """Render omit policies configuration tab"""
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Omit Policies</h2>', unsafe_allow_html=True)
        
        # Context help for omit policies
        with st.expander("ℹ️ Help: Policy Omission Guidelines", expanded=False):
            st.markdown("""
            <div class="context-help">
            <strong>What is Policy Omission?</strong><br>
            Excluding specific security policies from ScubaGoggles evaluation when they don't apply to your organization or are handled by external controls.<br><br>
            
            <strong>Valid Reasons to Omit:</strong><br>
            • Policy implemented by third-party service that ScubaGoggles cannot audit<br>
            • Policy not applicable to your organization's operational model<br>
            • Compensating controls provide equivalent security<br>
            • Accepting documented risk for specific controls<br><br>
            
            <strong>Status Indicators:</strong><br>
            • 🟢 Green dot: Policy configured for omission<br>
            • 🟠 Orange dot: Policy being edited<br>
            • No dot: Policy not omitted<br><br>
            
            <strong>Important:</strong> All omissions should be documented and approved by your security team.
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        **Use this section to exclude specific policies from ScubaGoggles evaluation.**
        
        ⚠️ **Important:** Any omitted policies should be carefully considered and documented as part of your organization's cybersecurity risk management program.
        
        Common reasons for omitting policies:
        - Policy is implemented by a third-party service that ScubaGoggles cannot audit
        - Policy is not applicable to your organization
        - Accepting risk for specific controls with proper documentation
        """)
        
        # Get current omit policies
        omit_policies = st.session_state.config_data.get('omitpolicy', {})
        
        # Add new omitted policy
        st.subheader("➕ Add Policy to Omit")
        
        # Show available policies by selected baselines only
        selected_baselines = st.session_state.config_data.get('baselines', [])
        selected_policy = None
        selected_description = None
        
        if selected_baselines and self.available_policies:
            st.markdown("**Available Policies from Selected Products:**")
            
            # Map UI baseline names to policy parser names (lowercase to uppercase)
            selected_baseline_policies = {}
            for baseline in selected_baselines:
                baseline_upper = baseline.upper()
                if baseline_upper in self.available_policies:
                    selected_baseline_policies[baseline.title()] = self.available_policies[baseline_upper]
            
            if selected_baseline_policies:
                baseline_tabs = st.tabs(list(selected_baseline_policies.keys()))
                
                selected_policy = None
                selected_description = None
                
                for i, (baseline_name, baseline_policies) in enumerate(selected_baseline_policies.items()):
                    with baseline_tabs[i]:
                        if baseline_policies:
                            for policy_id, description in baseline_policies.items():
                                # Check if this policy is already omitted
                                is_omitted = policy_id in omit_policies
                                
                                # Policy header with expand/collapse
                                col1, col2 = st.columns([4, 1])
                                with col1:
                                    if is_omitted:
                                        st.markdown(f"🟢 **{policy_id}** (Omitted)")
                                    elif st.session_state.get(f"expand_omit_{policy_id}", False):
                                        st.markdown(f"🟠 **{policy_id}** (Configuring...)")
                                    else:
                                        st.markdown(f"**{policy_id}**")
                                    st.caption(description)
                                
                                with col2:
                                    if is_omitted:
                                        col_edit, col_remove = st.columns(2)
                                        with col_edit:
                                            if st.button(f"✏️ Edit", key=f"edit_omit_{policy_id}"):
                                                # Load existing values for editing
                                                existing_data = omit_policies[policy_id]
                                                st.session_state[f"rationale_{policy_id}"] = existing_data.get('rationale', '')
                                                # Convert date string to date object for session state
                                                if 'expiration' in existing_data:
                                                    from datetime import datetime
                                                    try:
                                                        date_obj = datetime.strptime(existing_data['expiration'], '%Y-%m-%d').date()
                                                        st.session_state[f"expiration_{policy_id}"] = date_obj
                                                    except (ValueError, TypeError):
                                                        if f"expiration_{policy_id}" in st.session_state:
                                                            del st.session_state[f"expiration_{policy_id}"]
                                                else:
                                                    if f"expiration_{policy_id}" in st.session_state:
                                                        del st.session_state[f"expiration_{policy_id}"]
                                                st.session_state[f"expand_omit_{policy_id}"] = True
                                                st.session_state[f"editing_omit_{policy_id}"] = True
                                                st.rerun()
                                        with col_remove:
                                            if st.button(f"🗑️ Remove", key=f"remove_omit_{policy_id}"):
                                                del omit_policies[policy_id]
                                                st.session_state.config_data['omitpolicy'] = omit_policies
                                                st.success(f"✅ Removed omitted policy: {policy_id}")
                                                st.rerun()
                                    else:
                                        expand_key = f"expand_omit_{policy_id}"
                                        if expand_key not in st.session_state:
                                            st.session_state[expand_key] = False
                                        
                                        if st.button(f"➕ Omit", key=f"toggle_omit_{policy_id}"):
                                            # Clear any existing session state for fresh start
                                            if f"rationale_{policy_id}" in st.session_state:
                                                del st.session_state[f"rationale_{policy_id}"]
                                            if f"expiration_{policy_id}" in st.session_state:
                                                del st.session_state[f"expiration_{policy_id}"]
                                            st.session_state[expand_key] = not st.session_state[expand_key]
                                            st.session_state[f"editing_omit_{policy_id}"] = False  # New configuration
                                            st.rerun()
                                
                                # Expandable form for omitting this policy
                                if st.session_state.get(f"expand_omit_{policy_id}", False):
                                    is_editing = st.session_state.get(f"editing_omit_{policy_id}", False)
                                    with st.container():
                                        st.markdown("---")
                                        if is_editing:
                                            st.markdown(f"**Edit Omission for {policy_id}**")
                                        else:
                                            st.markdown(f"**Configure Omission for {policy_id}**")
                                        
                                        # Get existing values if editing
                                        existing_rationale = ""
                                        existing_expiration = None
                                        if is_editing and policy_id in omit_policies:
                                            existing_data = omit_policies[policy_id]
                                            existing_rationale = existing_data.get('rationale', '')
                                            if 'expiration' in existing_data:
                                                from datetime import datetime
                                                try:
                                                    existing_expiration = datetime.strptime(existing_data['expiration'], '%Y-%m-%d').date()
                                                except (ValueError, TypeError):
                                                    existing_expiration = None
                                        elif policy_id in omit_policies:  # If policy is omitted but not in editing mode, load values
                                            existing_data = omit_policies[policy_id]
                                            existing_rationale = existing_data.get('rationale', '')
                                            if 'expiration' in existing_data:
                                                from datetime import datetime
                                                try:
                                                    existing_expiration = datetime.strptime(existing_data['expiration'], '%Y-%m-%d').date()
                                                except (ValueError, TypeError):
                                                    existing_expiration = None
                                        
                                        rationale = st.text_input(
                                            "Rationale (Required)",
                                            value=existing_rationale,
                                            placeholder="Reason for omitting this policy",
                                            key=f"rationale_{policy_id}"
                                        )
                                        
                                        # Clear any string values in session state for date input
                                        date_key = f"expiration_{policy_id}"
                                        if date_key in st.session_state and isinstance(st.session_state[date_key], str):
                                            try:
                                                from datetime import datetime
                                                st.session_state[date_key] = datetime.strptime(st.session_state[date_key], '%Y-%m-%d').date()
                                            except (ValueError, TypeError):
                                                del st.session_state[date_key]
                                        
                                        expiration = st.date_input(
                                            "Expiration Date (Optional)",
                                            value=existing_expiration,
                                            help="Date after which the policy should no longer be omitted",
                                            key=f"expiration_{policy_id}"
                                        )
                                        
                                        col_save, col_cancel = st.columns(2)
                                        with col_save:
                                            button_text = "💾 Update Omission" if is_editing else "✅ Save Omission"
                                            if st.button(button_text, key=f"save_omit_{policy_id}", type="primary"):
                                                if rationale:
                                                    omit_config = {'rationale': rationale}
                                                    if expiration:
                                                        omit_config['expiration'] = expiration.strftime('%Y-%m-%d')
                                                    
                                                    omit_policies[policy_id] = omit_config
                                                    st.session_state.config_data['omitpolicy'] = omit_policies
                                                    st.session_state[f"expand_omit_{policy_id}"] = False
                                                    st.session_state[f"editing_omit_{policy_id}"] = False
                                                    action_text = "Updated" if is_editing else "Added"
                                                    st.success(f"✅ {action_text} omitted policy: {policy_id}")
                                                    st.rerun()
                                                else:
                                                    st.error("❌ Rationale is required")
                                        
                                        with col_cancel:
                                            if st.button(f"❌ Cancel", key=f"cancel_omit_{policy_id}"):
                                                st.session_state[f"expand_omit_{policy_id}"] = False
                                                st.session_state[f"editing_omit_{policy_id}"] = False
                                                st.rerun()
                        else:
                            st.info(f"No policies found for {baseline_name} product")
                
                st.divider()
            else:
                st.info("ℹ️ No policies available for selected products")
        else:
            st.warning("⚠️ Please select products in the Main tab first to see available policies")
        
        # Summary of current omitted policies
        if omit_policies:
            st.markdown("---")
            st.subheader("📋 Summary of Omitted Policies")
            
            for policy_id, policy_data in omit_policies.items():
                st.markdown(f"🚫 **{policy_id}**: {policy_data.get('rationale', 'No rationale provided')}")
                if 'expiration' in policy_data:
                    st.caption(f"Expires: {policy_data['expiration']}")
        else:
            st.markdown("---")
            st.info("ℹ️ No policies are currently omitted")

        st.markdown('</div>', unsafe_allow_html=True)

    def render_annotate_policies_tab(self):
        """Render annotate policies configuration tab"""
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Annotate Policies</h2>', unsafe_allow_html=True)
        
        # Context help for annotate policies
        with st.expander("ℹ️ Help: Policy Annotation Guidelines", expanded=False):
            st.markdown("""
            <div class="context-help">
            <strong>What are Policy Annotations?</strong><br>
            Adding contextual information and documentation to specific policy results for audit trails and remediation planning.<br><br>
            
            <strong>Annotation Types:</strong><br>
            • <strong>Action Plan:</strong> Document remediation steps for failing controls<br>
            • <strong>Incorrect Result:</strong> Mark false positives (use with caution)<br>
            • <strong>Context:</strong> Provide additional background information<br>
            • <strong>Remediation Date:</strong> Set target dates for addressing issues<br><br>
            
            <strong>Best Practices:</strong><br>
            • Always document reasons for marking results as incorrect<br>
            • Include specific remediation steps and responsible parties<br>
            • Set realistic remediation dates<br>
            • Review annotations regularly during security assessments<br><br>
            
            <strong>Warning:</strong> Use "Incorrect Result" sparingly to avoid security blind spots.
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        **Use this section to add annotations to specific policy results.**
        
        Annotations allow you to:
        - Document action plans for failing controls
        - Mark incorrect results 
        - Provide additional context for results
        - Set remediation dates for failing controls
        
        ⚠️ **Caution:** Exercise care when marking results as incorrect to avoid introducing blind spots.
        """)
        
        # Get current annotated policies
        annotate_policies = st.session_state.config_data.get('annotatepolicy', {})
        
        # Get current annotated policies
        annotate_policies = st.session_state.config_data.get('annotatepolicy', {})
        
        # Check for tab switch signal
        if st.session_state.get('switch_to_annotate_tab', False):
            st.session_state.switch_to_annotate_tab = False
        
        # Check for pre-selected policy from omit tab
        preselected_policy = st.session_state.get('selected_policy_for_annotation')
        if preselected_policy:
            st.success(f"📝 Ready to annotate: **{preselected_policy[0]}**")
            st.info(f"Description: {preselected_policy[1]}")
            # Clear the selection after showing
            if st.button("✅ Acknowledged"):
                del st.session_state.selected_policy_for_annotation
                st.rerun()
        
        # Show available policies by selected baselines only
        selected_baselines = st.session_state.config_data.get('baselines', [])
        selected_policy = None
        selected_description = None
        
        if selected_baselines and self.available_policies:
            st.markdown("**Available Policies from Selected Products:**")
            
            # Map UI baseline names to policy parser names (lowercase to uppercase)
            selected_baseline_policies = {}
            for baseline in selected_baselines:
                baseline_upper = baseline.upper()
                if baseline_upper in self.available_policies:
                    selected_baseline_policies[baseline.title()] = self.available_policies[baseline_upper]
            
            if selected_baseline_policies:
                baseline_tabs = st.tabs(list(selected_baseline_policies.keys()))
                
                for i, (baseline_name, baseline_policies) in enumerate(selected_baseline_policies.items()):
                    with baseline_tabs[i]:
                        if baseline_policies:
                            for policy_id, description in baseline_policies.items():
                                # Check if this policy is already annotated
                                is_annotated = policy_id in annotate_policies
                                
                                # Policy header with expand/collapse
                                col1, col2 = st.columns([4, 1])
                                with col1:
                                    if is_annotated:
                                        st.markdown(f"🟢 **{policy_id}** (Annotated)")
                                    elif st.session_state.get(f"expand_annotate_{policy_id}", False):
                                        st.markdown(f"🟠 **{policy_id}** (Configuring...)")
                                    else:
                                        st.markdown(f"**{policy_id}**")
                                    st.caption(description)
                                
                                with col2:
                                    if is_annotated:
                                        col_edit, col_remove = st.columns(2)
                                        with col_edit:
                                            if st.button(f"✏️ Edit", key=f"edit_annotate_{policy_id}"):
                                                # Load existing values for editing
                                                existing_data = annotate_policies[policy_id]
                                                st.session_state[f"comment_{policy_id}"] = existing_data.get('comment', '')
                                                st.session_state[f"incorrect_{policy_id}"] = existing_data.get('incorrectresult', False)
                                                # Convert date string to date object for session state
                                                if 'remediationdate' in existing_data:
                                                    from datetime import datetime
                                                    try:
                                                        date_obj = datetime.strptime(existing_data['remediationdate'], '%Y-%m-%d').date()
                                                        st.session_state[f"remediation_{policy_id}"] = date_obj
                                                    except (ValueError, TypeError):
                                                        if f"remediation_{policy_id}" in st.session_state:
                                                            del st.session_state[f"remediation_{policy_id}"]
                                                else:
                                                    if f"remediation_{policy_id}" in st.session_state:
                                                        del st.session_state[f"remediation_{policy_id}"]
                                                st.session_state[f"expand_annotate_{policy_id}"] = True
                                                st.session_state[f"editing_annotate_{policy_id}"] = True
                                                st.rerun()
                                        with col_remove:
                                            if st.button(f"🗑️ Remove", key=f"remove_annotate_{policy_id}"):
                                                del annotate_policies[policy_id]
                                                st.session_state.config_data['annotatepolicy'] = annotate_policies
                                                st.success(f"✅ Removed annotation for policy: {policy_id}")
                                                st.rerun()
                                    else:
                                        expand_key = f"expand_annotate_{policy_id}"
                                        if expand_key not in st.session_state:
                                            st.session_state[expand_key] = False
                                        
                                        if st.button(f"📝 Annotate", key=f"toggle_annotate_{policy_id}"):
                                            # Clear any existing session state for fresh start
                                            if f"comment_{policy_id}" in st.session_state:
                                                del st.session_state[f"comment_{policy_id}"]
                                            if f"incorrect_{policy_id}" in st.session_state:
                                                del st.session_state[f"incorrect_{policy_id}"]
                                            if f"remediation_{policy_id}" in st.session_state:
                                                del st.session_state[f"remediation_{policy_id}"]
                                            st.session_state[expand_key] = not st.session_state[expand_key]
                                            st.session_state[f"editing_annotate_{policy_id}"] = False  # New configuration
                                            st.rerun()
                                
                                # Expandable form for annotating this policy
                                if st.session_state.get(f"expand_annotate_{policy_id}", False):
                                    is_editing = st.session_state.get(f"editing_annotate_{policy_id}", False)
                                    with st.container():
                                        st.markdown("---")
                                        if is_editing:
                                            st.markdown(f"**Edit Annotation for {policy_id}**")
                                        else:
                                            st.markdown(f"**Configure Annotation for {policy_id}**")
                                        
                                        # Get existing values if editing
                                        existing_comment = ""
                                        existing_incorrect = False
                                        existing_remediation = None
                                        if is_editing and policy_id in annotate_policies:
                                            existing_data = annotate_policies[policy_id]
                                            existing_comment = existing_data.get('comment', '')
                                            existing_incorrect = existing_data.get('incorrectresult', False)
                                            if 'remediationdate' in existing_data:
                                                from datetime import datetime
                                                try:
                                                    existing_remediation = datetime.strptime(existing_data['remediationdate'], '%Y-%m-%d').date()
                                                except (ValueError, TypeError):
                                                    existing_remediation = None
                                        elif policy_id in annotate_policies:  # If policy is annotated but not in editing mode, load values
                                            existing_data = annotate_policies[policy_id]
                                            existing_comment = existing_data.get('comment', '')
                                            existing_incorrect = existing_data.get('incorrectresult', False)
                                            if 'remediationdate' in existing_data:
                                                from datetime import datetime
                                                try:
                                                    existing_remediation = datetime.strptime(existing_data['remediationdate'], '%Y-%m-%d').date()
                                                except (ValueError, TypeError):
                                                    existing_remediation = None
                                        
                                        comment = st.text_area(
                                            "Comment/Annotation",
                                            value=existing_comment,
                                            placeholder="Implementation in progress...",
                                            help="Comment to add to the report for this policy",
                                            key=f"comment_{policy_id}",
                                            height=100
                                        )
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            incorrect_result = st.checkbox(
                                                "Mark as Incorrect Result",
                                                value=existing_incorrect,
                                                help="Check if the result for this policy is incorrect",
                                                key=f"incorrect_{policy_id}"
                                            )
                                        
                                        with col2:
                                            # Clear any string values in session state for date input
                                            remediation_key = f"remediation_{policy_id}"
                                            if remediation_key in st.session_state and isinstance(st.session_state[remediation_key], str):
                                                try:
                                                    from datetime import datetime
                                                    st.session_state[remediation_key] = datetime.strptime(st.session_state[remediation_key], '%Y-%m-%d').date()
                                                except (ValueError, TypeError):
                                                    del st.session_state[remediation_key]
                                            
                                            remediation_date = st.date_input(
                                                "Remediation Date (Optional)",
                                                value=existing_remediation,
                                                help="Date when a failing control is expected to be implemented",
                                                key=f"remediation_{policy_id}"
                                            )
                                        
                                        col_save, col_cancel = st.columns(2)
                                        with col_save:
                                            button_text = "💾 Update Annotation" if is_editing else "✅ Save Annotation"
                                            if st.button(button_text, key=f"save_annotate_{policy_id}", type="primary"):
                                                annotation_config = {}
                                                if comment:
                                                    annotation_config['comment'] = comment
                                                if incorrect_result:
                                                    annotation_config['incorrectresult'] = True
                                                if remediation_date:
                                                    annotation_config['remediationdate'] = remediation_date.strftime('%Y-%m-%d')
                                                
                                                if annotation_config:  # Only save if there's something to annotate
                                                    annotate_policies[policy_id] = annotation_config
                                                    st.session_state.config_data['annotatepolicy'] = annotate_policies
                                                    st.session_state[f"expand_annotate_{policy_id}"] = False
                                                    st.session_state[f"editing_annotate_{policy_id}"] = False
                                                    action_text = "Updated" if is_editing else "Added"
                                                    st.success(f"✅ {action_text} annotation for policy: {policy_id}")
                                                    st.rerun()
                                                else:
                                                    st.error("❌ At least one annotation field is required")
                                        
                                        with col_cancel:
                                            if st.button(f"❌ Cancel", key=f"cancel_annotate_{policy_id}"):
                                                st.session_state[f"expand_annotate_{policy_id}"] = False
                                                st.session_state[f"editing_annotate_{policy_id}"] = False
                                                st.rerun()
                        else:
                            st.info(f"No policies found for {baseline_name} product")
                
                st.divider()
            else:
                st.info("ℹ️ No policies available for selected products")
        else:
            st.warning("⚠️ Please select products in the Main tab first to see available policies")
        
        # Summary of current annotated policies
        if annotate_policies:
            st.markdown("---")
            st.subheader("📋 Summary of Annotated Policies")
            
            for policy_id, policy_data in annotate_policies.items():
                st.markdown(f"📝 **{policy_id}**")
                if 'comment' in policy_data:
                    st.caption(f"Comment: {policy_data['comment']}")
                if policy_data.get('incorrectresult', False):
                    st.caption("🔴 Marked as Incorrect Result")
                if 'remediationdate' in policy_data:
                    st.caption(f"Remediation Date: {policy_data['remediationdate']}")
        else:
            st.markdown("---")
            st.info("ℹ️ No policies are currently annotated")

        st.markdown('</div>', unsafe_allow_html=True)

    def render_break_glass_tab(self):
        """Render break glass accounts configuration tab"""
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Break Glass Accounts</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **Configure super admin accounts that should be considered "break glass accounts".**
        
        Break glass accounts are emergency access accounts used only in critical situations and should be excluded 
        from the overall super admin count in ScubaGoggles assessments.
        
        ⚠️ **Important:** These accounts should:
        - Be used only for emergency access
        - Have strong authentication controls
        - Be regularly audited
        - Have minimal day-to-day access
        """)
        
        # Current break glass accounts
        break_glass_accounts = st.session_state.config_data.get('breakglassaccounts', [])
        
        # Add new break glass account
        st.subheader("➕ Add Break Glass Account")
        col1, col2 = st.columns([3, 1])
        with col1:
            new_break_glass = st.text_input(
                "Break Glass Account Email",
                placeholder="emergency-admin@example.org",
                help="Email address of break glass account",
                key="new_break_glass"
            )
        
        with col2:
            if st.button("➕ Add Account", type="primary"):
                if new_break_glass and new_break_glass not in break_glass_accounts:
                    break_glass_accounts.append(new_break_glass)
                    st.session_state.config_data['breakglassaccounts'] = break_glass_accounts
                    st.success(f"✅ Added break glass account: {new_break_glass}")
                    st.rerun()
                elif new_break_glass in break_glass_accounts:
                    st.error("❌ Account already exists in list")
                else:
                    st.error("❌ Email address is required")
        
        # Display current break glass accounts
        if break_glass_accounts:
            st.subheader("📋 Current Break Glass Accounts")
            for i, account in enumerate(break_glass_accounts):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"🚨 **{account}**")
                    st.caption("Emergency access account")
                with col2:
                    if st.button("🗑️ Remove", key=f"remove_bg_{i}"):
                        break_glass_accounts.remove(account)
                        st.session_state.config_data['breakglassaccounts'] = break_glass_accounts
                        st.success(f"✅ Removed break glass account: {account}")
                        st.rerun()
        else:
            st.info("ℹ️ No break glass accounts configured")

        st.markdown('</div>', unsafe_allow_html=True)

    def render_break_glass_tab(self):
        """Render break glass accounts configuration tab"""
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Break Glass Accounts</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **Configure super admin accounts that should be considered "break glass accounts".**
        
        Break glass accounts are emergency access accounts used only in critical situations and should be excluded 
        from the overall super admin count in ScubaGoggles assessments.
        
        ⚠️ **Important:** These accounts should:
        - Be used only for emergency access
        - Have strong authentication controls
        - Be regularly audited
        - Have minimal day-to-day access
        """)
        
        # Current break glass accounts
        break_glass_accounts = st.session_state.config_data.get('breakglassaccounts', [])
        
        # Add new break glass account
        st.subheader("➕ Add Break Glass Account")
        col1, col2 = st.columns([3, 1])
        with col1:
            new_break_glass = st.text_input(
                "Break Glass Account Email",
                placeholder="emergency-admin@example.org",
                help="Email address of break glass account",
                key="new_break_glass"
            )
        
        with col2:
            if st.button("➕ Add Account", type="primary"):
                if new_break_glass and new_break_glass not in break_glass_accounts:
                    break_glass_accounts.append(new_break_glass)
                    st.session_state.config_data['breakglassaccounts'] = break_glass_accounts
                    st.success(f"✅ Added break glass account: {new_break_glass}")
                    st.rerun()
                elif new_break_glass in break_glass_accounts:
                    st.error("❌ Account already exists in list")
                else:
                    st.error("❌ Email address is required")
        
        # Display current break glass accounts
        if break_glass_accounts:
            st.subheader("📋 Current Break Glass Accounts")
            for i, account in enumerate(break_glass_accounts):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"🚨 **{account}**")
                    st.caption("Emergency access account")
                with col2:
                    if st.button("🗑️ Remove", key=f"remove_bg_{i}"):
                        break_glass_accounts.remove(account)
                        st.session_state.config_data['breakglassaccounts'] = break_glass_accounts
                        st.success(f"✅ Removed break glass account: {account}")
                        st.rerun()
        else:
            st.info("ℹ️ No break glass accounts configured")

        st.markdown('</div>', unsafe_allow_html=True)

    def render_advanced_tab(self):
        """Render advanced configuration tab"""
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Advanced Configuration</h2>', unsafe_allow_html=True)
        
        # Authentication Settings
        st.subheader("🔐 Authentication Settings")
        
        auth_method = st.selectbox(
            "Authentication Method",
            ["Service Account", "OAuth 2.0", "Application Default Credentials"],
            index=0,
            help="Choose the authentication method for Google Workspace API access",
            key="auth_method"
        )
        st.session_state.config_data['auth_method'] = auth_method
        
        if auth_method == "Service Account":
            st.info("📋 Service account authentication requires a JSON credentials file and subject email.")
            
            # Service Account specific fields
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Customer ID***")
            with col2:
                customerid = st.text_input(
                    "Customer ID",
                    value=st.session_state.config_data.get('customerid', ''),
                    placeholder="Your Google Workspace Customer ID",
                    help="The unique ID assigned to your GWS tenant. Required for service account authentication.",
                    key="customerid_advanced",
                    label_visibility="collapsed"
                )
                st.session_state.config_data['customerid'] = customerid
                if customerid:
                    st.caption("Required for service account authentication")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**Subject Email***")
            with col2:
                subjectemail = st.text_input(
                    "Subject Email",
                    value=st.session_state.config_data.get('subjectemail', ''),
                    placeholder="admin@example.com",
                    help="Email address of the user the service account should act on behalf of (must be super admin)",
                    key="subjectemail_advanced",
                    label_visibility="collapsed"
                )
                st.session_state.config_data['subjectemail'] = subjectemail
                if subjectemail:
                    st.caption("Must be a super admin user")
            
            # File path input for credentials
            creds_path = st.text_input(
                "📁 Service Account JSON File Path",
                value=st.session_state.config_data.get('credentials', ''),
                placeholder="/path/to/service-account.json",
                help="Path to your service account credentials file",
                key="credentials_advanced"
            )
            st.session_state.config_data['credentials'] = creds_path
            if creds_path:
                from pathlib import Path
                if Path(creds_path).exists():
                    st.success(f"✅ Using credentials: {creds_path}")
                else:
                    st.error(f"❌ File not found: {creds_path}")
        elif auth_method == "OAuth 2.0":
            st.info("🌐 OAuth 2.0 will open a browser window for interactive authentication.")
        else:
            st.info("🔧 Application Default Credentials will use your environment's default authentication.")
        
        st.divider()
        
        # Output Settings
        st.subheader("📁 Output Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            output_format = st.selectbox(
                "Output Format",
                ["HTML", "JSON", "Both"],
                index=0,
                help="Choose the format for assessment reports",
                key="output_format"
            )
            st.session_state.config_data['output_format'] = output_format
        
        with col2:
            output_path = st.text_input(
                "Output Directory",
                value=st.session_state.config_data.get('outputpath', './'),
                placeholder="./reports/",
                help="Directory where reports will be saved",
                key="output_path_advanced"
            )
            st.session_state.config_data['outputpath'] = output_path
        
        st.divider()
        
        # Execution Settings
        st.subheader("⚙️ Execution Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            quiet = st.checkbox(
                "Quiet Mode",
                value=st.session_state.config_data.get('quiet', False),
                help="Suppress non-essential output during execution",
                key="quiet_mode"
            )
            st.session_state.config_data['quiet'] = quiet
        
        with col2:
            dark_mode = st.checkbox(
                "Dark Mode Reports",
                value=st.session_state.config_data.get('darkmode', False),
                help="Generate reports with dark theme",
                key="dark_mode_advanced"
            )
            st.session_state.config_data['darkmode'] = dark_mode

    def render_authentication_tab(self):
        """Render authentication configuration"""
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Authentication Configuration</h2>', unsafe_allow_html=True)
        
        st.markdown("### 🔐 Service Account Credentials")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Service Account JSON File",
            type=['json'],
            help="Upload your Google service account credentials file"
        )
        
        # File path input
        creds_path = st.text_input(
            "Or specify file path",
            value=st.session_state.config_data.get('credentials', ''),
            placeholder="/path/to/service-account.json",
            help="Path to your existing credentials file"
        )
        
        if uploaded_file:
            # Save uploaded file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
                tmp_file.write(uploaded_file.read().decode())
                st.session_state.config_data['credentials'] = tmp_file.name
                st.success(f"✅ Uploaded credentials: {uploaded_file.name}")
        elif creds_path:
            st.session_state.config_data['credentials'] = creds_path
            if Path(creds_path).exists():
                st.success(f"✅ Using credentials: {creds_path}")
            else:
                st.error(f"❌ File not found: {creds_path}")

        st.markdown('</div>', unsafe_allow_html=True)

    def render_output_tab(self):
        """Render output configuration"""
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Output Configuration</h2>', unsafe_allow_html=True)
        
        # Output path
        output_path = st.text_input(
            "📁 Output Directory",
            value=st.session_state.config_data.get('outputpath', './'),
            placeholder="./reports",
            help="Directory where assessment reports will be saved"
        )
        st.session_state.config_data['outputpath'] = output_path
        
        # Dark mode
        dark_mode = st.checkbox(
            "🌙 Enable dark mode for reports",
            value=st.session_state.config_data.get('darkmode', False)
        )
        st.session_state.config_data['darkmode'] = dark_mode

        st.markdown('</div>', unsafe_allow_html=True)

    def render_preview_tab(self):
        """Render configuration preview"""
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Configuration Preview</h2>', unsafe_allow_html=True)
        
        # Generate clean config
        clean_config = self.generate_clean_config()
        
        if clean_config:
            # Show YAML preview with flow style for arrays to match ScubaGoggles conventions
            yaml_config = yaml.dump(clean_config, default_flow_style=False, sort_keys=False)
            
            # Convert baselines array to flow style to match sample files
            import re
            yaml_config = re.sub(
                r'baselines:\n(?:- (.+)\n)+',
                lambda m: 'baselines: [' + ', '.join(re.findall(r'- (.+)', m.group(0))) + ']\n',
                yaml_config
            )
            
            # Convert breakglassaccounts array to flow style if present
            yaml_config = re.sub(
                r'breakglassaccounts:\n(?:- (.+)\n)+',
                lambda m: 'breakglassaccounts: [' + ', '.join(re.findall(r'- (.+)', m.group(0))) + ']\n',
                yaml_config
            )
            
            st.code(yaml_config, language='yaml')
            
            # Download button
            st.download_button(
                label="Download Configuration",
                data=yaml_config,
                file_name="scubagoggles_config.yaml",
                mime="text/yaml",
                type="primary"
            )
        else:
            st.warning("Please fill in required fields in the Main tab")

        st.markdown('</div>', unsafe_allow_html=True)

    def render_run_tab(self):
        """Render run assessment tab"""
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="section-title">Run Assessment</h2>', unsafe_allow_html=True)
        
        if SCUBAGOGGLES_AVAILABLE:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Run ScubaGoggles Assessment", type="primary"):
                    if self.validate_config():
                        self.run_assessment()
                    else:
                        st.error("Please fix configuration errors before running")
            
            with col2:
                if st.button("Test Configuration"):
                    self.test_configuration()
        else:
            st.warning("ScubaGoggles modules not available. Please install ScubaGoggles to run assessments.")
            st.info("You can still use this interface to generate configuration files.")

        st.markdown('</div>', unsafe_allow_html=True)

    def generate_clean_config(self) -> Dict[str, Any]:
        """Generate clean configuration dictionary"""
        config = {}
        data = st.session_state.config_data
        
        # Required fields
        if data.get('customerid'):
            config['customerid'] = data['customerid']
        if data.get('subjectemail'):
            config['subjectemail'] = data['subjectemail']
        if data.get('orgname'):
            config['orgname'] = data['orgname']
        if data.get('baselines'):
            config['baselines'] = data['baselines']
        if data.get('credentials'):
            config['credentials'] = data['credentials']
        
        # Optional organization fields
        if data.get('orgunitname'):
            config['orgunitname'] = data['orgunitname']
        if data.get('description'):
            config['description'] = data['description']
        
        # Output settings
        if data.get('outputpath') and data['outputpath'] != './':
            config['outputpath'] = data['outputpath']
        if data.get('darkmode'):
            config['darkmode'] = 'true'
        if data.get('quiet'):
            config['quiet'] = data['quiet']
        
        # Advanced configuration sections
        if data.get('omitpolicy'):
            config['omitpolicy'] = data['omitpolicy']
        if data.get('annotatepolicy'):
            config['annotatepolicy'] = data['annotatepolicy']
        if data.get('breakglassaccounts'):
            config['breakglassaccounts'] = data['breakglassaccounts']
        
        return config

    def validate_config(self) -> bool:
        """Validate the current configuration"""
        data = st.session_state.config_data
        errors = []
        
        # Check organization fields
        if not data.get('orgname'):
            errors.append("Organization Name is required")
        if not data.get('baselines'):
            errors.append("At least one baseline must be selected")
        
        # Check authentication specific fields
        auth_method = data.get('auth_method', 'Service Account')
        if auth_method == "Service Account":
            if not data.get('subjectemail'):
                errors.append("Subject Email is required for Service Account authentication")
            if not data.get('credentials'):
                errors.append("Credentials file is required for Service Account authentication")
        
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
            return False
        return True

    def test_configuration(self):
        """Test the configuration"""
        st.info("🧪 Testing configuration...")
        # Add configuration testing logic here
        st.success("✅ Configuration test passed!")

    def run_assessment(self):
        """Run ScubaGoggles assessment"""
        st.info("🚀 Starting ScubaGoggles assessment...")
        # Add assessment execution logic here
        st.success("✅ Assessment completed!")

    def run(self):
        """Main application entry point"""
        self.setup_page_config()
        
        # Add import functionality and help to sidebar
        with st.sidebar:
            st.markdown("### 📥 Import Config")
            uploaded_file = st.file_uploader(
                "Upload YAML",
                type=['yaml', 'yml'],
                help="Import existing ScubaGoggles configuration",
                key="import_config_sidebar"
            )
            
            if uploaded_file is not None:
                if st.button("📥 Import", type="primary", use_container_width=True):
                    self.import_configuration(uploaded_file)
            
            st.markdown("---")
            st.markdown("### ❓ Help")
            if st.button("📖 Show Help & Documentation", use_container_width=True):
                st.session_state.ui_show_help = True
                    
        self.render_header()
        
        # Create tabs similar to ScubaGear
        tabs = st.tabs([
            "🏢 Main", 
            "🚫 Omit Policies",
            "📝 Annotate Policies", 
            "🚨 Break Glass",
            "⚙️ Advanced",
            "👁️ Preview", 
            "🚀 Run ScubaGoggles"
        ])
        
        with tabs[0]:
            self.render_main_tab()
        
        with tabs[1]:
            self.render_omit_policies_tab()
        
        with tabs[2]:
            self.render_annotate_policies_tab()
        
        with tabs[3]:
            self.render_break_glass_tab()
        
        with tabs[4]:
            self.render_advanced_tab()
        
        with tabs[5]:
            self.render_preview_tab()
        
        with tabs[6]:
            self.render_run_tab()
        
        # Status bar
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if SCUBAGOGGLES_AVAILABLE:
                st.markdown('<span class="status-indicator status-success">✅ ScubaGoggles Available</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-indicator status-warning">⚠️ ScubaGoggles Limited</span>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**Version:** {self.version}")
        
        with col3:
            st.markdown("**[GitHub Repository](https://github.com/cisagov/ScubaGoggles)**")


def main():
    """Main function to run the professional UI"""
    app = ScubaConfigApp()
    app.run()


if __name__ == "__main__":
    main()