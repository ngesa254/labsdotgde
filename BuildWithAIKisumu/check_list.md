


# Cloud Run Deployment Checklist

## Pre-Deployment Checklist

Use this checklist before deploying your ADK agent to Cloud Run.

---

### ✅ Account & Project Setup

- [ ] Authenticated with correct Google account
  ```bash
  gcloud auth list
  # Should show: ngesa.marvin@gmail.com (active)
  ```

- [ ] Active project is set correctly
  ```bash
  gcloud config get-value project
  # Should show: devfestdala
  ```

- [ ] Billing is enabled on project
  ```bash
  gcloud beta billing projects describe devfestdala
  ```

---

### ✅ API Enablement

- [ ] Cloud Run API enabled
  ```bash
  gcloud services list --enabled | grep run.googleapis.com
  ```

- [ ] Artifact Registry API enabled
  ```bash
  gcloud services list --enabled | grep artifactregistry.googleapis.com
  ```

- [ ] Cloud Build API enabled
  ```bash
  gcloud services list --enabled | grep cloudbuild.googleapis.com
  ```

**Enable all at once if needed:**
```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

---

### ✅ IAM Permissions

- [ ] You have Cloud Run Admin role
  ```bash
  gcloud projects get-iam-policy devfestdala \
    --flatten="bindings[].members" \
    --filter="bindings.members:ngesa.marvin@gmail.com" \
    --format="table(bindings.role)"
  ```

**Required roles:**
- `roles/run.admin` - Cloud Run Admin
- `roles/iam.serviceAccountUser` - Service Account User
- `roles/storage.admin` - Storage Admin (for Artifact Registry)

---

### ✅ Agent Readiness

- [ ] Agent works locally
  ```bash
  cd ~/dala
  adk web
  # Test at http://127.0.0.1:8000
  ```

- [ ] Agent directory contains required files
  ```bash
  ls -la ~/dala
  # Should show: agent.py, .env, __init__.py
  ```

- [ ] API key is set in .env
  ```bash
  grep -q "GOOGLE_API_KEY" ~/dala/.env && echo "✓ API key found" || echo "✗ API key missing"
  ```

- [ ] No syntax errors in agent.py
  ```bash
  python3 -m py_compile ~/dala/agent.py
  ```

---

### ✅ Deployment Configuration

- [ ] Project ID confirmed: **devfestdala**
- [ ] Region selected: **africa-south1** (Johannesburg)
- [ ] Service name chosen: **dala-service**
- [ ] Memory allocation decided: **512Mi** (default) or custom
- [ ] CPU allocation decided: **1** (default) or custom
- [ ] Min instances decided: **0** (scale to zero) or **1+** (always ready)
- [ ] Max instances decided: **10** (default) or custom
- [ ] Access control decided: **Public** or **Private**

---

### ✅ Cost Consideration

- [ ] Understand Cloud Run pricing model
  - Pay per request
  - Pay for CPU/memory while processing
  - Free tier: 2M requests/month

- [ ] Budget alert configured (optional but recommended)
  ```bash
  gcloud billing budgets list --billing-account=BILLING_ACCOUNT_ID
  ```

- [ ] Starting with conservative resource limits
  - Memory: 512Mi (can adjust later)
  - Max instances: 10 (prevents runaway costs)

---

### ✅ Security Checklist

- [ ] API key not committed to git
  ```bash
  git check-ignore .env
  # Should output: .env
  ```

- [ ] Consider using Secret Manager for production
  ```bash
  # Create secret (optional for now)
  # echo -n "API_KEY" | gcloud secrets create google-api-key --data-file=-
  ```

- [ ] Decide on authentication strategy
  - Public: `--allow-unauthenticated` (for demos)
  - Private: `--no-allow-unauthenticated` (for internal)

---

## Deployment Command Ready

Once all checks pass, run:

```bash
cd ~/dala

adk deploy cloud_run \
  --project=devfestdala \
  --region=africa-south1 \
  --service_name=dala-service \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=10 \
  --allow-unauthenticated \
  ./dala
