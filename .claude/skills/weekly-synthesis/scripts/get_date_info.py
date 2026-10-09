#!/usr/bin/env python3
"""Output today's date, weekday, ISO week number, and week date range."""
from datetime import date, timedelta

today = date.today()
weekday = today.strftime("%A")
iso_year, iso_week, iso_weekday = today.isocalendar()
monday = today - timedelta(days=iso_weekday - 1)
friday = monday + timedelta(days=4)

print(f"date: {today.isoformat()}")
print(f"weekday: {weekday}")
print(f"week_number: W{iso_week:02d}")
print(f"iso_year: {iso_year}")
print(f"week_range: {monday.strftime('%d %b')}–{friday.strftime('%d %b %Y')}")
