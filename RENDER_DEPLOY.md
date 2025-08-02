# Render Deployment Guide

## Deploy to Render.com (Better for ML apps)

1. **Go to [render.com](https://render.com)** and sign up
2. **Connect your GitHub account**
3. **Create a new Web Service**
4. **Connect your `hackrx1` repository**
5. **Use these settings:**

### Build & Deploy Settings:
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Environment Variables:
```
GEMINI_API_KEY=your_actual_gemini_api_key
BEARER_TOKEN=your_secure_bearer_token
PORT=10000
```

### Advanced Settings:
- **Auto-Deploy**: Yes
- **Health Check Path**: `/health`

## Why Render is Better:
- ✅ No 4GB image size limit
- ✅ Better for ML dependencies
- ✅ Handles torch, tensorflow, etc.
- ✅ More reliable builds
- ✅ Better logging

## After Deployment:
Your API will be available at: `https://your-app-name.onrender.com`

- Health: `https://your-app-name.onrender.com/health`
- Docs: `https://your-app-name.onrender.com/docs`
