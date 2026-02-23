# GitHub Actions CI/CD Setup Guide

This guide explains how to set up automatic deployment to EC2 using GitHub Actions.

## Overview

When you push code to the `main` branch, GitHub Actions will automatically:
1. ✅ Connect to your EC2 instance
2. ✅ Upload the latest code
3. ✅ Install/update dependencies
4. ✅ Restart the application
5. ✅ Verify deployment success

## Setup Instructions

### Step 1: Prepare Your EC2 Instance

First, ensure your EC2 instance is set up with:
- Supervisor configured to manage the app
- Virtual environment created
- All dependencies installed

If not done yet, SSH into your EC2 and run:

```bash
cd /home/ubuntu
git clone https://github.com/dungarpan/Image-Captioning.git
cd Image-Captioning

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup supervisor (if not done)
sudo apt install -y supervisor
sudo cp deployment/supervisor.conf /etc/supervisor/conf.d/image-caption.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start image-caption
```

### Step 2: Add GitHub Secrets

You need to add three secrets to your GitHub repository:

#### 1. Get your EC2 SSH Private Key content
```bash
cat captioning-key-pair.pem
```
Copy the entire content (including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`)

#### 2. Add Secrets to GitHub

Go to your GitHub repository:
1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the following three secrets:

**Secret 1: EC2_SSH_KEY**
- Name: `EC2_SSH_KEY`
- Value: Paste your entire `.pem` file content

**Secret 2: EC2_HOST**
- Name: `EC2_HOST`
- Value: Your EC2 public IP or domain (e.g., `54.123.45.67`)

**Secret 3: EC2_USER**
- Name: `EC2_USER`
- Value: `ubuntu` (or your EC2 username)

### Step 3: Test the Workflow

#### Option A: Push to trigger deployment
```bash
git add .
git commit -m "Test deployment"
git push origin main
```

#### Option B: Manual trigger
1. Go to your GitHub repository
2. Click **Actions** tab
3. Click **Deploy to EC2** workflow
4. Click **Run workflow** → **Run workflow**

### Step 4: Monitor Deployment

1. Go to **Actions** tab in your GitHub repository
2. Click on the latest workflow run
3. Watch the deployment progress in real-time
4. Check for any errors in the logs

## Workflow File Explained

The workflow file (`.github/workflows/deploy.yml`) does the following:

```yaml
on:
  push:
    branches: [main]  # Triggers on push to main
  workflow_dispatch:   # Allows manual trigger
```

- Automatically runs when you push to `main`
- Can be manually triggered from GitHub UI

## Troubleshooting

### SSH Connection Failed
- Check that `EC2_SSH_KEY` secret contains the correct private key
- Verify `EC2_HOST` has your correct EC2 IP
- Ensure EC2 security group allows SSH (port 22) from GitHub's IP ranges

### Permission Denied
- Make sure the SSH key matches the one used when creating EC2
- Verify EC2_USER is correct (usually `ubuntu` for Ubuntu AMI)

### Application Won't Start
- SSH into EC2 manually: `ssh -i captioning-key-pair.pem ubuntu@YOUR_EC2_IP`
- Check logs: `sudo supervisorctl tail -f image-caption`
- Check supervisor status: `sudo supervisorctl status`

### Deployment Succeeds but App Not Working
- Check if dependencies installed: `source venv/bin/activate && pip list`
- Check app logs: `sudo tail -f /var/log/image-caption.err.log`
- Restart manually: `sudo supervisorctl restart image-caption`

## Advanced Configuration

### Deploy to Multiple Environments

Add separate workflows for staging and production:

```yaml
# .github/workflows/deploy-staging.yml
on:
  push:
    branches: [develop]
```

```yaml
# .github/workflows/deploy-production.yml
on:
  push:
    branches: [main]
```

### Add Notifications

Add Slack/Discord notifications:

```yaml
- name: Notify on Success
  if: success()
  run: |
    curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
      -d '{"text":"Deployment to EC2 successful!"}'
```

### Run Tests Before Deploy

```yaml
- name: Run Tests
  run: |
    pip install pytest
    pytest tests/
```

## Security Best Practices

1. ✅ **Never commit `.pem` files** - They're in `.gitignore`
2. ✅ **Use GitHub Secrets** - Never hardcode credentials
3. ✅ **Rotate SSH keys** regularly
4. ✅ **Limit SSH access** - Use Security Groups to restrict IP ranges
5. ✅ **Use IAM roles** - Consider AWS IAM roles instead of SSH keys for production

## Useful Commands

### Check Workflow Status
```bash
gh run list  # If you have GitHub CLI installed
```

### View Workflow Logs
```bash
gh run view --log
```

### Manually Trigger Workflow
```bash
gh workflow run deploy.yml
```

## What Gets Deployed

The workflow deploys:
- ✅ All Python files (`app.py`, etc.)
- ✅ `requirements.txt`
- ✅ `deployment/` directory
- ✅ `README.md` and documentation
- ❌ `.env` files (excluded by `.gitignore`)
- ❌ `.pem` files (excluded by `.gitignore`)
- ❌ `venv/` (excluded by `.gitignore`)
- ❌ Image files (optional, based on `.gitignore`)

## Cost Considerations

- GitHub Actions provides **2,000 free minutes/month** for private repos
- This workflow typically takes **1-2 minutes per deployment**
- You can run ~1,000 deployments/month for free

---

## Quick Reference

```bash
# Local: Push changes
git add .
git commit -m "Update feature"
git push origin main

# GitHub Actions automatically:
# 1. Connects to EC2
# 2. Uploads code
# 3. Installs dependencies
# 4. Restarts app
# 5. Verifies deployment

# Verify on EC2
curl http://YOUR_EC2_IP/health
```

Your API will be updated automatically! 🚀

