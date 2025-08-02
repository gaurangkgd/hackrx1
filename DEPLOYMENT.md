# Deployment Guide for Railway

## Quick Railway Deployment

### 1. Prerequisites
- GitHub account with your code pushed to a repository
- Railway account (sign up at [railway.app](https://railway.app))
- Google Gemini API key

### 2. Environment Variables Setup
In Railway dashboard, add these environment variables:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
BEARER_TOKEN=your_secure_bearer_token_here
PORT=8000
PYTHONPATH=.
```

### 3. Deploy to Railway

#### Option A: Connect GitHub Repository
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your hackrx repository
5. Railway will automatically detect Python and deploy

#### Option B: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 4. Post-Deployment
- Railway will provide a public URL
- Health check endpoint: `https://your-app.railway.app/health`
- API docs: `https://your-app.railway.app/docs`

### 5. Environment Variables Required
- `GEMINI_API_KEY`: Your Google Gemini API key
- `BEARER_TOKEN`: Authentication token for API access
- `PORT`: Automatically set by Railway (defaults to 8000)

### 6. Scaling & Monitoring
- Railway automatically handles scaling
- Monitor usage in Railway dashboard
- Check logs for debugging

## Alternative Deployment Options

### Docker Deployment
```bash
# Build image
docker build -t hackrx-app .

# Run container
docker run -p 8000:8000 --env-file .env hackrx-app
```

### Local Development
```bash
# Activate virtual environment
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set environment variables in .env file
# Start server
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## Configuration Files Created

- `Procfile`: Railway startup command
- `railway.toml`: Railway-specific configuration
- `Dockerfile`: Container deployment option
- `runtime.txt`: Python version specification
- `.env.example`: Environment variables template

## Security Notes

- Never commit `.env` file to GitHub
- Use strong, unique tokens for BEARER_TOKEN
- Rotate API keys regularly
- Monitor API usage to prevent abuse

## Support

For deployment issues:
- Check Railway logs in dashboard
- Verify all environment variables are set
- Ensure API keys are valid
- Check the `/health` endpoint for service status
