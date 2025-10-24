# Quick Setup Guide (5 Minutes)

Follow these steps to get your smart webhook scheduler running on GitHub Actions.

## Prerequisites

- GitHub account (free tier is fine)
- n8n webhook URL

## Step 1: Create GitHub Repository (2 minutes)

### Option A: Create New Repository

1. Go to https://github.com/new
2. **Repository name**: `webhook-scheduler` (or any name you prefer)
3. **Visibility**: Private (recommended) or Public
4. **IMPORTANT**: Do NOT check "Add a README file"
5. Click **Create repository**

### Option B: Use Existing Repository

Skip to Step 2 if you already have a repository.

## Step 2: Upload Files (2 minutes)

### Via GitHub Website (Easiest)

1. On your new repository page, click **"uploading an existing file"**
2. Drag and drop ALL files from this folder:
   - `.github/` folder (including the workflows inside)
   - `scheduler.py`
   - `call_log.json`
   - `README.md`
   - `QUICK_SETUP.md`
   - `HOW_IT_WORKS.md`
3. Click **"Commit changes"**

### Via Git Command Line

```bash
# Navigate to this folder
cd /path/to/webhook-scheduler

# Initialize git (if not already a repo)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Smart webhook scheduler"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR-USERNAME/webhook-scheduler.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Add Your Webhook URL as a Secret (1 minute)

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. **Name**: `N8N_WEBHOOK_URL`
6. **Value**: Paste your full n8n webhook URL
   - Example: `https://your-n8n-instance.com/webhook/your-webhook-id`
7. Click **Add secret**

## Step 4: Verify It's Running

1. Go to the **Actions** tab in your repository
2. You should see the "Smart Webhook Scheduler" workflow
3. Wait up to 15 minutes for the first run (it runs every 15 minutes)
4. Click on any workflow run to see the logs

### Test It Immediately (Optional)

Don't want to wait? Trigger it manually:

1. Go to **Actions** tab
2. Click **Smart Webhook Scheduler** in the left sidebar
3. Click **Run workflow** button (top right)
4. Click the green **Run workflow** button
5. Watch it run in real-time!

## Step 5: Check the Logs

Click on any workflow run to see:

- Current date/time
- Business hours check
- Vacation check
- Random skip decisions
- Webhook call status
- Monthly call count

Example output:

```
============================================================
🤖 Smart Webhook Scheduler
============================================================
🕐 Current time: 2024-10-24 14:23:15 CEST
📅 Day: Thursday
📊 Calls this month: 23/600
------------------------------------------------------------
✅ All checks passed. Calling webhook...
⏱️ Adding human jitter: 12.45 seconds
✅ Webhook called successfully! (Call #24 this month)
📊 Response: 200
============================================================
```

## What Happens Now?

The workflow will:

- Run automatically every 15 minutes
- Check if it's business hours (9 AM - 5 PM Rome time)
- Apply all human behavior patterns
- Call your webhook if all checks pass
- Update `call_log.json` with the call count
- Stop automatically at 600 calls/month

## Monitoring

### Daily Monitoring

- Go to **Actions** tab
- Click on any run to see what happened
- Green checkmark = success
- Red X = error (click to see why)

### Monthly Stats

Check `call_log.json` in your repository to see:
```json
{
  "month": "2024-10",
  "count": 342,
  "last_call": "2024-10-24T14:23:15+02:00"
}
```

## Customization (Optional)

Want to change the behavior? Edit `scheduler.py`:

```python
# Change business hours
BUSINESS_START = 9  # Default: 9 AM
BUSINESS_END = 17   # Default: 5 PM

# Change timezone
TIMEZONE = ZoneInfo('Europe/Rome')  # Default: Rome

# Change monthly limit
MAX_CALLS_PER_MONTH = 600  # Default: 600

# Change skip probabilities
# Line ~65: Day skip (default 10%)
if random.random() < 0.10:

# Line ~72: Hour skip (default 20%)
if random.random() < 0.20:
```

## Troubleshooting

### "Workflow not running"

- Check if repository is active (GitHub disables after 60 days of no activity)
- Go to Actions tab and enable workflows if disabled

### "Webhook call failed"

- Verify `N8N_WEBHOOK_URL` secret is correct
- Test the webhook URL manually with curl:
  ```bash
  curl -X POST "YOUR_WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d '{"test": true}'
  ```

### "Too many/few calls"

- Adjust `MAX_CALLS_PER_MONTH` in `scheduler.py`
- Change skip probabilities
- Modify business hours

### "Permission denied when pushing call_log.json"

- This is normal on first run
- The workflow will create the commit on next run
- If persists, check repository permissions

## Next Steps

- Read [HOW_IT_WORKS.md](HOW_IT_WORKS.md) to understand the patterns
- Check GitHub Actions logs regularly
- Customize behavior in `scheduler.py` if needed

## Support

For issues:
1. Check the **Actions** logs for detailed error messages
2. Verify your webhook URL works manually
3. Review this guide for missed steps

---

**That's it! Your smart webhook scheduler is now running with realistic human patterns.**
