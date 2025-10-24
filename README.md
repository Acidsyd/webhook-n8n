# Smart Webhook Scheduler with Ultra-Realistic Human Behavior

A GitHub Actions-powered webhook scheduler that mimics natural human activity patterns to call your n8n webhook approximately **600 times per month** with ultra-realistic behavior.

## Why This Is Different

Most automated schedulers have detectable patterns. This one doesn't. It simulates realistic human behavior with:

- **Business Hours Only**: 9 AM - 5 PM Rome time, Monday-Friday
- **Vacation Breaks**: Automatically skips August, Christmas, and random weeks
- **Lunch Slowdown**: 70% less activity during lunch hours (12-2 PM)
- **Weekly Patterns**: Slower on Mondays (70%) and Fridays (80%)
- **Random Skips**: Days (10%), hours (20%), and individual executions (15%)
- **Human Jitter**: Random 0-10 minute delays before each call
- **Monthly Cap**: Automatically stops at 600 calls per month

## Quick Start

**See [QUICK_SETUP.md](QUICK_SETUP.md) for step-by-step setup instructions (5 minutes).**

## How It Works

**See [HOW_IT_WORKS.md](HOW_IT_WORKS.md) for a visual diagram and detailed explanation.**

## Features

### Realistic Time Patterns

- Runs every 15 minutes (GitHub Actions cron)
- Filters for business hours: 9 AM - 5 PM Rome time
- Weekdays only (no weekends)
- Reduced activity during lunch: 12-2 PM

### Vacation Intelligence

Automatically skips:
- **August**: Full summer vacation
- **Christmas**: December 20 - January 6
- **Random weeks**: 10% chance per week throughout the year

### Activity Variation

- **Monday**: 70% activity (slow start to week)
- **Tuesday-Thursday**: 100% activity (peak productivity)
- **Friday**: 80% activity (winding down)
- **Lunch hours**: 30% activity (12-2 PM)

### Random Behavior

- **10% chance** to skip entire day
- **20% chance** to skip current hour
- **~15% chance** to skip individual execution
- **0-10 minutes** random delay before each call

### Monthly Limit

- Tracks calls per month in `call_log.json`
- Stops automatically at 600 calls
- Resets counter on new month

## Files

- `.github/workflows/webhook-scheduler.yml` - GitHub Actions workflow
- `scheduler.py` - Smart scheduling logic with human patterns
- `call_log.json` - Monthly call counter (auto-updated)
- `README.md` - This file
- `QUICK_SETUP.md` - Setup guide
- `HOW_IT_WORKS.md` - Detailed explanation

## Requirements

- GitHub account (free tier works)
- n8n webhook URL
- No local installation needed (runs entirely on GitHub)

## Cost

**$0.00/month** - Runs entirely on GitHub Actions free tier.

GitHub provides 2,000 free minutes/month. This workflow uses ~100 minutes/month.

## Setup

1. Fork this repository or create a new one with these files
2. Add your webhook URL as a secret (`N8N_WEBHOOK_URL`)
3. Push to GitHub
4. Done! It runs automatically every 15 minutes

**For detailed setup steps, see [QUICK_SETUP.md](QUICK_SETUP.md).**

## Monitoring

Check the "Actions" tab in your GitHub repository to see:
- Workflow runs
- Call success/failure
- Monthly call count
- Skip reasons

## Customization

Edit `scheduler.py` to adjust:
- Business hours (`BUSINESS_START`, `BUSINESS_END`)
- Timezone (`TIMEZONE`)
- Monthly limit (`MAX_CALLS_PER_MONTH`)
- Skip probabilities
- Vacation periods

## Privacy & Security

- Your webhook URL is stored as a GitHub secret (encrypted)
- Call logs only track counts, not data
- No external services or databases
- Runs entirely on GitHub infrastructure

## Troubleshooting

### Webhook not being called

1. Check GitHub Actions logs for errors
2. Verify `N8N_WEBHOOK_URL` secret is set correctly
3. Test webhook manually with `workflow_dispatch`

### Too many/few calls

- Adjust `MAX_CALLS_PER_MONTH` in `scheduler.py`
- Modify skip probabilities
- Change business hours

### Workflow not running

- Ensure repository is active (GitHub disables workflows after 60 days of inactivity)
- Check `.github/workflows/webhook-scheduler.yml` syntax
- Verify cron schedule is correct

## License

MIT - Free to use and modify

## Support

For issues or questions, see the GitHub Actions logs in the "Actions" tab of your repository.

---

**Built with realistic human behavior patterns for undetectable automation.**
