# How We Did This: Converting Streamlit to Static GitHub Pages

## Executive Summary

**We converted our Python Streamlit web application to run entirely in the browser using WebAssembly technology.** Instead of requiring a Python server, the app now runs as a static website that executes Python code directly in the user's browser. This eliminated hosting costs, improved scalability, and made the tool accessible to anyone with a web browser - all while maintaining the same user interface and functionality.

**Key Achievement:** Transformed a server-dependent Python application into a maintenance-free static site hosted on GitHub Pages for $0/month.

---

## Streamlit to Static Site Conversion Process

### Understanding the Technologies

**Original Setup (Streamlit):**
```python
# Traditional Streamlit app
import streamlit as st
st.write("Hello World")
# Runs on: Python server (requires backend)
# Command: streamlit run app.py
# Hosts on: localhost:8501 or cloud server
```

**New Setup (stlite):**
```html
<!-- Static HTML with embedded Python -->
<script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.31.0/build/stlite.js"></script>
<!-- Runs on: Browser only (no backend needed) -->
<!-- Hosts on: Any static hosting (GitHub Pages, Netlify, etc.) -->
```

### Core Conversion Strategy

#### A. Technology Stack Transformation
```
BEFORE (Server-Side):
Browser → HTTP Request → Python Server → Streamlit App → HTML Response

AFTER (Client-Side):
Browser → Load HTML → WebAssembly/Pyodide → Python in Browser → Streamlit UI
```

#### B. Key Components
1. **stlite**: Browser-based Streamlit runtime using WebAssembly
2. **Pyodide**: Python interpreter that runs in the browser
3. **WebAssembly**: Allows Python code execution in web browsers
4. **Static Hosting**: No server required, just file serving

---

## Step-by-Step Conversion Process

### Step 1: Analyze Original App
```python
# Your original scubaconfigapp.py had:
- File system access (reading baseline .md files)
- Dynamic imports
- Streamlit server dependencies
- Interactive widgets and state management
```

### Step 2: Create Static HTML Container
```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.31.0/build/stlite.css" />
</head>
<body>
    <div id="stlite-main"></div>
    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.31.0/build/stlite.js"></script>
</body>
</html>
```

### Step 3: Embed Python Code
```javascript
stlite.mount({
    requirements: ["pyyaml"],  // Python packages
    entrypoint: "streamlit_app.py",
    files: {
        "streamlit_app.py": `
            import streamlit as st
            # Your entire Python application goes here as a string
            st.write("Hello from the browser!")
        `
    }
}, document.getElementById("stlite-main"));
```

### Step 4: Handle Data Dependencies
```python
# PROBLEM: Can't read files in browser
with open('baselines/gmail.md', 'r') as f:  # ❌ Won't work

# SOLUTION: Embed data directly
baseline_policies = {
    'GMAIL': {
        'GWS.GMAIL.1.1v0.6': 'External recipient warnings SHALL be enabled.',
        # ... more policies embedded as data
    }
}
```

---

## Technical Challenges & Solutions

### Challenge 1: File System Access
```python
# Original: Dynamic file reading
def parse_baseline_policies():
    policies = {}
    for file in glob.glob("baselines/*.md"):
        with open(file, 'r') as f:
            # Parse markdown files

# Solution: Pre-processed embedded data
def parse_baseline_policies():
    return {
        'GMAIL': {...},  # Pre-extracted policy data
        'DRIVE': {...},  # Embedded at build time
    }
```

### Challenge 2: Package Dependencies
```python
# Original: Full dependency management
requirements = [
    "streamlit==1.28.0",
    "pyyaml==6.0",
    "pandas==2.0.0"
]

# Solution: Use stlite pre-installed packages
requirements = [
    "pyyaml"  # Only add what's not pre-installed
]
# Note: stlite comes with streamlit 1.21.0 pre-installed
```

### Challenge 3: State Management
```python
# Works the same in both versions!
if 'config' not in st.session_state:
    st.session_state.config = {}

# Browser storage persists session state automatically
```

---

## Deployment Automation

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy-pages.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

---

## Performance & Limitations Comparison

