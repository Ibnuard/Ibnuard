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
        self.total_contributions = "1,143"
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
    print(f"Error fetching data: {e}, using existing local data if available.")
    try:
        with open('contributions.json') as f:
            existing_data = json.load(f)
        contrib_count = existing_data.get('total', "1,143")
        days = existing_data.get('days', [])
        if not days:
            raise ValueError("contributions.json does not contain days data")
        print(f"Using existing contributions.json with {len(days)} days.")
    except Exception as fallback_error:
        print(f"Local fallback unavailable: {fallback_error}, using defaults.")
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
print("Saved contributions.json")

# ================= BALATRO JOKER SVG GENERATION =================
joker_svg = f"""<svg viewBox="0 0 600 250" width="100%" height="250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="holo-grad" cx="35%" cy="20%" r="85%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.18" />
      <stop offset="24%" stop-color="#f5c2e7" stop-opacity="0.16" />
      <stop offset="52%" stop-color="#7aa2f7" stop-opacity="0.12" />
      <stop offset="78%" stop-color="#73daca" stop-opacity="0.1" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </radialGradient>
    <linearGradient id="sweep-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="45%" stop-color="#f5c2e7" stop-opacity="0.28" />
      <stop offset="55%" stop-color="#7aa2f7" stop-opacity="0.2" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>
    <clipPath id="card-clip">
      <rect x="20" y="15" width="150" height="220" rx="12" ry="12" />
    </clipPath>
  </defs>

  <style>
    @keyframes card-float {{
      0%, 100% {{ transform: translateY(0px) rotate(-0.5deg); }}
      50% {{ transform: translateY(-4px) rotate(0.5deg); }}
    }}
    @keyframes foil-breathe {{
      0%, 100% {{ opacity: 0.24; transform: translate(-8px, -3px) scale(1); }}
      50% {{ opacity: 0.42; transform: translate(8px, 5px) scale(1.04); }}
    }}
    @keyframes light-sweep {{
      0% {{ opacity: 0; transform: translate(-92px, -20px); }}
      30% {{ opacity: 0.7; }}
      65% {{ opacity: 0.18; }}
      100% {{ opacity: 0; transform: translate(120px, 36px); }}
    }}
    @keyframes popup-bounce-loop {{
      0%, 75% {{ transform: translateY(0px) scale(0.8); opacity: 0; }}
      80% {{ transform: translateY(-20px) scale(1.1); opacity: 1; }}
      90% {{ transform: translateY(-35px) scale(1.0); opacity: 1; }}
      95%, 100% {{ transform: translateY(-45px) scale(0.9); opacity: 0; }}
    }}

    .joker-card-group {{
      transform-origin: 95px 125px;
      animation: card-float 6s ease-in-out infinite;
    }}
    .mult-pop {{
      fill: #f7768e;
      animation: popup-bounce-loop 8s infinite ease-out;
      transform-origin: 95px 125px;
      pointer-events: none;
    }}
    .foil-aurora {{
      animation: foil-breathe 8s ease-in-out infinite;
      transform-origin: 95px 125px;
      mix-blend-mode: screen;
    }}
    .sweep-overlay {{ animation: light-sweep 5.5s ease-in-out infinite; mix-blend-mode: screen; }}
    .font-retro {{ font-family: 'Fira Code', monospace; font-weight: 900; }}
    .font-sans-bold {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-weight: 700; }}
    .font-sans-regular {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; font-weight: 500; }}
  </style>

  <rect x="5" y="5" width="590" height="240" rx="12" ry="12" fill="#11111b" stroke="#313244" stroke-width="4" />
  <rect x="12" y="12" width="576" height="226" rx="8" ry="8" fill="#181825" />
  <path d="M 190 12 L 190 238" stroke="#313244" stroke-width="2" />

  <g class="joker-card-group">
    <rect x="20" y="15" width="150" height="220" rx="12" ry="12" fill="#11111b" stroke="#7aa2f7" stroke-width="3" />
    <rect x="22" y="17" width="146" height="216" rx="10" ry="10" fill="#1e1e2e" />
    <rect x="30" y="25" width="130" height="16" rx="3" fill="#313244" />
    <text x="95" y="37" fill="#cdd6f4" font-size="8.5" text-anchor="middle" class="font-retro" letter-spacing="0.5">IBNUARD JOKER</text>

    <!-- Monitor Card Art -->
    <rect x="30" y="48" width="130" height="85" rx="6" fill="#11111b" stroke="#f5c2e7" stroke-width="1.5" />
    <path d="M 80 112 L 110 112 L 115 122 L 75 122 Z" fill="#585b70" />
    <rect x="54" y="60" width="82" height="52" rx="4" fill="#1e1e2e" stroke="#fab387" stroke-width="1.5" />
    <rect x="57" y="63" width="76" height="38" rx="2" fill="#000000" />
    <text x="61" y="73" fill="#a6e3a1" font-size="7" class="font-retro">&gt;_ ibnuard</text>
    <text x="61" y="82" fill="#89b4fa" font-size="5.5" class="font-retro">stats: active</text>
    <text x="61" y="90" fill="#f5c2e7" font-size="5.5" class="font-retro">mindset: break</text>
    <text x="61" y="98" fill="#f9e2af" font-size="5.5" class="font-retro">ship: fast_dev</text>
    
    <!-- Modifiers -->
    <rect x="30" y="142" width="130" height="52" rx="6" fill="#11111b" stroke="#45475a" stroke-width="1" />
    <rect x="36" y="148" width="34" height="12" rx="3" fill="#f38ba8" />
    <text x="53" y="157" fill="#11111b" font-size="7" font-weight="900" text-anchor="middle" class="font-retro">+8 Mult</text>
    <text x="76" y="157" fill="#cdd6f4" font-size="7" class="font-sans-bold">low-level hacks</text>
    <rect x="36" y="165" width="34" height="12" rx="3" fill="#89b4fa" />
    <text x="53" y="174" fill="#11111b" font-size="7" font-weight="900" text-anchor="middle" class="font-retro">x1.5 Mult</text>
    <text x="76" y="174" fill="#cdd6f4" font-size="7" class="font-sans-bold">ship web/mobile</text>

    <text x="35" y="210" fill="#585b70" font-size="7.5" class="font-retro">#001</text>
    <text x="155" y="210" fill="#585b70" font-size="7.5" class="font-retro" text-anchor="end">v2.0.0</text>

    <g clip-path="url(#card-clip)">
      <ellipse cx="78" cy="86" rx="112" ry="168" fill="url(#holo-grad)" class="foil-aurora" />
      <path d="M -18 185 C 36 120 76 118 122 52 C 145 18 171 10 210 -12"
        fill="none" stroke="url(#sweep-grad)" stroke-width="34" stroke-linecap="round" class="sweep-overlay" />
    </g>

    <!-- Score popup -->
    <text x="95" y="120" font-size="16" class="font-retro mult-pop" text-anchor="middle" font-weight="900">+{contrib_count} Mult</text>
  </g>

  <!-- Right Panel Info -->
  <rect x="210" y="22" width="180" height="20" rx="3" fill="#313244" />
  <text x="220" y="36" fill="#f5c2e7" font-size="9" class="font-retro">SHOP INSPECT - JOKER INFO</text>

  <rect x="210" y="50" width="360" height="116" rx="6" fill="#11111b" stroke="#45475a" stroke-width="1.5" />
  <text x="225" y="70" fill="#f38ba8" font-size="10" class="font-retro" font-weight="900">LEGENDARY JOKER (HOLOGRAPHIC)</text>
  <text x="225" y="90" fill="#cdd6f4" font-size="9.5" class="font-sans-regular">Each commit adds <tspan fill="#f38ba8" font-weight="bold">+8 Mult</tspan> to score. Active daily streaks</text>
  <text x="225" y="106" fill="#cdd6f4" font-size="9.5" class="font-sans-regular">apply a <tspan fill="#89b4fa" font-weight="bold">x1.5 Mult</tspan>. Low-level assembly/C hacks have a</text>
  <text x="225" y="122" fill="#cdd6f4" font-size="9.5" class="font-sans-regular">1 in 4 chance to trigger <tspan fill="#f9e2af" font-weight="bold">+50 Mult</tspan>.</text>
  <rect x="225" y="136" width="330" height="1" fill="#313244" />
  <text x="225" y="152" fill="#a6adc8" font-size="9" class="font-sans-regular" font-style="italic">"build ──> break ──> understand ──> ship"</text>

  <g transform="translate(210, 178)">
    <rect x="0" y="0" width="112" height="46" rx="4" fill="#11111b" stroke="#313244" stroke-width="1" />
    <text x="10" y="14" fill="#a6adc8" font-size="8" class="font-retro">YEARLY MULT</text>
    <text x="10" y="34" fill="#f38ba8" font-size="16" class="font-retro">+{contrib_count}</text>
  </g>

  <g transform="translate(334, 178)">
    <rect x="0" y="0" width="112" height="46" rx="4" fill="#11111b" stroke="#313244" stroke-width="1" />
    <text x="10" y="14" fill="#a6adc8" font-size="8" class="font-retro">DAILY STREAK</text>
    <text x="10" y="34" fill="#a6e3a1" font-size="16" class="font-retro">10 days</text>
  </g>

  <g transform="translate(458, 178)">
    <rect x="0" y="0" width="112" height="46" rx="4" fill="#11111b" stroke="#f5c2e7" stroke-width="1" />
    <text x="56" y="27" fill="#f5c2e7" font-size="9" text-anchor="middle" class="font-retro" font-weight="900">README EMBED</text>
  </g>
</svg>
"""

