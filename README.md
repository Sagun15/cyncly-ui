# AI Auto Design - Streamlit App

A Streamlit web application for designing kitchen spaces using AI Auto Design API.

## Features

- Select kitchen appliances (Cooktop, Refrigerator, Oven, Range, Dishwasher)
- Choose plumbing fixtures (Sink)
- Select cabinet types (Roof, Base, Tall)
- Pick worktop materials (Granite, Quartz, Marble, Wood, Stainless Steel, Laminate)
- Real-time progress tracking with automatic polling
- View design results in JSON format

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your bearer token:

   **For local development:**
   ```bash
   # Copy the example secrets file
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   
   # Edit .streamlit/secrets.toml and add your bearer token
   # BEARER_TOKEN = "your_actual_token_here"
   ```

   **Or use environment variable:**
   ```bash
   export BEARER_TOKEN="your_actual_token_here"
   ```

3. Run the app:
```bash
streamlit run app.py
```

## Deployment

### Streamlit Community Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and set:
   - **Main file path**: `app.py`
   - **App URL**: (auto-generated)
6. Click "Deploy"

The app will be live at `https://your-app-name.streamlit.app`

## Configuration

The app uses the following API endpoint:
- Base URL: `https://ai-auto-design-api-service.azurewebsites.net`
- Bearer token must be configured via Streamlit secrets or environment variable

### Setting up Secrets in Streamlit Cloud

1. After deploying to Streamlit Cloud, go to your app's settings
2. Click on "Secrets" in the left sidebar
3. Add the following:
   ```toml
   BEARER_TOKEN = "your_actual_bearer_token_here"
   ```
4. Save and the app will automatically redeploy

## Requirements

- Python 3.8+
- streamlit>=1.28.0
- requests>=2.31.0