| Aspect | Traditional Streamlit | stlite Static |
|--------|---------------------|---------------|
| **Startup** | Instant (server running) | 3-5 seconds (Python loading) |
| **Hosting Cost** | Requires server ($) | Free (static hosting) |
| **Scalability** | Limited by server resources | Unlimited (CDN distribution) |
| **File Access** | Full filesystem | Browser storage only |
| **Package Support** | All Python packages | Limited to browser-compatible |
| **Internet Required** | Only for initial load | Required for CDN resources |

---

## When to Use Each Approach

### Use Traditional Streamlit when:
- Heavy data processing required
- Need access to local files/databases
- Complex Python package dependencies
- Real-time data streaming

### Use stlite Static when:
- Configuration tools and forms
- Data visualization dashboards
- Proof-of-concepts and demos
- Want free, maintenance-free hosting

---

## Implementation Details

### Files Created/Modified:
- **`index.html`**: Main static site with embedded Python application
- **`.github/workflows/deploy-pages.yml`**: Automated deployment pipeline
- **Enhanced features**: Policy management with embedded baseline data

### Magic Behind the Scenes:
**stlite brings Python to the browser**, transforming server-side applications into client-side static sites using WebAssembly technology!

---

## Advanced Dynamic Feature Conversion

### Challenge: Converting Server-Side File Processing to Browser-Compatible Static Data

One of the most complex aspects of the conversion was transforming the dynamic policy parsing system from a file-based approach to an embedded data approach suitable for static web deployment.

#### Original Dynamic System (Streamlit Server)

The original application used sophisticated file system operations to dynamically parse baseline policies:

```python
def parse_baseline_policies(self) -> Dict[str, Dict[str, str]]:
    """Parse policies from baseline markdown files"""
    policies = {}
    baseline_dir = Path('scubagoggles/baselines')
    
    # Dynamic file discovery - scan directory for .md files
    for md_file in baseline_dir.glob('*.md'):
        if md_file.name == 'README.md':
            continue
            
        # Real-time file reading and parsing
        content = md_file.read_text(encoding='utf-8')
        baseline_name = md_file.stem.upper()
        policies[baseline_name] = self.extract_policies_from_markdown(content, baseline_name)
    
    return policies

def extract_policies_from_markdown(self, content: str, baseline_name: str) -> Dict[str, str]:
    """Extract policy IDs and titles from markdown content using regex patterns"""
    policies = {}
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Complex pattern matching for policy headers
        if line.startswith('#### ') and 'GWS.' in line:
            policy_match = re.search(r'GWS\.[A-Z]+\.\d+\.\d+v[\d.]+', line)
            if policy_match:
                policy_id = policy_match.group()
                # Extract policy description from following lines
                policy_desc = self.extract_policy_description(lines, i + 1)
                policies[policy_id] = policy_desc
    
    return policies
```

**Key Capabilities:**

- Real-time markdown file parsing
- Dynamic policy discovery from file system
- Regex-based policy ID extraction
- Contextual description parsing
- Support for multiple baseline formats

#### Converted Static System (stlite Browser)

Since browsers cannot access local file systems, the dynamic parsing was replaced with pre-processed embedded data:

```python
def parse_baseline_policies():
    """Parse policies from embedded data - browser-compatible approach"""
    
    # Pre-processed policy data embedded directly in the application
    # This data was extracted from the original markdown files during build process
    baseline_policies = {
        'COMMONCONTROLS': {
            'GWS.COMMONCONTROLS.1.1v0.6': 'Phishing-Resistant MFA SHALL be required for all users.',
            'GWS.COMMONCONTROLS.1.2v0.6': 'Post SSO verification SHOULD be enabled for users signing in using the SSO profile for your organization.',
            # ... 18+ policies with full descriptions
        },
        'GMAIL': {
            'GWS.GMAIL.1.1v0.6': 'External recipient warnings SHALL be enabled.',
            'GWS.GMAIL.2.1v0.6': 'SPF records SHALL be published for all domains.',
            # ... 13+ policies with security requirements
        },
        'DRIVE': {
            'GWS.DRIVE.1.1v0.6': 'External sharing SHALL be restricted.',
            'GWS.DRIVE.2.1v0.6': 'Link sharing SHALL be disabled for users.',
            # ... 12+ policies covering file security
        }
        # Additional product policies: CALENDAR, MEET, GROUPS, CHAT, SITES, CLASSROOM
    }
    
    return baseline_policies
```