for svg_path in ('balatro_preview.svg', 'balatro_joker.svg'):
    with open(svg_path, 'w') as f:
        f.write(joker_svg)
    print(f"Saved {svg_path}")

# ================= BOMBERMAN SVG GENERATION =================
if len(days) > 0:
    start_date = datetime.datetime.strptime(days[0]['date'], '%Y-%m-%d')
    start_row = (start_date.weekday() + 1) % 7
else:
    start_row = 0

col = 0
row = start_row
commit_blocks_xml = []
blast_points = [(7, 4), (17, 2), (28, 5), (39, 3), (48, 1)]
phase_timings = [(18, 25), (31, 38), (44, 51), (57, 64), (70, 78)]


def cell_center(c, r):
    return (20 + c * 12.5 + 5, 30 + r * 12.5 + 5)


def wave_keyframes(index, clear_start, clear_end):
    return f"""    @keyframes brick-wave-{index}-clear {{
      0%, {clear_start - 0.1:.1f}% {{ opacity: 1; }}
      {clear_start}%, 95% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
    .brick-wave-{index} {{
      animation: brick-wave-{index}-clear 16s infinite steps(1);
    }}

    @keyframes bomb-marker-{index}-blink {{
      0%, {clear_start - 4.1:.1f}% {{ opacity: 0; transform: scale(0.6); }}
      {clear_start - 4:.1f}%, {clear_start - 0.2:.1f}% {{ opacity: 1; transform: scale(1); }}
      {clear_start}%, 100% {{ opacity: 0; transform: scale(0.6); }}
    }}
    .bomb-marker-{index} {{
      animation: bomb-marker-{index}-blink 16s infinite steps(1);
    }}

    @keyframes blast-wave-{index}-pop {{
      0%, {clear_start - 0.1:.1f}% {{ opacity: 0; transform: scale(0.2); }}
      {clear_start}%, {clear_start + 2:.1f}% {{ opacity: 1; transform: scale(1); }}
      {clear_end}%, 100% {{ opacity: 0; transform: scale(1.15); }}
    }}
    .blast-wave-{index} {{
      animation: blast-wave-{index}-pop 16s infinite ease-out;
    }}"""


