import sys
import json
from dateparser import parse
from datetime import datetime, timedelta

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_common_dates():
    now = datetime.now()
    common_dates = {
        "Today": now.strftime('%Y-%m-%d'),
        "Tomorrow": (now + timedelta(days=1)).strftime('%Y-%m-%d'),
        "Day After Tomorrow": (now + timedelta(days=2)).strftime('%Y-%m-%d'),
        "End of This Week": (now + timedelta(days=(6 - now.weekday()))).strftime('%Y-%m-%d'),
        "Start of Next Week": (now + timedelta(days=(7 - now.weekday()))).strftime('%Y-%m-%d'),
        "End of This Month": (now.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1),
        "Start of Next Month": (now.replace(day=28) + timedelta(days=4)).replace(day=1),
        "End of This Year": datetime(now.year, 12, 31).strftime('%Y-%m-%d'),
        "Start of Next Year": datetime(now.year + 1, 1, 1).strftime('%Y-%m-%d'),
    }
    return {k: v.strftime('%Y-%m-%d') if isinstance(v, datetime) else v for k, v in common_dates.items()}

def get_iso_date(user_input):
    try:
        date_obj = parse(user_input, settings={'PREFER_DATES_FROM': 'future'})
        if date_obj:
            iso_date = date_obj.strftime('%Y-%m-%d')
            return iso_date
        return None
    except Exception as e:
        eprint(f"Error parsing date: {e}")
        return None

def main():
    user_input = sys.argv[1] if len(sys.argv) > 1 else None
    items = []

    if user_input:
        iso_date = get_iso_date(user_input)
        if iso_date:
            items.append({
                "title": iso_date,
                "arg": iso_date
            })
        else:
            items.append({
                "title": f"Could not parse date: {user_input}",
                "arg": ""
            })
    else:
        # Show common dates if there is no user input
        common_dates = get_common_dates()
        for label, date in common_dates.items():
            items.append({
                "title": f"{label}: {date}",
                "arg": date
            })

    print(json.dumps({"items": items}))

if __name__ == "__main__":
    main()