```

---

## Post-Deployment Verification

After deployment completes:

- [ ] Service URL obtained
  ```bash
  gcloud run services describe dala-service \
    --region=africa-south1 \
    --format='value(status.url)'
  ```

- [ ] Service is accessible
  ```bash
  curl $(gcloud run services describe dala-service \
    --region=africa-south1 \
    --format='value(status.url)')
  ```

- [ ] Agent responds correctly
  - Open service URL in browser
  - Send test message
  - Verify response

- [ ] Logs are accessible
  ```bash
  gcloud run services logs read dala-service \
    --region=africa-south1 \
    --limit=10
  ```

- [ ] No errors in logs
  ```bash
  gcloud run services logs read dala-service \
    --region=africa-south1 \
    --filter="severity>=ERROR" \
    --limit=10
  ```

---

## Quick Command Reference

### One-Line Verification
```bash
echo "Account: $(gcloud config get-value account) | Project: $(gcloud config get-value project) | Agent: $([ -f ~/dala/agent.py ] && echo '✓' || echo '✗') | APIs: $(gcloud services list --enabled | grep -c 'run.googleapis.com')/3"
```

### Enable All Required APIs
```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

### Test Agent Locally
```bash
cd ~/dala && adk web
```

### Deploy
```bash
cd ~/dala && adk deploy cloud_run \
  --project=devfestdala \
  --region=africa-south1 \
  --service_name=dala-service \
  ./dala
```

### Get Service URL
```bash
gcloud run services describe dala-service \
  --region=africa-south1 \
  --format='value(status.url)'
```

### View Logs
```bash
gcloud run services logs tail dala-service --region=africa-south1
```

---

## Troubleshooting Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| Billing not enabled | Visit: https://console.cloud.google.com/billing |
| API not enabled | `gcloud services enable run.googleapis.com` |
| Permission denied | Check IAM roles in Cloud Console |
| Agent not working locally | Check `adk web` for errors |
| Deployment fails | Check Cloud Build logs |
| Service not responding | Check environment variables |

---

## Emergency Rollback

If deployment fails or service has issues:

```bash
# List revisions
gcloud run revisions list --service=dala-service --region=africa-south1

# Rollback to previous revision
gcloud run services update-traffic dala-service \
  --region=africa-south1 \
  --to-revisions=PREVIOUS_REVISION=100

# Or delete service and redeploy
gcloud run services delete dala-service --region=africa-south1
```

---

## Estimated Timeline

- **Pre-checks:** 5-10 minutes
- **API enablement:** 2-3 minutes
- **Deployment:** 5-10 minutes
- **Verification:** 2-3 minutes
- **Total:** 15-25 minutes

---

## Success Criteria

Deployment is successful when:

✅ Command completes without errors  
✅ Service URL is returned  
✅ Service is accessible via browser  
✅ Agent responds to test queries  
✅ No errors in logs  
✅ Service shows as "Ready" in console  

---

**Ready to Deploy?**

If all checkboxes above are ticked, you're ready to deploy! 🚀

```bash
cd ~/dala
adk deploy cloud_run \
  --project=devfestdala \
  --region=africa-south1 \
  --service_name=dala-service \
  --allow-unauthenticated \
  ./dala
```

---

**Created:** November 8, 2025  
**Last Updated:** November 8, 2025




/////


# 🚀 ADK Quick Start Guide - From Zero to Deployed in 30 Minutes

## Your Configuration
- **Email:** ngesa.marvin@gmail.com
- **Project:** devfestdala
- **Region:** africa-south1 (Johannesburg)
- **Service:** dala-service

---

## 📋 Complete Command Sequence

Copy and paste these commands in order. That's it!

### Step 1: Setup (5 minutes)

```bash
# Login and configure
gcloud auth login --account=ngesa.marvin@gmail.com --update-adc
gcloud config set project devfestdala

# Verify setup
bash verify_adk_setup.sh

# If verification fails, fix issues and re-run
```

### Step 2: Create Agent (5 minutes)
*(Skip if you already have ~/dala)*

