# Railway Deployment Checklist

## Pre-Deployment Checklist

### ✅ Repository Setup
- [ ] Code pushed to GitHub repository
- [ ] `.env` file is in `.gitignore` (never commit API keys!)
- [ ] `.env.example` file created with template
- [ ] `requirements.txt` is up to date

### ✅ Railway Configuration Files
- [ ] `Procfile` created with startup command
- [ ] `railway.toml` created with deployment config
- [ ] `runtime.txt` specifies Python version
- [ ] `Dockerfile` created (optional)

### ✅ Environment Variables
- [ ] `GEMINI_API_KEY` - Your Google Gemini API key
- [ ] `BEARER_TOKEN` - Secure authentication token
- [ ] `PORT` - Will be set automatically by Railway

### ✅ API Keys & Tokens
- [ ] Google Gemini API key is valid and active
- [ ] Bearer token is secure (not the default one)
- [ ] API key has sufficient quota for expected usage

## Deployment Steps

### 1. Railway Account Setup
- [ ] Sign up at [railway.app](https://railway.app)
- [ ] Connect your GitHub account

### 2. Project Deployment
- [ ] Create new project in Railway
- [ ] Connect to your GitHub repository
- [ ] Set environment variables in Railway dashboard
- [ ] Deploy and wait for build completion

### 3. Post-Deployment Testing
- [ ] Check health endpoint: `/health`
- [ ] Test API documentation: `/docs`
- [ ] Test a simple API call with valid bearer token
- [ ] Verify logs in Railway dashboard

## URLs After Deployment

Replace `your-app-name` with your actual Railway app name:

- **Health Check**: `https://your-app-name.railway.app/health`
- **API Docs**: `https://your-app-name.railway.app/docs`
- **Main API**: `https://your-app-name.railway.app/hackrx/run`
- **Upload API**: `https://your-app-name.railway.app/hackrx/upload`

## Testing Your Deployed API

### Using curl:
```bash
# Test health endpoint
curl https://your-app-name.railway.app/health

# Test document processing
curl -X POST "https://your-app-name.railway.app/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-bearer-token" \
  -d '{
    "documents": "https://example.com/sample.pdf",
    "questions": ["What is this document about?"]
  }'
```

### Using Python:
```python
import requests

url = "https://your-app-name.railway.app/hackrx/run"
headers = {
    "Authorization": "Bearer your-bearer-token",
    "Content-Type": "application/json"
}
data = {
    "documents": "https://example.com/sample.pdf",
    "questions": ["What is this document about?"]
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

## Troubleshooting

### Common Issues:
1. **Build fails**: Check `requirements.txt` and Python version
2. **App crashes**: Check environment variables are set correctly
3. **API errors**: Verify GEMINI_API_KEY is valid
4. **Authentication fails**: Check BEARER_TOKEN is set and correct

### Check Logs:
- Go to Railway dashboard
- Select your project
- Click on "Deployments" tab
- View build and runtime logs

## Security Reminders

- ✅ `.env` file is in `.gitignore`
- ✅ Real API keys are only in Railway environment variables
- ✅ Bearer token is strong and unique
- ✅ No sensitive data in git history

## Performance Tips

- Monitor API usage in Railway dashboard
- Check Google Gemini API quota usage
- Scale up Railway plan if needed for higher traffic
- Use Railway's metrics to monitor response times

---

**Your HackRX 5.0 project is now ready for Railway deployment! 🚀**
