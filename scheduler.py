#!/usr/bin/env python3
"""
Smart Webhook Scheduler with Ultra-Realistic Human Behavior Patterns
Designed to mimic natural user activity and avoid detection as automated traffic.
"""

import os
import json
import random
import time
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Configuration
WEBHOOK_URL = os.environ.get('N8N_WEBHOOK_URL')
TIMEZONE = ZoneInfo('Europe/Rome')
CALL_LOG_FILE = 'call_log.json'
MAX_CALLS_PER_MONTH = 1800

# Business hours: 9 AM to 5 PM Rome time
BUSINESS_START = 9
BUSINESS_END = 17

# Lunch break: 12 PM to 2 PM (30% less activity)
LUNCH_START = 12
LUNCH_END = 14
LUNCH_ACTIVITY_REDUCTION = 0.3


def load_call_log():
    """Load the call log from file."""
    if os.path.exists(CALL_LOG_FILE):
        with open(CALL_LOG_FILE, 'r') as f:
            return json.load(f)
    return {'month': None, 'count': 0}


def save_call_log(log):
    """Save the call log to file."""
    with open(CALL_LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)


def get_current_month():
    """Get current month in YYYY-MM format."""
    return datetime.now(TIMEZONE).strftime('%Y-%m')


def is_vacation_period():
    """Check if it's a vacation period (August, Christmas, or random week)."""
    now = datetime.now(TIMEZONE)
    month = now.month
    day = now.day

    # August vacation
    if month == 8:
        return True

    # Christmas vacation (Dec 20 - Jan 6)
    if (month == 12 and day >= 20) or (month == 1 and day <= 6):
        return True

    # Random vacation weeks (10% chance per week)
    week_number = now.isocalendar()[1]
    random.seed(f"{now.year}-{week_number}")  # Consistent per week
    if random.random() < 0.10:
        return True

    return False


def is_business_hours():
    """Check if current time is within business hours (9 AM - 5 PM Rome time)."""
    now = datetime.now(TIMEZONE)
    hour = now.hour

    # Weekend check
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False

    # Business hours check
    return BUSINESS_START <= hour < BUSINESS_END


def get_day_activity_multiplier():
    """Get activity multiplier based on day of week with randomness."""
    now = datetime.now(TIMEZONE)
    day = now.weekday()  # Monday = 0, Sunday = 6

    # Add randomness to each day instead of fixed multipliers
    if day == 0:  # Monday: slower start
        base = 0.85
        multiplier = base + random.uniform(-0.05, 0.10)  # 0.80-0.95
    elif day == 4:  # Friday: variable (sometimes distracted, sometimes productive)
        base = 0.90
        multiplier = base + random.uniform(-0.10, 0.10)  # 0.80-1.00
    else:  # Tuesday-Thursday: mostly active but with variation
        base = 1.0
        multiplier = base + random.uniform(-0.05, 0.05)  # 0.95-1.05

    return max(0.7, min(multiplier, 1.05))  # Keep within reasonable bounds


def get_lunch_multiplier():
    """Get activity multiplier during lunch hours with randomness."""
    now = datetime.now(TIMEZONE)
    hour = now.hour

    if LUNCH_START <= hour < LUNCH_END:
        # Variable lunch behavior - sometimes people work through lunch, sometimes not
        base_reduction = LUNCH_ACTIVITY_REDUCTION + random.uniform(-0.15, 0.10)
        base_reduction = max(0.10, min(base_reduction, 0.50))  # 50-90% activity
        return 1.0 - base_reduction
    return 1.0


def should_skip_day():
    """Random chance to skip entire day - varies by day."""
    # Don't use seeded random - make it truly unpredictable
    # Base chance is 3%, but add some randomness
    skip_chance = random.uniform(0.02, 0.05)  # 2-5% chance
    return random.random() < skip_chance


def should_skip_hour():
    """Random chance to skip current hour - varies throughout the day."""
    now = datetime.now(TIMEZONE)

    # Base skip probability varies by time of day
    hour = now.hour

    # Early morning (9-10 AM): lower skip chance (getting started)
    if 9 <= hour < 10:
        base_skip = 0.05
    # Mid-morning (10-12): very active
    elif 10 <= hour < 12:
        base_skip = 0.08
    # Lunch time (12-14): higher skip chance
    elif 12 <= hour < 14:
        base_skip = 0.25
    # Afternoon (14-16): active again
    elif 14 <= hour < 16:
        base_skip = 0.10
    # Late afternoon (16-17): winding down
    else:
        base_skip = 0.15

    # Add randomness to the base probability
    skip_chance = base_skip + random.uniform(-0.03, 0.05)
    skip_chance = max(0, min(skip_chance, 0.4))  # Keep between 0-40%

    return random.random() < skip_chance