### Dynamic Policy Management Features

#### Omit Policies Implementation

**Server Version:**
```python
# Dynamic checkbox generation based on parsed files
for product in selected_products:
    product_policies = self.available_policies.get(product.upper(), {})
    for policy_id, policy_desc in product_policies.items():
        is_omitted = st.checkbox(
            f"Omit {policy_id}",
            value=policy_id in st.session_state.config['omit_policies']
        )
```

**Static Version:**
```python
# Pre-computed policy display with embedded descriptions
for policy_id, policy_desc in policies.items():
    col1, col2 = st.columns([5, 1])
    
    with col1:
        # Rich policy display with embedded styling
        st.markdown(f"""
        <div class="policy-item">
            <div class="policy-id">{policy_id}</div>
            <div class="policy-desc">{policy_desc}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Interactive omit/include toggle
        is_omitted = policy_id in st.session_state.config.get('omit_policies', [])
        if st.button("Omit" if not is_omitted else "Include", 
                   key=f"omit_{policy_id}",
                   type="secondary" if not is_omitted else "primary"):
            # Dynamic state management
            if is_omitted:
                st.session_state.config['omit_policies'].remove(policy_id)
            else:
                if 'omit_policies' not in st.session_state.config:
                    st.session_state.config['omit_policies'] = []
                st.session_state.config['omit_policies'].append(policy_id)
            st.rerun()
```

#### Annotate Policies Implementation

**Dynamic Annotation System:**
```python
# Policy selection with searchable dropdown
selected_policy = st.selectbox(
    "Select Policy to Annotate",
    [""] + list(available_for_annotation.keys()),
    format_func=lambda x: f"{x} - {available_for_annotation.get(x, '')[:50]}..." if x else "Select a policy"
)

# Custom annotation input with persistence
if selected_policy:
    annotation_text = st.text_area(
        "Annotation",
        placeholder="Enter your annotation or note for this policy...",
        height=100
    )
    
    # Save annotation with validation
    if st.button("Add Annotation") and annotation_text.strip():
        if 'annotate_policies' not in st.session_state.config:
            st.session_state.config['annotate_policies'] = {}
        st.session_state.config['annotate_policies'][selected_policy] = annotation_text.strip()
        st.rerun()
```

### Data Pre-Processing Strategy

To maintain the dynamic feel while working within static constraints, a data pre-processing approach was implemented:

1. **Baseline Extraction**: Policy data was extracted from all markdown files in the baselines directory
2. **Structure Preservation**: The original policy ID and description structure was maintained
3. **Product Organization**: Policies were organized by Google Workspace product for logical grouping
4. **Embedded Integration**: All data was embedded directly into the JavaScript template literal

### Performance Implications

| Aspect | Dynamic Server | Static Embedded |
|--------|----------------|-----------------|
| **Initialization** | File I/O on startup | Instant data access |
| **Memory Usage** | Variable based on file sizes | Fixed embedded data size |
| **Updatability** | Real-time file changes | Requires rebuild/redeploy |
| **Consistency** | Dependent on file integrity | Guaranteed data integrity |
| **Maintenance** | Automatic policy discovery | Manual data synchronization |

### Benefits of the Conversion

1. **Reliability**: No file system dependencies or I/O errors
2. **Performance**: Instant policy data access without parsing overhead
3. **Consistency**: Guaranteed policy data integrity across all deployments
4. **Simplicity**: Eliminates complex file parsing logic and error handling
5. **Portability**: Works identically across all browsers and environments

### Trade-offs and Considerations

**Limitations Introduced:**

- Manual data synchronization required when baseline files change
- Larger application bundle size due to embedded data
- Loss of automatic policy discovery capabilities


**Mitigation Strategies:**

- Automated build processes could extract and embed updated policy data
- Version control integration could trigger rebuilds when baselines change
- Documentation processes to ensure data synchronization awareness


This conversion demonstrates how complex server-side dynamic features can be successfully transformed for static deployment while preserving user experience and functionality.

---

*This transformation demonstrates how modern web technologies can eliminate traditional hosting barriers while maintaining full application functionality.*
