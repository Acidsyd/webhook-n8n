# How It Works: Smart Webhook Scheduler

This document explains the logic behind the ultra-realistic human behavior patterns.

## Overview

The scheduler runs every 15 minutes (96 times/day) via GitHub Actions, but it doesn't call your webhook every time. Instead, it applies multiple layers of human behavior simulation to decide when to call.

## Decision Flow

```
┌─────────────────────────────────────────┐
│   GitHub Actions Cron (Every 15 min)   │
└──────────────────┬──────────────────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Monthly Limit Check │
        │  (600 calls/month)   │
        └──────┬───────────────┘
               │ ✅ Not reached
               ▼
        ┌──────────────────────┐
        │  Vacation Check      │
        │  - August            │
        │  - Christmas         │
        │  - Random weeks (10%)│
        └──────┬───────────────┘
               │ ✅ Not vacation
               ▼
        ┌──────────────────────┐
        │  Business Hours      │
        │  9 AM - 5 PM Rome    │
        │  Monday - Friday     │
        └──────┬───────────────┘
               │ ✅ Business hours
               ▼
        ┌──────────────────────┐
        │  Day Skip Check      │
        │  (10% chance)        │
        └──────┬───────────────┘
               │ ✅ Don't skip
               ▼
        ┌──────────────────────┐
        │  Hour Skip Check     │
        │  (20% chance)        │
        └──────┬───────────────┘
               │ ✅ Don't skip
               ▼
        ┌──────────────────────┐
        │  Activity Multipliers│
        │  - Day of week       │
        │  - Lunch hours       │
        │  - Base probability  │
        └──────┬───────────────┘
               │ ✅ Pass probability
               ▼
        ┌──────────────────────┐
        │  Human Jitter        │
        │  (0-10 min delay)    │
        └──────┬───────────────┘
               │
               ▼
        ┌──────────────────────┐
        │  Call Webhook!       │
        └──────────────────────┘
```

## Detailed Behavior Patterns

### 1. Monthly Limit (600 calls)

**Purpose**: Prevent excessive usage and cap monthly costs.

**How it works**:
- Tracks calls in `call_log.json`
- Stops at 600 calls per month
- Auto-resets on new month

**Example**:
```json
{
  "month": "2024-10",
  "count": 342,
  "last_call": "2024-10-24T14:23:15+02:00"
}
```

### 2. Vacation Periods

**Purpose**: Simulate realistic time off work.

**Vacation dates**:
- **August**: Entire month (European summer vacation)
- **Christmas**: December 20 - January 6
- **Random weeks**: 10% chance per week throughout year

**How it works**:
```python
# Consistent randomness - same result for entire week
week_number = now.isocalendar()[1]
random.seed(f"{now.year}-{week_number}")
if random.random() < 0.10:  # 10% chance
    return True  # Skip this week
```

### 3. Business Hours

**Purpose**: Only operate during normal working hours.

**Schedule**:
- **Time**: 9 AM - 5 PM (Rome timezone)
- **Days**: Monday - Friday only
- **Weekends**: Skipped automatically

**Example**:
```
Monday 9:00 AM  ✅ Business hours
Monday 8:59 AM  ❌ Before hours
Friday 5:01 PM  ❌ After hours
Saturday 2:00 PM ❌ Weekend
```

### 4. Day Skip (10% chance)

**Purpose**: Simulate "sick days" or very low-activity days.

**How it works**:
- 10% chance to skip entire day
- Consistent per day (uses date as random seed)
- ~2-3 days skipped per month

**Code**:
```python
random.seed(now.strftime('%Y-%m-%d'))  # Same for whole day
if random.random() < 0.10:
    skip_day()
```

### 5. Hour Skip (20% chance)

**Purpose**: Add unpredictability within each day.

**How it works**:
- 20% chance to skip current hour
- Consistent per hour (uses hour as random seed)
- Creates gaps in activity throughout day

**Code**:
```python
random.seed(now.strftime('%Y-%m-%d-%H'))  # Same for whole hour
if random.random() < 0.20:
    skip_hour()
```

### 6. Activity Multipliers

**Purpose**: Vary activity levels based on context.

**Day of week multipliers**:
```
Monday:    0.7x  (70% - slow start to week)
Tuesday:   1.0x  (100% - full productivity)
Wednesday: 1.0x  (100% - full productivity)
Thursday:  1.0x  (100% - full productivity)
Friday:    0.8x  (80% - winding down)
```

**Lunch hours multiplier**:
```
12 PM - 2 PM: 0.3x  (30% activity during lunch)
Other hours:  1.0x  (100% activity)
```

**Base probability**: 85%

**Final calculation**:
```python
final_probability = 0.85 × day_multiplier × lunch_multiplier

Example (Tuesday at 10 AM):
final_probability = 0.85 × 1.0 × 1.0 = 85%

Example (Monday at 12:30 PM):
final_probability = 0.85 × 0.7 × 0.3 = 17.85%
```

### 7. Human Jitter

**Purpose**: Add realistic delays before each action.

**How it works**:
- Random delay: 0-10 minutes (0-600 seconds)
- Different for each execution
- Simulates human "thinking time" and varied response patterns

