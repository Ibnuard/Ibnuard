import urllib.request
import re
import json
import datetime
from html.parser import HTMLParser

# ================= PARSER FOR GITHUB CONTRIBUTIONS =================
class ContributionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []
        self.total_contributions = "1,143"  # fallback
        self.total_match_found = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if (tag in ['td', 'rect']) and 'class' in attrs_dict and 'ContributionCalendar-day' in attrs_dict['class']:
            level = int(attrs_dict.get('data-level', 0))
            date = attrs_dict.get('data-date', '')
            self.days.append({'date': date, 'level': level})

    def handle_data(self, data):
        if not self.total_match_found:
            match = re.search(r'([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year', data, re.IGNORECASE)
            if match:
                self.total_contributions = match.group(1)
                self.total_match_found = True

# Fetch data
try:
    print("Fetching contributions data for 'Ibnuard'...")
    html = urllib.request.urlopen('https://github.com/users/Ibnuard/contributions').read().decode('utf-8')
    parser = ContributionParser()
    parser.feed(html)
    contrib_count = parser.total_contributions
    days = parser.days
    print(f"Successfully parsed {len(days)} days. Yearly contributions: {contrib_count}")
except Exception as e:
    print(f"Error fetching data: {e}, using defaults.")
    contrib_count = "1,143"
    days = [{'date': (datetime.date.today() - datetime.timedelta(days=i)).strftime('%Y-%m-%d'), 'level': 0} for i in range(370)]
    days.reverse()

# Save JSON Data file for the interactive HTML web apps
contributions_data = {
    'total': contrib_count,
    'days': days,
    'last_updated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}
with open('contributions.json', 'w') as f:
    json.dump(contributions_data, f, indent=2)
print("Saved contributions.json successfully!")
