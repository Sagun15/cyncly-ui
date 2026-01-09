import streamlit as st
import requests
import json
import time
import os
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Auto Design",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    .stButton>button:disabled,
    .stButton>button[disabled],
    button[disabled] {
        opacity: 0.6 !important;
        cursor: not-allowed !important;
        background: linear-gradient(90deg, #9ca3af 0%, #6b7280 100%) !important;
        transform: none !important;
        box-shadow: none !important;
        pointer-events: none !important;
    }
    .stButton>button:disabled:hover,
    .stButton>button[disabled]:hover,
    button[disabled]:hover {
        transform: none !important;
        box-shadow: none !important;
        cursor: not-allowed !important;
        opacity: 0.6 !important;
    }
    /* Target the button container when disabled */
    .stButton:has(button[disabled]) {
        cursor: not-allowed !important;
    }
    .stButton:has(button[disabled]) > button {
        cursor: not-allowed !important;
    }
    .success-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin-top: 1rem;
    }
    .error-message {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin-top: 1rem;
    }
    /* Multiselect ellipsis styling for selected values */
    div[data-baseweb="select"] {
        max-width: 100%;
    }
    div[data-baseweb="select"] > div {
        max-width: 100%;
        overflow: hidden;
    }
    div[data-baseweb="select"] div[role="combobox"] {
        max-width: 100%;
        overflow: hidden;
    }
    div[data-baseweb="select"] div[role="combobox"] > div {
        max-width: 100%;
        overflow: hidden;
    }
    /* Selected tags container */
    div[data-baseweb="select"] div[role="combobox"] > div > div {
        max-width: 100%;
        overflow: hidden;
        display: flex;
        flex-wrap: wrap;
    }
    /* Individual selected tag */
    div[data-baseweb="select"] span[data-baseweb="tag"] {
        max-width: 150px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    /* Selected text when collapsed */
    div[data-baseweb="select"] div[role="combobox"] > div > div:first-child {
        max-width: 100%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    /* Loading animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    .progress-container {
        text-align: center;
        padding: 3rem 2rem;
    }
    .progress-text {
        font-size: 1.5rem;
        font-weight: 600;
        color: #667eea;
        margin-top: 1rem;
    }
    .progress-subtext {
        font-size: 1rem;
        color: #718096;
        margin-top: 0.5rem;
    }
    /* Layout type selection buttons */
    .layout-button-container {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin: 1rem 0;
    }
    .layout-button {
        flex: 1;
        padding: 2rem 1rem;
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        cursor: pointer;
        text-align: center;
        transition: all 0.3s ease;
        font-size: 3rem;
        color: #2d3748;
    }
    .layout-button:hover {
        border-color: #667eea;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    .layout-button.selected {
        border-color: #667eea;
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .layout-button-label {
        font-size: 1rem;
        font-weight: 600;
        color: #2d3748;
        margin-top: 0.5rem;
    }
    .layout-button.selected .layout-button-label {
        color: #667eea;
    }
    /* Layout button - completely hide the Streamlit button and its container */
    div[data-testid="column"]:has(button[key="layout_l"]) {
        position: relative;
    }
    /* Hide the button wrapper/container */
    div:has(button[key="layout_l"]) {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    button[key="layout_l"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        opacity: 0 !important;
        z-index: 10 !important;
        cursor: pointer !important;
        min-height: 120px !important;
        box-shadow: none !important;
    }
    /* Ensure button container doesn't show any gradient or background */
    .stButton:has(button[key="layout_l"]),
    div:has(button[key="layout_l"]),
    div:has(button[key="layout_l"]) > div,
    div:has(button[key="layout_l"]) > div > div,
    .layout-card-wrapper,
    .layout-card-wrapper > * {
        background: transparent !important;
        background-image: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }
    /* Specifically target the column containing the layout button */
    div[data-testid="column"]:has(button[key="layout_l"]) {
        overflow: hidden !important;
    }
    div[data-testid="column"]:has(button[key="layout_l"]) > div {
        overflow: hidden !important;
        background: transparent !important;
        background-image: none !important;
    }
    /* Hide any gradient specifically from button and all its parents */
    button[key="layout_l"],
    button[key="layout_l"]::before,
    button[key="layout_l"]::after,
    .stButton:has(button[key="layout_l"])::before,
    .stButton:has(button[key="layout_l"])::after {
        background: transparent !important;
        background-image: none !important;
    }
    button[key="layout_l"]:hover,
    button[key="layout_l"]:focus,
    button[key="layout_l"]:active {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        opacity: 0 !important;
    }
    /* Hide any gradient or background from button parent */
    .stButton:has(button[key="layout_l"]) {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# API endpoint
API_ENDPOINT = "https://ai-auto-design-api-service.azurewebsites.net/api/v1/ai-auto-design"
API_BASE_URL = "https://ai-auto-design-api-service.azurewebsites.net"

# Get bearer token from Streamlit secrets or environment variable
# For local development, create .streamlit/secrets.toml with: BEARER_TOKEN = "your_token"
# For Streamlit Cloud, add it in Settings > Secrets
try:
    BEARER_TOKEN = st.secrets["BEARER_TOKEN"]
except (KeyError, AttributeError):
    BEARER_TOKEN = os.getenv("BEARER_TOKEN", "")
    
if not BEARER_TOKEN:
    st.error("⚠️ BEARER_TOKEN not found! Please set it in Streamlit secrets or as an environment variable.")
    st.stop()

def build_request_body(
    appliances: List[str],
    cabinet_types: List[str],
    worktop_material: str,
    plumbing_fixtures: List[str],
    layout_type: str = "L-Shaped",
    width: int = 4000,
    depth: int = 4000
) -> Dict[str, Any]:
    """Build the request body with user selections."""
    
    # Base request body structure
    request_body = {
        "sourceDesign": {
            "info": {
                "name": "Sample Design v1.2",
                "formatVersion": "1.2.0",
                "source": {
                    "applicationId": "TestHub",
                    "applicationVersion": "1.5.17"
                },
                "coordinateConventions": {
                    "baseMeasurementUnit": "mm",
                    "axisOrientation": "rightHanded",
                    "axisElevation": "zAxisUp"
                }
            },
            "spaces": [
                {
                    "id": "1532d48e-73b8-4b79-8eea-6159db89350d",
                    "name": "Kitchen Space",
                    "functions": ["kitchen"],
                    "walls": {
                        "perimeterWalls": [
                            {
                                "id": "south_wall",
                                "type": "solidWall",
                                "name": "South Wall",
                                "startPosition": [0, 0],
                                "thickness": 150,
                                "outdoorPerimeter": True,
                                "startHeight": 3200,
                                "endHeight": 3200
                            },
                            {
                                "id": "east_wall",
                                "type": "solidWall",
                                "name": "East Wall",
                                "startPosition": [width, 0],
                                "thickness": 150,
                                "outdoorPerimeter": False,
                                "startHeight": 3200,
                                "endHeight": 3200
                            },
                            {
                                "id": "north_wall",
                                "type": "solidWall",
                                "name": "North Wall",
                                "startPosition": [width, depth],
                                "thickness": 150,
                                "outdoorPerimeter": False,
                                "startHeight": 3200,
                                "endHeight": 3200
                            },
                            {
                                "id": "west_wall",
                                "type": "solidWall",
                                "name": "West Wall",
                                "startPosition": [0, depth],
                                "thickness": 150,
                                "outdoorPerimeter": False,
                                "startHeight": 3200,
                                "endHeight": 3200
                            }
                        ]
                    },
                    "floor": {"id": "0f51b8fb-e147-4a80-91ba-0047d881c7cf"},
                    "ceiling": {"id": "c58c9ce1-cb93-48da-9d1d-aae3efb0ec12"}
                }
            ]
        },
        "autoDesignInputs": {
            "roomConfig": {
                "functionLayoutType": layout_type,
                "functionStyle": "modern"
            },
            "requiredItemTypes": []
        }
    }
    
    # Build preferences for appliances
    appliance_preferences = []
    for appliance in appliances:
        appliance_preferences.append({"baseItemType": f"appliance.{appliance}"})
    
    if appliance_preferences:
        request_body["autoDesignInputs"]["requiredItemTypes"].append({
            "catalogVersionIDs": [6958, 8347],
            "preferences": appliance_preferences
        })
    
    # Build preferences for plumbing fixtures
    plumbing_preferences = []
    for fixture in plumbing_fixtures:
        plumbing_preferences.append({"baseItemType": f"plumbingFixture.{fixture}"})
    
    if plumbing_preferences:
        request_body["autoDesignInputs"]["requiredItemTypes"].append({
            "catalogVersionIDs": [6958],
            "preferences": plumbing_preferences
        })
    
    # Build preferences for cabinets
    cabinet_preferences = []
    for cabinet_type in cabinet_types:
        cabinet_preferences.append({
            "baseItemType": "cabinetry.cabinet",
            "subType": cabinet_type
        })
    
    if cabinet_preferences:
        request_body["autoDesignInputs"]["requiredItemTypes"].append({
            "catalogVersionIDs": [8204],
            "preferences": cabinet_preferences
        })
    
    # Build preferences for worktop
    if worktop_material:
        request_body["autoDesignInputs"]["requiredItemTypes"].append({
            "catalogVersionIDs": [8204],
            "preferences": [
                {"baseItemType": "worktop.slab", "material": worktop_material.lower()}
            ]
        })
    
    return request_body

def send_request(request_body: Dict[str, Any]) -> Tuple[bool, Any, Optional[str]]:
    """Send POST request to the API. Returns (success, result, location_header)."""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }
        response = requests.post(
            API_ENDPOINT,
            json=request_body,
            headers=headers,
            timeout=30
        )
        
        # Handle 202 Accepted status
        if response.status_code == 202:
            location = response.headers.get("location", "")
            result = response.json() if response.content else {}
            return True, result, location
        
        response.raise_for_status()
        result = response.json() if response.content else {"message": "Success"}
        return True, result, None
    except requests.exceptions.RequestException as e:
        return False, str(e), None

def poll_status(location_path: str) -> Tuple[bool, Dict[str, Any]]:
    """Poll the status endpoint using the location path. Returns (success, result)."""
    try:
        # Handle both relative paths (starting with /) and absolute URLs
        if location_path.startswith("http://") or location_path.startswith("https://"):
            url = location_path
        else:
            # Relative path - append to base URL
            url = f"{API_BASE_URL}{location_path}"
        
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json() if response.content else {}
        return True, result
    except requests.exceptions.RequestException as e:
        return False, {"error": str(e)}

# Initialize session state
if "polling_active" not in st.session_state:
    st.session_state.polling_active = False
if "location_path" not in st.session_state:
    st.session_state.location_path = None
if "request_id" not in st.session_state:
    st.session_state.request_id = None
if "last_poll_time" not in st.session_state:
    st.session_state.last_poll_time = None
if "poll_interval" not in st.session_state:
    st.session_state.poll_interval = 10  # 10 seconds
if "request_in_progress" not in st.session_state:
    st.session_state.request_in_progress = False
if "pending_request" not in st.session_state:
    st.session_state.pending_request = None
if "last_request_result" not in st.session_state:
    st.session_state.last_request_result = None
if "showing_result" not in st.session_state:
    st.session_state.showing_result = False

# Clear previous request result if a new request is in progress or pending
# This prevents old buttons from showing when a new request starts
if st.session_state.request_in_progress or st.session_state.pending_request:
    st.session_state.last_request_result = None

# Check query parameters to see if we're in progress view
query_params = st.query_params
is_progress_view = False
request_id_from_url = None

# Check if progress parameter exists
if "progress" in query_params:
    progress_value = query_params.get("progress")
    if isinstance(progress_value, list):
        is_progress_view = progress_value[0] == "true" if progress_value else False
    else:
        is_progress_view = progress_value == "true"

# Get request_id from URL
if "request_id" in query_params:
    request_id_value = query_params.get("request_id")
    if isinstance(request_id_value, list):
        request_id_from_url = request_id_value[0] if request_id_value else None
    else:
        request_id_from_url = request_id_value

# If we're in progress view, set up polling state
if is_progress_view and request_id_from_url:
    # Reconstruct location_path from request_id
    if not st.session_state.location_path:
        st.session_state.location_path = f"/api/v1/ai-auto-design-result?request_id={request_id_from_url}"
    if not st.session_state.polling_active:
        st.session_state.polling_active = True
    if st.session_state.last_poll_time is None:
        st.session_state.last_poll_time = 0  # Reset to trigger immediate poll

# Check if we should show progress page (separate view)
# Show progress view if progress=true in URL, even if location_path needs to be set
if is_progress_view:
    # Ensure location_path is set from request_id if not already set
    if not st.session_state.location_path and request_id_from_url:
        st.session_state.location_path = f"/api/v1/ai-auto-design-result?request_id={request_id_from_url}"
    
    # Only show progress if we have a location_path
    if st.session_state.location_path:
        # Progress page - dedicated view for polling
        st.markdown('<h1 class="main-header">🏠 AI Auto Design</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Loading animation and status
        st.markdown("""
            <div class="progress-container">
                <div class="spinner"></div>
                <div class="progress-text">In Progress</div>
                <div class="progress-subtext">Your design is being generated. Please wait...</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Simple polling - check if we should poll now
        current_time = time.time()
        should_poll = False
        
        # Initialize last_poll_time if needed
        if st.session_state.last_poll_time is None:
            st.session_state.last_poll_time = 0
        
        # Check if it's time to poll (first time or after interval)
        if st.session_state.last_poll_time == 0:
            should_poll = True
        else:
            time_since_last_poll = current_time - st.session_state.last_poll_time
            if time_since_last_poll >= st.session_state.poll_interval:
                should_poll = True
        
        if should_poll:
            with st.spinner("🔄 Checking status..."):
                success, result = poll_status(st.session_state.location_path)
                st.session_state.last_poll_time = current_time
                
                if success:
                    # Check if codeMajor is still processing
                    code_major = result.get("codeMajor", "unknown")
                    
                    if code_major != "processing":
                        # Status changed, stop polling and show result
                        st.session_state.polling_active = False
                        st.session_state.status_result = result
                        st.session_state.status = code_major
                        # Clear query params to show result on main page
                        st.query_params.clear()
                        st.rerun()
                    else:
                        # Still processing, show status
                        st.info(f"🔄 Status: {code_major}. It'll take about 3 minutes to generate your layout. ")
                else:
                    st.error(f"❌ Error polling status: {result.get('error', 'Unknown error')}")
                    # Stop polling on error
                    st.session_state.polling_active = False
        
        # If still polling, wait and rerun after interval
        if st.session_state.polling_active:
            # Calculate time remaining
            if st.session_state.last_poll_time and st.session_state.last_poll_time > 0:
                time_elapsed = time.time() - st.session_state.last_poll_time
                time_remaining = max(0, st.session_state.poll_interval - time_elapsed)
            else:
                time_remaining = st.session_state.poll_interval
            
            if time_remaining > 0:

                # Wait for the full remaining time before next poll
                time.sleep(time_remaining)
                st.rerun()
            else:
                # Time to poll again immediately
                st.rerun()
        
        # Add a button to go back to main page
        st.markdown("---")
        if st.button("← Back to Main Page", key="back_to_main"):
            # Clear query parameters to go back to main page
            st.query_params.clear()
            st.session_state.polling_active = False
            st.rerun()
        
        # Stop here - don't show main form when in progress view
        st.stop()

# Main page - only shown when not polling
else:
    # Check if we just finished polling and show result
    if "status_result" in st.session_state and "status" in st.session_state:
        code_major = st.session_state.status
        full_response = st.session_state.status_result
        
        # Only show if codeMajor is not "processing" (polling has stopped)
        if code_major != "processing":
            # Set flag to indicate we're showing a result
            st.session_state.showing_result = True
            
            # If codeMajor is "success", show the result object
            if code_major == "success":
                st.success(f"✅ Kitchen Design Generated Successfully!")
                result_object = full_response.get("result", {})
                
                # Instructions section for viewing results in SFx Tool
                st.info("""
                📖 **How to View Your Design in SFx Tool**
                
                Follow these steps to view your generated design:
                
                **Step 1:** Open the SFx Tool
                - Click here: [**SFx Tool**](https://planner.cyncly-idealspaces.com/us/design/Draft?partnership=isdemositena)
                
                **Step 2:** Open the Browser Console
                You can open the console using one of these methods:
                
                **For Windows:**
                - Press `F12` key, OR
                - Press `Ctrl + Shift + J` (Chrome/Edge), OR
                - Press `Ctrl + Shift + K` (Firefox), OR
                - Right-click anywhere on the page → Select **"Inspect"** → Click the **"Console"** tab
                
                **For Mac:**
                - Press `Cmd + Option + J` (Chrome/Edge), OR
                - Press `Cmd + Option + K` (Firefox), OR
                - Right-click anywhere on the page → Select **"Inspect"** → Click the **"Console"** tab
                
                **Step 3:** Copy the command below and paste it in the console
                """)
                
                # Generate the command with the result object
                # Format the result object as a JavaScript object literal (JSON is valid JavaScript)
                result_object_js = json.dumps(result_object)
                command = f'commands.environment.loadCDFModel(JSON.stringify({result_object_js}))'
                
                st.code(command, language="javascript")
                
                st.info("""
                **Step 4:** Execute the command
                - After pasting the command in the console, press `Enter`
                - Your design will be loaded and displayed in the SFx Tool
                
                **Note:** Make sure you've copied the entire command including the `commands.environment.loadCDFModel(JSON.stringify(...))` part with the result object.
                """)
                
                st.markdown("---")
                
                with st.expander("📋 View Result", expanded=True):
                    st.json(result_object)
            else:
                # For other statuses, show the full response
                st.markdown("### Final Response:")
                st.json(full_response)
            
            # Add "Start New Design" button after showing result
            st.markdown("---")
            if st.button("🔄 Start New Design", type="primary", use_container_width=True, key="start_new_design"):
                # Clear result state and set showing_result to False, then rerun - form will appear
                st.session_state.showing_result = False
                if "status_result" in st.session_state:
                    del st.session_state.status_result
                if "status" in st.session_state:
                    del st.session_state.status
                st.query_params.clear()
                st.rerun()
    
    # Main UI - only show if not displaying a result
    if not st.session_state.showing_result:
        st.markdown('<h1 class="main-header">🏠 AI Auto Design</h1>', unsafe_allow_html=True)
        st.markdown("---")

        # Sidebar for additional info
        with st.sidebar:
            st.header("ℹ️ About")
            st.markdown("""
            This application allows you to design your kitchen space by selecting:
            - **Appliances**: Choose from various kitchen appliances
            - **Plumbing Fixtures**: Select plumbing fixtures like sinks
            - **Cabinets**: Select cabinet types (wall/base/tall)
            - **Worktops**: Pick your preferred worktop material
            
            Click **Build** to generate your design!
            """)
            st.markdown("---")
            st.markdown("**API Endpoint:**")
            st.code(API_ENDPOINT, language=None)

        # Layout Type Selection - Clean and simple design
        st.markdown('<div class="section-header">📐 Layout Type</div>', unsafe_allow_html=True)
        
        # Initialize layout type in session state
        if "selected_layout_type" not in st.session_state:
            st.session_state.selected_layout_type = "L-Shaped"

        # Simple visual cards with clickable buttons
        layout_col1, layout_col2, layout_col3 = st.columns([1, 1, 1])

        with layout_col1:
            is_selected = st.session_state.selected_layout_type == "L-Shaped"
            border_color = "#667eea" if is_selected else "#e2e8f0"
            bg_color = "rgba(102, 126, 234, 0.1)" if is_selected else "white"
            text_color = "#667eea" if is_selected else "#2d3748"
            border_width = "3px" if is_selected else "2px"
            
            st.markdown(f"""
            <div style="padding: 2rem 1rem; text-align: center; border: {border_width} solid {border_color}; border-radius: 10px; background: {bg_color}; margin-bottom: 0.5rem; height: 150px; display: flex; flex-direction: column; justify-content: center; align-items: center; box-sizing: border-box;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem; font-weight: bold; color: {text_color};">L</div>
                <div style="font-size: 1rem; font-weight: 600; color: {text_color};">L-Shaped</div>
                <div style="font-size: 0.75rem; color: transparent; margin-top: 0.5rem; height: 1.2em;">Placeholder</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("✓ Select", key="layout_l", use_container_width=True, type="primary" if is_selected else "secondary"):
                st.session_state.selected_layout_type = "L-Shaped"
                st.rerun()

        with layout_col2:
            st.markdown("""
            <div style="padding: 2rem 1rem; text-align: center; border: 2px solid #e2e8f0; border-radius: 10px; background: #f7fafc; margin-bottom: 0.5rem; opacity: 0.6; height: 150px; display: flex; flex-direction: column; justify-content: center; align-items: center; box-sizing: border-box;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem; font-weight: bold; color: #a0aec0;">U</div>
                <div style="font-size: 1rem; font-weight: 600; color: #a0aec0;">U-Shaped</div>
                <div style="font-size: 0.75rem; color: #a0aec0; margin-top: 0.5rem;">Coming Soon</div>
            </div>
            """, unsafe_allow_html=True)
            st.button("Select", key="layout_u", use_container_width=True, disabled=True)

        with layout_col3:
            st.markdown("""
            <div style="padding: 2rem 1rem; text-align: center; border: 2px solid #e2e8f0; border-radius: 10px; background: #f7fafc; margin-bottom: 0.5rem; opacity: 0.6; height: 150px; display: flex; flex-direction: column; justify-content: center; align-items: center; box-sizing: border-box;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem; font-weight: bold; color: #a0aec0;">I</div>
                <div style="font-size: 1rem; font-weight: 600; color: #a0aec0;">I-Shaped</div>
                <div style="font-size: 0.75rem; color: #a0aec0; margin-top: 0.5rem;">Coming Soon</div>
            </div>
            """, unsafe_allow_html=True)
            st.button("Select", key="layout_i", use_container_width=True, disabled=True)

        st.markdown("---")

        # Room Dimensions Section
        st.markdown('<div class="section-header">📏 Room Dimensions</div>', unsafe_allow_html=True)
        dim_col1, dim_col2 = st.columns([1, 1])
        
        with dim_col1:
            width = st.number_input(
                "Width (mm):",
                min_value=3500,
                max_value=6000,
                value=4000,
                step=100,
                help="Width of the room (3500-6000 mm)"
            )
        
        with dim_col2:
            depth = st.number_input(
                "Depth (mm):",
                min_value=3500,
                max_value=6000,
                value=4000,
                step=100,
                help="Depth of the room (3500-6000 mm)"
            )

        st.markdown("---")

        # Main content area
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown('<div class="section-header">🔌 Appliances</div>', unsafe_allow_html=True)
            st.markdown("Select the appliances you want in your kitchen:")
            
            appliance_options = {
                "Cooktop": "cooktop",
                "Refrigerator": "refrigerator",
                "Oven": "oven",
                "Range": "range",
                "Dishwasher": "dishwasher"
            }
            
            selected_appliance_labels = st.multiselect(
                "Choose appliances:",
                options=list(appliance_options.keys()),
                default=["Cooktop", "Refrigerator", "Dishwasher"],
                label_visibility="collapsed"
            )
            
            selected_appliances = [appliance_options[label] for label in selected_appliance_labels]

        with col2:
            st.markdown('<div class="section-header">🚰 Plumbing Fixtures</div>', unsafe_allow_html=True)
            st.markdown("Select plumbing fixtures:")
            
            plumbing_options = {
                "Sink": "sink"
            }
            
            selected_plumbing_labels = st.multiselect(
                "Choose plumbing fixtures:",
                options=list(plumbing_options.keys()),
                default=["Sink"],
                label_visibility="collapsed"
            )
            
            selected_plumbing_fixtures = [plumbing_options[label] for label in selected_plumbing_labels]

        # Cabinets and Worktop section
        col3, col4 = st.columns([1, 1])

        with col3:
            st.markdown('<div class="section-header">🗄️ Cabinets</div>', unsafe_allow_html=True)
            st.markdown("Select cabinet types:")
            
            cabinet_options = {
                "Wall Cabinet": "roof",
                "Base Cabinet": "base",
                "Tall Cabinet": "tall"
            }
            
            selected_cabinet_labels = st.multiselect(
                "Choose cabinet types:",
                options=list(cabinet_options.keys()),
                default=["Wall Cabinet", "Base Cabinet", "Tall Cabinet"],
                label_visibility="collapsed"
            )
            
            selected_cabinets = [cabinet_options[label] for label in selected_cabinet_labels]

        with col4:
            # Worktop selection
            st.markdown('<div class="section-header">🪨 Worktop Material</div>', unsafe_allow_html=True)
            st.markdown("Choose your worktop material:")
            worktop_material = st.selectbox(
                "Choose your worktop material:",
                ["Granite"],
                index=0,
                label_visibility="collapsed"
            )

        # Build button - hide during request, show otherwise
        st.markdown("---")
        if not st.session_state.request_in_progress:
            build_button = st.button(
                "🚀 Build Design", 
                type="primary", 
                use_container_width=True,
                key="build_design_button"
            )
            # Clear previous request result immediately if button was clicked
            # This prevents old buttons from showing before rerun
            if build_button and st.session_state.last_request_result:
                st.session_state.last_request_result = None
        else:
            # Show a message instead of the button when request is in progress
            st.info("🔄 Preparing your personalized layout...")
            build_button = False

        # Redisplay last request result if available (after rerun)
        # CRITICAL: Only show if NO request is in progress and NO pending request exists
        # This prevents old buttons from showing when a new request starts
        
        # If a request is in progress, explicitly remove any previous button HTML using JavaScript
        if st.session_state.request_in_progress or st.session_state.pending_request:
            # Use JavaScript to explicitly remove any previous progress button divs
            st.markdown("""
            <script>
            (function() {
                function removeProgressButtons() {
                    // Remove any progress button containers by ID
                    const buttons = document.querySelectorAll('[id^="progress_button_"]');
                    buttons.forEach(btn => {
                        if (btn && btn.parentNode) {
                            btn.parentNode.removeChild(btn);
                        }
                    });
                    // Also remove by content matching (fallback)
                    const allDivs = document.querySelectorAll('div');
                    allDivs.forEach(div => {
                        if (div.innerHTML && div.innerHTML.includes('Open Progress Page') && 
                            div.innerHTML.includes('Click below to open the progress page')) {
                            const bgColor = window.getComputedStyle(div).backgroundColor;
                            if (bgColor === 'rgb(30, 58, 95)' || bgColor === '#1e3a5f' || 
                                div.style.backgroundColor === 'rgb(30, 58, 95)' || 
                                div.style.backgroundColor === '#1e3a5f') {
                                if (div.parentNode) {
                                    div.parentNode.removeChild(div);
                                }
                            }
                        }
                    });
                }
                // Run immediately
                removeProgressButtons();
                // Also run after a short delay to catch any late-rendered elements
                setTimeout(removeProgressButtons, 100);
                setTimeout(removeProgressButtons, 500);
            })();
            </script>
            """, unsafe_allow_html=True)
        elif st.session_state.last_request_result is not None:
            result_data = st.session_state.last_request_result
            if result_data["type"] == "success":
                if "request_id" in result_data and result_data["request_id"]:
                    request_id = result_data["request_id"]
                    progress_url = f"?progress=true&request_id={request_id}" if request_id else "?progress=true"
                    
                    st.success(f"✅ Request submitted successfully! **Request ID:** `{request_id}`")
                    
                    st.info(f"""
                    📋 **Important: Please save your Request ID**
                    
                    **Your Request ID:** `{request_id}`
                    
                    Please **keep this Request ID** with you. In the future, if you want to view your generated design, you can:
                    
                    1. Open this application (use the same URL you're using now)
                    2. Add `?progress=true&request_id={request_id}` to the end of the URL
                    3. The application will automatically load and display your design
                    
                    **Example:** If your current URL is `https://cyncly-ui-vxunrzzf8qbqb2ltgmsio4.streamlit.app`, you would use:
                    `https://cyncly-ui-vxunrzzf8qbqb2ltgmsio4.streamlit.app?progress=true&request_id={request_id}`
                    """)
                    
                    # Only show button if absolutely no request is in progress
                    # Final check to ensure we're not processing anything
                    # Use a unique ID based on request_id so Streamlit can track it
                    button_id = f"progress_button_{request_id}"
                    if (not st.session_state.request_in_progress and 
                        not st.session_state.pending_request and 
                        st.session_state.last_request_result is not None):
                        st.markdown(f"""
                        <div id="{button_id}" style="margin-top: 1rem; padding: 1.5rem; background-color: #1e3a5f; border-radius: 10px; border: 1px solid #667eea;">
                            <p style="color: #a0aec0; margin-bottom: 1rem; font-size: 1rem;">Click below to open the progress page in a new tab:</p>
                            <a href="{progress_url}" target="_blank" style="
                                display: inline-block;
                                padding: 0.75rem 2rem;
                                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                                color: white;
                                text-decoration: none;
                                border-radius: 10px;
                                font-weight: 600;
                                cursor: pointer;
                            ">🚀 Open Progress Page</a>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Explicitly render empty div to clear any previous button
                        st.markdown(f'<div id="{button_id}" style="display: none;"></div>', unsafe_allow_html=True)
                elif "result" in result_data:
                    st.success("✅ Design built successfully!")
                    st.markdown("### Response:")
                    st.json(result_data["result"])
            elif result_data["type"] == "error":
                st.error(f"❌ Error: {result_data.get('error', 'Unknown error')}")
            
            # Clear the stored result after displaying (optional - comment out if you want it to persist)
            # st.session_state.last_request_result = None

        # Handle button click - store request data and set flag
        if build_button:
            if not selected_appliances:
                st.error("⚠️ Please select at least one appliance.")
            elif not selected_plumbing_fixtures:
                st.error("⚠️ Please select at least one plumbing fixture.")
            elif not selected_cabinets:
                st.error("⚠️ Please select at least one cabinet type.")
            else:
                # Store request data and set flag, then rerun to hide button immediately
                st.session_state.request_in_progress = True
                st.session_state.last_request_result = None  # Clear previous request result to hide old buttons
                st.session_state.last_request_id = None
                st.session_state.pending_request = {
                    "appliances": selected_appliances,
                    "cabinets": selected_cabinets,
                    "worktop": worktop_material,
                    "plumbing": selected_plumbing_fixtures,
                    "layout": st.session_state.selected_layout_type,
                    "width": width,
                    "depth": depth
                }
                st.rerun()

# Process the pending request (runs after rerun when button is hidden)
if st.session_state.pending_request:
    req_data = st.session_state.pending_request
    
    with st.spinner("🔄 Building your design... This may take a moment."):
        request_body = build_request_body(
            req_data["appliances"],
            req_data["cabinets"],
            req_data["worktop"],
            req_data["plumbing"],
            req_data["layout"],
            req_data.get("width", 4000),
            req_data.get("depth", 4000)
        )
        
        # Show request preview (optional, can be collapsed)
        with st.expander("📋 View Request Body"):
            st.json(request_body)
        
        success, result, location = send_request(request_body)
    
    if success:
        # Check if we got a 202 response with location header
        if location:
            # Extract request_id from location
            request_id = None
            if "request_id=" in location:
                request_id = location.split("request_id=")[1].split("&")[0]
                st.session_state.request_id = request_id
            
            # Store location_path in session state
            st.session_state.location_path = location
            
            # Store result for redisplay after rerun
            st.session_state.last_request_result = {
                "type": "success",
                "request_id": request_id,
                "location": location
            }
            
            # Create progress URL with query parameters
            progress_url = f"?progress=true&request_id={request_id}" if request_id else "?progress=true"
            
            # Success message with requestId
            if request_id:
                st.success(f"✅ Request submitted successfully! **Request ID:** `{request_id}`")
                
                # Important info section for stakeholders
                st.info(f"""
                📋 **Important: Please save your Request ID**
                
                **Your Request ID:** `{request_id}`
                
                Please **keep this Request ID** with you. In the future, if you want to view your generated design, you can:
                
                1. Open this application (use the same URL you're using now)
                2. Add `?progress=true&request_id={request_id}` to the end of the URL
                3. The application will give you a command to visualize your design in SFx Tool
                
                **Example:** If your current URL is `https://cyncly-ui-3mutwu6qv5tpk55tdjsd3r.streamlit.app/`, you would use:
                `https://cyncly-ui-3mutwu6qv5tpk55tdjsd3r.streamlit.app/?progress=true&request_id={request_id}`
                """)
                
                # Note: The "Open Progress Page" button is shown in the "Redisplay" section
                # after rerun, not here, to avoid duplicate buttons
            else:
                st.success("✅ Request submitted successfully!")
            
        else:
            # Regular success response
            st.session_state.last_request_result = {
                "type": "success",
                "result": result
            }
            st.success("✅ Design built successfully!")
            st.markdown("### Response:")
            st.json(result)
    else:
        st.session_state.last_request_result = {
            "type": "error",
            "error": result
        }
        st.error(f"❌ Error: {result}")
    
    # Clear pending request and re-enable button after request completes (success or error)
    st.session_state.pending_request = None
    st.session_state.request_in_progress = False
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #718096; padding: 2rem;'>"
    "Built with ❤️ using Streamlit<br><br>"
    "<span style='font-size: 0.9rem;'>"
    "Need help? Contact the developer: "
    "<a href='mailto:sagun.sangwan@kickdrumtech.com' style='color: #667eea; text-decoration: none;'>"
    "sagun.sangwan@kickdrumtech.com"
    "</a>"
    "</span>"
    "</div>",
    unsafe_allow_html=True
)
