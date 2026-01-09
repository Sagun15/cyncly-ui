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
    plumbing_fixtures: List[str]
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
                                "startPosition": [4000, 0],
                                "thickness": 150,
                                "outdoorPerimeter": False,
                                "startHeight": 3200,
                                "endHeight": 3200
                            },
                            {
                                "id": "north_wall",
                                "type": "solidWall",
                                "name": "North Wall",
                                "startPosition": [4000, 4000],
                                "thickness": 150,
                                "outdoorPerimeter": False,
                                "startHeight": 3200,
                                "endHeight": 3200
                            },
                            {
                                "id": "west_wall",
                                "type": "solidWall",
                                "name": "West Wall",
                                "startPosition": [0, 4000],
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
                "functionLayoutType": "L-Shaped",
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
                        st.info(f"🔄 Status: {code_major}. Next check in {st.session_state.poll_interval} seconds...")
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
                st.markdown(f"⏱️ Next check in {int(time_remaining)} seconds...")
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
            st.success(f"✅ Status changed to: {code_major}")
            
            # If codeMajor is "success", show the result object
            if code_major == "success":
                result_object = full_response.get("result", {})
                with st.expander("📋 View Result", expanded=True):
                    st.json(result_object)
            else:
                # For other statuses, show the full response
                st.markdown("### Final Response:")
                st.json(full_response)
            
            # Clear the status result after showing
            if "status_result" in st.session_state:
                del st.session_state.status_result
            if "status" in st.session_state:
                del st.session_state.status
    
    # Main UI
    st.markdown('<h1 class="main-header">🏠 AI Auto Design</h1>', unsafe_allow_html=True)
    st.markdown("---")

# Sidebar for additional info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This application allows you to design your kitchen space by selecting:
    - **Appliances**: Choose from various kitchen appliances
    - **Plumbing Fixtures**: Select plumbing fixtures like sinks
    - **Cabinets**: Select cabinet types (roof/base/tall)
    - **Worktops**: Pick your preferred worktop material
    
    Click **Build** to generate your design!
    """)
    st.markdown("---")
    st.markdown("**API Endpoint:**")
    st.code(API_ENDPOINT, language=None)

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
        "Roof Cabinet": "roof",
        "Base Cabinet": "base",
        "Tall Cabinet": "tall"
    }
    
    selected_cabinet_labels = st.multiselect(
        "Choose cabinet types:",
        options=list(cabinet_options.keys()),
        default=["Roof Cabinet", "Base Cabinet", "Tall Cabinet"],
        label_visibility="collapsed"
    )
    
    selected_cabinets = [cabinet_options[label] for label in selected_cabinet_labels]

with col4:
    # Worktop selection
    st.markdown('<div class="section-header">🪨 Worktop Material</div>', unsafe_allow_html=True)
    st.markdown("Choose your worktop material:")
    worktop_material = st.selectbox(
        "Choose your worktop material:",
        ["Granite", "Quartz", "Marble", "Wood", "Stainless Steel", "Laminate"],
        index=0,
        label_visibility="collapsed"
    )

# Build button
st.markdown("---")
build_button = st.button("🚀 Build Design", type="primary", use_container_width=True)

# Handle button click
if build_button:
    if not selected_appliances:
        st.error("⚠️ Please select at least one appliance.")
    elif not selected_plumbing_fixtures:
        st.error("⚠️ Please select at least one plumbing fixture.")
    elif not selected_cabinets:
        st.error("⚠️ Please select at least one cabinet type.")
    else:
        with st.spinner("🔄 Building your design... This may take a moment."):
            request_body = build_request_body(
                selected_appliances,
                selected_cabinets,
                worktop_material,
                selected_plumbing_fixtures
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
                    
                    # Create progress URL with query parameters
                    progress_url = f"?progress=true&request_id={request_id}" if request_id else "?progress=true"
                    
                    st.success("✅ Request submitted successfully!")
                    
                    # Show a clickable link to open progress page
                    st.markdown(f"""
                    <div style="margin-top: 1rem; padding: 1.5rem; background-color: #1e3a5f; border-radius: 10px; border: 1px solid #667eea;">
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
                    # Regular success response
                    st.success("✅ Design built successfully!")
                    st.markdown("### Response:")
                    st.json(result)
            else:
                st.error(f"❌ Error: {result}")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #718096; padding: 2rem;'>"
    "Built with ❤️ using Streamlit"
    "</div>",
    unsafe_allow_html=True
)