def should_execute():
    """Determine if webhook should be called based on all factors."""
    # Check monthly limit
    log = load_call_log()
    current_month = get_current_month()

    # Reset counter if new month
    if log['month'] != current_month:
        log['month'] = current_month
        log['count'] = 0
        save_call_log(log)

    # Check if monthly limit reached
    if log['count'] >= MAX_CALLS_PER_MONTH:
        print(f"✋ Monthly limit reached ({MAX_CALLS_PER_MONTH} calls). Skipping.")
        return False

    # Check vacation period
    if is_vacation_period():
        print("🏖️ Vacation period. Skipping.")
        return False

    # Check business hours
    if not is_business_hours():
        print("🌙 Outside business hours. Skipping.")
        return False

    # Check day skip
    if should_skip_day():
        print("📅 Random day skip. Skipping.")
        return False

    # Check hour skip
    if should_skip_hour():
        print("⏰ Random hour skip. Skipping.")
        return False

    # Calculate execution probability based on multipliers
    day_mult = get_day_activity_multiplier()
    lunch_mult = get_lunch_multiplier()

    # Variable base probability instead of fixed 95%
    base_probability = random.uniform(0.85, 0.98)  # 85-98% base chance

    final_probability = base_probability * day_mult * lunch_mult

    # Add occasional "micro-break" - random very low probability periods
    if random.random() < 0.05:  # 5% chance of micro-break
        final_probability *= 0.3  # Reduce probability to 30%
        print(f"☕ Micro-break period detected (probability: {final_probability:.2%})")

    # Random execution skip (based on final probability)
    if random.random() > final_probability:
        print(f"🎲 Random execution skip (probability: {final_probability:.2%}). Skipping.")
        return False

    return True


def add_human_jitter():
    """Add random delay to simulate human interaction timing with exponential distribution."""
    # Use exponential distribution for more realistic behavior
    # Most delays are short, but occasionally long delays occur
    # 80% of delays will be under 5 minutes, but can go up to 15 minutes

    if random.random() < 0.15:  # 15% chance of "burst" activity (quick response)
        jitter = random.uniform(0, 60)  # 0-1 minute
    elif random.random() < 0.70:  # 70% normal activity
        jitter = random.expovariate(1/180) # Average 3 minutes, but exponentially distributed
        jitter = min(jitter, 600)  # Cap at 10 minutes
    else:  # 15% chance of distracted/slow response
        jitter = random.uniform(300, 900)  # 5-15 minutes

    minutes = jitter / 60
    print(f"⏱️ Adding human jitter: {jitter:.0f} seconds ({minutes:.1f} minutes)")
    time.sleep(jitter)


def call_webhook():
    """Call the n8n webhook."""
    if not WEBHOOK_URL:
        print("❌ Error: N8N_WEBHOOK_URL environment variable not set!")
        return False

    try:
        now = datetime.now(TIMEZONE)
        timestamp = now.isoformat()

        # Add human jitter before calling
        add_human_jitter()

        # Make the webhook call
        response = requests.post(
            WEBHOOK_URL,
            json={
                'timestamp': timestamp,
                'source': 'github-actions-scheduler',
                'timezone': 'Europe/Rome'
            },
            timeout=30
        )

        response.raise_for_status()

        # Update call log
        log = load_call_log()
        log['count'] += 1
        log['last_call'] = timestamp
        save_call_log(log)

        print(f"✅ Webhook called successfully! (Call #{log['count']} this month)")
        print(f"📊 Response: {response.status_code}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Error calling webhook: {e}")
        return False


def main():
    """Main execution function."""
    print("=" * 60)
    print("🤖 Smart Webhook Scheduler")
    print("=" * 60)

    now = datetime.now(TIMEZONE)
    print(f"🕐 Current time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"📅 Day: {now.strftime('%A')}")

    # Load current stats
    log = load_call_log()
    current_month = get_current_month()
    if log['month'] == current_month:
        print(f"📊 Calls this month: {log['count']}/{MAX_CALLS_PER_MONTH}")
    else:
        print(f"📊 New month detected. Counter will reset.")

    print("-" * 60)

    # Decide if we should execute
    if should_execute():
        print("✅ All checks passed. Calling webhook...")
        call_webhook()
    else:
        print("⏭️ Skipping this execution cycle.")

    print("=" * 60)


if __name__ == '__main__':
    main()