def blast_markup(index, col_index, row_index):
    cx, cy = cell_center(col_index, row_index)
    return f"""  <g class="blast-wave blast-wave-{index}" transform-origin="{cx}px {cy}px" filter="url(#neon-glow)">
    <rect x="{cx - 31.25:.1f}" y="{cy - 4:.1f}" width="62.5" height="8" rx="2" fill="#ff7043" />
    <rect x="{cx - 26.25:.1f}" y="{cy - 3:.1f}" width="52.5" height="6" rx="2" fill="#ffca28" />
    <rect x="{cx - 4:.1f}" y="{cy - 31.25:.1f}" width="8" height="62.5" rx="2" fill="#ff7043" />
    <rect x="{cx - 3:.1f}" y="{cy - 26.25:.1f}" width="6" height="52.5" rx="2" fill="#ffca28" />
  </g>"""


def bomb_markup(index, col_index, row_index):
    cx, cy = cell_center(col_index, row_index)
    return f"""  <g class="bomb-marker bomb-marker-{index}" transform-origin="{cx}px {cy}px">
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="#313244" />
    <path d="M {cx + 0.5:.1f} {cy - 4.5:.1f} L {cx + 2.5:.1f} {cy - 7.5:.1f}" stroke="#ffffff" stroke-width="1" />
    <circle cx="{cx + 3.5:.1f}" cy="{cy - 8.5:.1f}" r="1" fill="#f9e2af" />
  </g>"""