```bash
# Navigate home
cd ~

# Create agent
adk create dala

# When prompted:
# Model: 1 (gemini-2.5-flash)
# Backend: 1 (Google AI)
# API Key: [Get from https://aistudio.google.com/apikey]
```

### Step 3: Test Locally (5 minutes)

```bash
# Start local server
cd ~/dala
adk web

# Open http://127.0.0.1:8000 in browser
# Test your agent
# Press Ctrl+C to stop when done
```

### Step 4: Deploy to Cloud Run (10-15 minutes)

```bash
# Automated deployment (recommended)
bash deploy_to_cloudrun.sh

# Follow prompts, confirm deployment
# Wait for completion
# Copy your service URL when provided
```

**OR Manual Deployment:**

```bash
# Enable APIs first
gcloud services enable run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com

# Deploy
cd ~/dala
adk deploy cloud_run \
  --project=devfestdala \
  --region=africa-south1 \
  --service_name=dala-service \
  --allow-unauthenticated \
  ./dala

# Get your service URL
gcloud run services describe dala-service \
  --region=africa-south1 \
  --format='value(status.url)'
```

---

## ✅ Success Checklist

After running the commands above:

- [ ] `verify_adk_setup.sh` shows "ALL CHECKS PASSED!"
- [ ] Agent works at http://127.0.0.1:8000
- [ ] Deployment completes without errors
- [ ] You receive a service URL (https://dala-service-XXX.run.app)
- [ ] Service URL opens in browser
- [ ] Agent responds online

**If all checked → You're done! 🎉**

---

## 🆘 If Something Goes Wrong

### Setup Issues
```bash
# Re-run verification to identify problem
bash verify_adk_setup.sh

# Common fixes:
gcloud auth login --account=ngesa.marvin@gmail.com --update-adc
gcloud config set project devfestdala
uv tool install google-adk
```

### Deployment Issues
```bash
# Check what went wrong
bash deploy_to_cloudrun.sh

# The script will tell you exactly what's missing
# Fix that issue and run again

# View build logs if deployment fails
gcloud builds list --limit=1
gcloud builds log $(gcloud builds list --limit=1 --format='value(id)')
```

### Service Not Responding
```bash
# Check logs
gcloud run services logs read dala-service \
  --region=africa-south1 \
  --limit=50

# Look for errors
gcloud run services logs read dala-service \
  --region=africa-south1 \
  --filter="severity>=ERROR"
```

---

## 📱 Essential URLs

| What | Where |
|------|-------|
| AI Studio (API keys) | https://aistudio.google.com/apikey |
| GCP Console | https://console.cloud.google.com |
| Your Project | https://console.cloud.google.com/home/dashboard?project=devfestdala |
| Cloud Run Services | https://console.cloud.google.com/run?project=devfestdala |

---

## 🔄 Daily Workflow

Once set up, your daily workflow is simple:

```bash
# 1. Quick check (30 seconds)
bash verify_adk_setup.sh

# 2. Start local development (1 second)
cd ~/dala && adk web

# 3. Make your changes to agent.py
# ... edit files ...

# 4. Test locally
# ... test in browser ...

# 5. Deploy when ready (2 minutes)
bash deploy_to_cloudrun.sh
```

---

## 📊 What You Get

After deployment:

### Your Service
- **URL:** https://dala-service-[unique-id].run.app
- **Type:** Public (anyone can access)
- **Region:** Johannesburg, South Africa
- **Cost:** ~$0-5/month for dev/demo usage

### Features
- ✅ Auto-scaling (scales to 0 when idle)
- ✅ HTTPS by default
- ✅ Global CDN
- ✅ Automatic logging
- ✅ Zero maintenance

---

## 🎯 Next Steps

Now that you're deployed:

### Immediate (Today)
1. Test your deployed agent
2. Share the URL with team/stakeholders
3. Monitor logs for any issues

### This Week
1. Read `ADK_CLOUD_RUN_DEPLOYMENT.md` for advanced features
2. Set up monitoring and alerts
3. Configure budget alerts

### This Month
1. Implement authentication if going to production
2. Optimize resource usage based on metrics
3. Set up CI/CD pipeline

---

## 🔧 Useful Commands

### Check Everything
```bash
# One command to verify your entire setup
bash verify_adk_setup.sh
```

### Deploy
```bash
# One command to deploy with all checks
bash deploy_to_cloudrun.sh
```

### Get Service Info
```bash
# Get your service URL
gcloud run services describe dala-service \
  --region=africa-south1 \
  --format='value(status.url)'

# Check service status
gcloud run services describe dala-service \
  --region=africa-south1
```

### View Logs
```bash
# Live log streaming
gcloud run services logs tail dala-service \
  --region=africa-south1

# Recent errors only
gcloud run services logs read dala-service \
  --region=africa-south1 \
  --filter="severity>=ERROR" \
  --limit=20
```

### Update Service
```bash
# Update code
cd ~/dala
bash deploy_to_cloudrun.sh

# Update configuration only
gcloud run services update dala-service \
  --region=africa-south1 \
  --memory=1Gi \
  --max-instances=20
```

---

## 💰 Cost Estimates

Based on your configuration:

### Development/Demo (Current)
- **Requests:** < 10K/month
- **Instances:** Mostly zero (scales to 0)
- **Cost:** $0-5/month

### Light Production
- **Requests:** 10K-100K/month
- **Instances:** 1-5 running
- **Cost:** $10-50/month

### Heavy Production
- **Requests:** 100K-1M/month
- **Instances:** 5-20 running
- **Cost:** $50-500/month

**Free Tier:** 2 million requests/month included

---

## 🔐 Security Quick Tips

### For Development (Current Setup)
✅ API key in .env file  
✅ .env in .gitignore  
✅ Public access enabled (for demo)  

### For Production (Before Going Live)
✅ Move API key to Secret Manager  
✅ Disable public access  
✅ Implement authentication  
✅ Set up rate limiting  
✅ Enable Cloud Armor  

---

## 📖 Where to Find More Info

| Question | Document |
|----------|----------|
| How do I set up ADK? | `ADK_GCP_SETUP_GUIDE.md` |
| Quick command reference? | `ADK_QUICK_REFERENCE.md` |
| How do I deploy? | `ADK_CLOUD_RUN_DEPLOYMENT.md` |
| Pre-deployment checklist? | `DEPLOYMENT_CHECKLIST.md` |
| Complete workflow? | `README_COMPLETE.md` |

---

## 🎓 Pro Tips

1. **Always verify before deploying**
   ```bash
   bash verify_adk_setup.sh
   ```

2. **Test locally first**
   ```bash
   cd ~/dala && adk web
   ```

3. **Use the automated scripts**
   ```bash
   bash deploy_to_cloudrun.sh
   ```

4. **Monitor your logs**
   ```bash
   gcloud run services logs tail dala-service --region=africa-south1
   ```

5. **Set a budget alert**
   - Go to: https://console.cloud.google.com/billing
   - Set alert at $10, $25, $50

---

## ✨ You're All Set!

Your ADK agent is now:
- ✅ Running locally for development
- ✅ Deployed to Cloud Run for production
- ✅ Accessible via HTTPS
- ✅ Auto-scaling based on traffic
- ✅ Monitored and logged

**Start building amazing AI applications! 🚀**

---

## 📞 Quick Help

**Setup not working?**  
→ Run: `bash verify_adk_setup.sh`

**Deployment failing?**  
→ Run: `bash deploy_to_cloudrun.sh` (it will identify issues)

**Service not responding?**  
→ Check: `gcloud run services logs tail dala-service --region=africa-south1`

**Need detailed help?**  
→ Read: `ADK_CLOUD_RUN_DEPLOYMENT.md` (troubleshooting section)

---

**Created:** November 8, 2025  
**Version:** 1.0  
**Time to Deploy:** ~30 minutes  
**Documentation Files:** 8 total  

**Ready? Let's go! 🎯**

```bash
bash verify_adk_setup.sh
```