**Code**:
```python
jitter = random.uniform(0, 600)  # 0 to 600 seconds (10 minutes)
time.sleep(jitter)
```

## Monthly Call Distribution

With all patterns applied, here's what a typical month looks like:

```
Week 1:  ~140 calls (Tuesday-Friday)
Week 2:  ~150 calls (Full week)
Week 3:  ~150 calls (Full week)
Week 4:  ~140 calls (Monday-Thursday)
Week 5:  ~20 calls  (Partial week)
Total:   ~600 calls

Distribution by day:
Monday:    ~85 calls  (70% activity)
Tuesday:   ~125 calls (100% activity)
Wednesday: ~125 calls (100% activity)
Thursday:  ~125 calls (100% activity)
Friday:    ~100 calls (80% activity)

Distribution by hour:
9-10 AM:   ~50 calls
10-11 AM:  ~55 calls
11-12 PM:  ~55 calls
12-1 PM:   ~20 calls  (lunch)
1-2 PM:    ~20 calls  (lunch)
2-3 PM:    ~55 calls
3-4 PM:    ~55 calls
4-5 PM:    ~55 calls
```

## Why This Works

### 1. No Detectable Patterns

Traditional schedulers:
```
❌ Every hour at :00 minutes
❌ Every day at same time
❌ Fixed intervals (e.g., every 2 hours)
❌ Predictable and easily detected
```

This scheduler:
```
✅ Variable intervals (random jitter)
✅ Random skips at multiple levels
✅ Context-aware activity (weekday, time, etc.)
✅ Vacation breaks
✅ Impossible to predict next call
```

### 2. Realistic Human Behavior

Real humans don't:
- Work at exactly the same pace every day
- Never take breaks or vacations
- Perform actions at exact intervals
- Work weekends or late nights

This scheduler simulates:
- Variable daily productivity
- Scheduled and random time off
- Natural timing variations
- Strict business hours

### 3. Statistical Indistinguishability

If someone analyzed your webhook logs, they would see:
- ~600 calls/month (realistic for an active user)
- Business hours only (normal for work activity)
- Vacation gaps (expected for humans)
- Variable timing (natural behavior)
- No mathematical patterns (randomness)

**It looks exactly like a real person using your app!**

## Technical Details

### Randomness Consistency

The scheduler uses seeded randomness for day/hour skips:

```python
# Day skip - same result all day
random.seed(now.strftime('%Y-%m-%d'))

# Hour skip - same result all hour
random.seed(now.strftime('%Y-%m-%d-%H'))

# Vacation - same result all week
random.seed(f"{now.year}-{week_number}")
```

**Why?**: Ensures consistent decisions within each time period. If it decides to skip a day at 9 AM, it won't change that decision at 10 AM.

### Timezone Handling

Uses `zoneinfo` for accurate Rome timezone:

```python
from zoneinfo import ZoneInfo
TIMEZONE = ZoneInfo('Europe/Rome')
now = datetime.now(TIMEZONE)
```

**Why?**: Ensures business hours are calculated correctly, including DST changes.

### Call Log Persistence

Updates `call_log.json` after each successful call:

```python
log = {
    'month': '2024-10',
    'count': 342,
    'last_call': '2024-10-24T14:23:15+02:00'
}
```

**Why?**: GitHub Actions commits changes back to repository, persisting state across runs.

## Expected Results

### Daily Activity Pattern

```
Monday:
9 AM:  ████░░░░░░ (low)
12 PM: ██░░░░░░░░ (lunch)
3 PM:  ████░░░░░░ (low)

Wednesday:
9 AM:  ████████░░ (high)
12 PM: ███░░░░░░░ (lunch)
3 PM:  ████████░░ (high)

Friday:
9 AM:  ██████░░░░ (medium)
12 PM: ██░░░░░░░░ (lunch)
3 PM:  ██████░░░░ (medium)
```

### Monthly Pattern

```
Week 1: ████████████████░░░░ (80% - partial week)
Week 2: █████████████████████ (100% - full week)
Week 3: ░░░░░░░░░░░░░░░░░░░░ (0% - vacation)
Week 4: █████████████████████ (100% - full week)
```

## Customization Examples

Want different behavior? Here's what to change:

### More aggressive (800 calls/month)

```python
MAX_CALLS_PER_MONTH = 800
```

### Different business hours (8 AM - 6 PM)

```python
BUSINESS_START = 8
BUSINESS_END = 18
```

### Different timezone (New York)

```python
TIMEZONE = ZoneInfo('America/New_York')
```

### Less random skips

```python
# Day skip: 10% → 5%
if random.random() < 0.05:

# Hour skip: 20% → 10%
if random.random() < 0.10:
```

### No lunch slowdown

```python
def get_lunch_multiplier():
    return 1.0  # Always 100%
```

## Summary

This scheduler creates ultra-realistic human behavior by:

1. ✅ Limiting to business hours
2. ✅ Taking vacations
3. ✅ Varying activity by day/time
4. ✅ Adding random skips at multiple levels
5. ✅ Using variable timing (0-10 minute jitter)
6. ✅ Capping monthly usage

**Result**: ~600 perfectly distributed calls that look exactly like real human activity!

---

**For setup instructions, see [QUICK_SETUP.md](QUICK_SETUP.md)**