brick_wave_css = "\n".join(
    wave_keyframes(index, clear_start, clear_end)
    for index, (clear_start, clear_end) in enumerate(phase_timings)
)
blast_svg_content = "\n".join(
    blast_markup(index, col_index, row_index)
    for index, (col_index, row_index) in enumerate(blast_points)
)
bomb_svg_content = "\n".join(
    bomb_markup(index, col_index, row_index)
    for index, (col_index, row_index) in enumerate(blast_points)
)

route_points = [cell_center(c, r) for c, r in blast_points]
route_keyframes = [(0, route_points[0]), (12, route_points[0])]
for index in range(1, len(route_points)):
    route_keyframes.append((phase_timings[index][0] - 6, route_points[index]))
route_keyframes.extend([(88, route_points[-1]), (100, route_points[0])])
bomberman_route_css = "\n".join(
    f"      {percent}% {{ transform: translate({x:.1f}px, {y:.1f}px); }}"
    for percent, (x, y) in route_keyframes
)

# Build XML for green contribution cells only. The destroyable clay layer is
# drawn with a repeating SVG pattern so it stays light even while fully visible.
for i, day in enumerate(days):
    if col >= 53:
        break
    x = 20 + col * 12.5
    y = 30 + row * 12.5
    level = day['level']

    if level > 0:
        commit_blocks_xml.append(f'<use href="#mini-cube" x="{x}" y="{y}" class="lvl{level}" />')

    row += 1
    if row == 7:
        row = 0
        col += 1

brick_wave_rects = []
for phase in range(5):
    start_col = phase * 11
    col_count = min(11, 53 - start_col)
    if col_count <= 0:
        continue
    brick_wave_rects.append(
        f'<rect x="{20 + start_col * 12.5:.1f}" y="30" width="{col_count * 12.5:.1f}" height="87.5" fill="url(#brick-field)" class="brick-wave brick-wave-{phase}" />'
    )

cubes_svg_content = "\n    ".join(brick_wave_rects + commit_blocks_xml)

bomberman_svg = f"""<svg viewBox="0 0 820 180" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="screen-glow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="4" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="neon-glow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <pattern id="scanlines" width="100" height="3" patternUnits="userSpaceOnUse">
      <rect width="100" height="1" fill="#000000" opacity="0.25" />
    </pattern>
    <pattern id="grid-dots" width="12.5" height="12.5" patternUnits="userSpaceOnUse">
      <circle cx="6" cy="6" r="1.2" fill="#2d3139" opacity="0.8" />
    </pattern>
    <pattern id="brick-field" x="20" y="30" width="12.5" height="12.5" patternUnits="userSpaceOnUse">
      <rect x="0" y="0" width="10" height="10" rx="1" fill="#45475a" />
      <rect x="0.8" y="0.8" width="8.4" height="1.4" fill="#ffffff" opacity="0.2" />
      <rect x="0.8" y="0.8" width="1.4" height="8.4" fill="#ffffff" opacity="0.16" />
      <rect x="0.8" y="8.2" width="8.4" height="1" fill="#000000" opacity="0.36" />
      <rect x="8.2" y="0.8" width="1" height="8.4" fill="#000000" opacity="0.32" />
    </pattern>

    <!-- Hard block definition -->
    <g id="mini-cube">
      <rect x="0" y="0" width="10" height="10" rx="1.5" />
      <rect x="0.8" y="0.8" width="8.4" height="1.2" fill="#ffffff" opacity="0.4" />
      <rect x="0.8" y="0.8" width="1.2" height="8.4" fill="#ffffff" opacity="0.4" />
      <rect x="0.8" y="8.0" width="8.4" height="1.2" fill="#000000" opacity="0.5" />
      <rect x="8.0" y="0.8" width="1.2" height="8.4" fill="#000000" opacity="0.5" />
    </g>

  </defs>

  <style>
    .retro-font {{ font-family: 'Fira Code', monospace; font-weight: 900; }}

    .lvl1 {{ fill: #145e39; }}
    .lvl2 {{ fill: #1fb35a; }}
    .lvl3 {{ fill: #3ee27b; }}
    .lvl4 {{ fill: #9effc6; }}

    @keyframes bomberman-route {{
{bomberman_route_css}
    }}
    .bomberman-char {{
      animation: bomberman-route 16s infinite ease-in-out;
      transform-style: preserve-3d;
    }}

{brick_wave_css}

    @keyframes stat-pulse {{
      0%, 100% {{ fill: #9effc6; }}
      50% {{ fill: #3ee27b; }}
    }}
    .score-glowing {{ animation: stat-pulse 3s infinite; }}
  </style>

  <rect x="5" y="5" width="810" height="170" rx="12" ry="12" fill="#11111b" stroke="#313244" stroke-width="4" filter="url(#screen-glow)" />
  <rect x="12" y="12" width="796" height="156" rx="8" ry="8" fill="#181825" />
  <rect x="12" y="12" width="796" height="156" rx="8" ry="8" fill="url(#scanlines)" pointer-events="none" />

  <rect x="20" y="25" width="665" height="92" rx="4" fill="#0f0f15" stroke="#313244" stroke-width="1.5" />
  <rect x="20" y="25" width="665" height="92" rx="4" fill="url(#grid-dots)" />

  <text x="25" y="132" fill="#585b70" font-size="8" class="retro-font">Jul</text>
  <text x="120" y="132" fill="#585b70" font-size="8" class="retro-font">Sep</text>
  <text x="220" y="132" fill="#585b70" font-size="8" class="retro-font">Nov</text>
  <text x="320" y="132" fill="#585b70" font-size="8" class="retro-font">Jan</text>
  <text x="420" y="132" fill="#585b70" font-size="8" class="retro-font">Mar</text>
  <text x="520" y="132" fill="#585b70" font-size="8" class="retro-font">May</text>
  <text x="620" y="132" fill="#585b70" font-size="8" class="retro-font">Jul</text>

  <!-- Contribution Grid Blocks -->
  {cubes_svg_content}

  <!-- Bomb markers and blast waves sweep across the grid in five lightweight groups -->
{bomb_svg_content}
{blast_svg_content}

  <!-- walking Bomberman -->
  <g class="bomberman-char">
    <g class="glitch-monitor">
      <rect x="-3" y="-8" width="8" height="8" rx="2" fill="#ffffff" stroke="#11111b" stroke-width="0.8" />
      <circle cx="1" cy="-10" r="1.5" fill="#f38ba8" stroke="#11111b" stroke-width="0.5" />
      <ellipse cx="-0.5" cy="-4" rx="0.5" ry="1.5" fill="#000000" />
      <ellipse cx="2.5" cy="-4" rx="0.5" ry="1.5" fill="#000000" />
      <rect x="-2" y="0" width="6" height="5" fill="#89b4fa" stroke="#11111b" stroke-width="0.8" />
      <rect x="-2" y="3" width="6" height="1.5" fill="#f9e2af" />
    </g>
  </g>

  <!-- Stats HUD Display -->
  <g transform="translate(695, 25)">
    <rect x="0" y="0" width="105" height="42" rx="4" fill="#11111b" stroke="#313244" stroke-width="1.5" />
    <text x="10" y="14" fill="#a6adc8" font-size="7.5" class="retro-font">SCORE</text>
    <text x="10" y="32" fill="#fab387" font-size="14" class="retro-font score-glowing">002388</text>
  </g>

  <g transform="translate(695, 75)">
    <rect x="0" y="0" width="105" height="42" rx="4" fill="#11111b" stroke="#313244" stroke-width="1.5" />
    <text x="10" y="14" fill="#a6adc8" font-size="7.5" class="retro-font">YEARLY</text>
    <text x="10" y="32" fill="#a6e3a1" font-size="14" class="retro-font">{contrib_count}</text>
  </g>

  <circle cx="705" cy="136" r="3" fill="#f38ba8" />
  <circle cx="717" cy="136" r="3" fill="#f9e2af" />
  <circle cx="729" cy="136" r="3" fill="#a6e3a1" />
  <text x="795" y="140" fill="#585b70" font-size="8.5" class="retro-font" text-anchor="end">LVL 04</text>
</svg>
"""

for svg_path in ('bomberman_preview.svg', 'bomberman_contributions.svg'):
    with open(svg_path, 'w') as f:
        f.write(bomberman_svg)
    print(f"Saved {svg_path}")
print("All SVGs and JSON updated!")
