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

# Save JSON Data file for the interactive HTML web app
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
    <filter id="card-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <filter id="neon-glow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
    <pattern id="scanlines" width="100" height="4" patternUnits="userSpaceOnUse">
      <rect width="100" height="1" fill="#000000" opacity="0.2" />
    </pattern>
    <linearGradient id="holo-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff0055" stop-opacity="0.35" />
      <stop offset="20%" stop-color="#ff00ff" stop-opacity="0.3" />
      <stop offset="40%" stop-color="#7f00ff" stop-opacity="0.3" />
      <stop offset="60%" stop-color="#00aaff" stop-opacity="0.3" />
      <stop offset="80%" stop-color="#00ff88" stop-opacity="0.3" />
      <stop offset="100%" stop-color="#ffcc00" stop-opacity="0.35" />
    </linearGradient>
    <linearGradient id="sweep-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.5" />
      <stop offset="55%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>
    <clipPath id="card-clip">
      <rect x="20" y="15" width="150" height="220" rx="12" ry="12" />
    </clipPath>
  </defs>

  <style>
    @keyframes card-float {{
      0%, 100% {{ transform: perspective(600px) rotateX(1.5deg) rotateY(-2deg) translateY(0px); }}
      50% {{ transform: perspective(600px) rotateX(-2deg) rotateY(2deg) translateY(-5px); }}
    }}
    @keyframes foil-rotate {{
      0% {{ transform: rotate(0deg); }}
      100% {{ transform: rotate(360deg); }}
    }}
    @keyframes light-sweep {{
      0% {{ transform: translate(-150px, -150px); }}
      100% {{ transform: translate(150px, 150px); }}
    }}
    @keyframes sparkle {{
      0%, 100% {{ opacity: 0.2; transform: scale(0.8); }}
      50% {{ opacity: 0.9; transform: scale(1.2); }}
    }}
    @keyframes monitor-glitch {{
      0%, 100% {{ opacity: 0.95; }}
      50% {{ opacity: 0.7; }}
    }}

    /* Balatro scoring sequence on an 8-second loop */
    @keyframes mult-tag-trigger {{
      0%, 12% {{ transform: scale(1); filter: none; }}
      15%, 22% {{ transform: scale(1.15); fill: #ff0055; filter: url(#neon-glow); }}
      25%, 100% {{ transform: scale(1); filter: none; }}
    }}
    @keyframes streak-tag-trigger {{
      0%, 22% {{ transform: scale(1); filter: none; }}
      25%, 32% {{ transform: scale(1.15); fill: #00ffff; filter: url(#neon-glow); }}
      35%, 100% {{ transform: scale(1); filter: none; }}
    }}
    @keyframes popup-bounce-loop {{
      0%, 35% {{ transform: translateY(0px) scale(0.8); opacity: 0; }}
      40% {{ transform: translateY(-25px) scale(1.1); opacity: 1; }}
      55% {{ transform: translateY(-40px) scale(1.0); opacity: 1; }}
      60%, 100% {{ transform: translateY(-55px) scale(0.9); opacity: 0; }}
    }}
    @keyframes card-glitch-seq {{
      0%, 34% {{ filter: none; }}
      35% {{ filter: hue-rotate(90deg) brightness(1.5); }}
      37% {{ filter: none; }}
      39% {{ filter: hue-rotate(-90deg) brightness(1.3); }}
      41%, 100% {{ filter: none; }}
    }}
    @keyframes button-glow {{
      0%, 100% {{ fill: #f5c2e7; filter: none; }}
      50% {{ fill: #f8cde7; filter: url(#neon-glow); }}
    }}

    .joker-card-group {{
      transform-style: preserve-3d;
      transform-origin: 95px 125px;
      animation: card-float 6s ease-in-out infinite, card-glitch-seq 8s infinite;
      cursor: pointer;
    }}
    .joker-card-group:hover {{
      animation-play-state: paused;
      transform: perspective(600px) rotateX(8deg) rotateY(-10deg) scale(1.05) translateY(-4px);
      filter: drop-shadow(0 10px 20px rgba(122, 162, 247, 0.4));
      transition: transform 0.3s ease;
    }}
    .mult-pop {{
      fill: #f38ba8;
      animation: popup-bounce-loop 8s infinite ease-out;
      transform-origin: 95px 125px;
      pointer-events: none;
    }}
    .buy-btn {{ animation: button-glow 3s infinite ease-in-out; }}
    .foil-overlay {{
      animation: foil-rotate 8s linear infinite;
      transform-origin: 95px 125px;
      mix-blend-mode: color-dodge;
    }}
    .sweep-overlay {{ animation: light-sweep 3s ease-in-out infinite; mix-blend-mode: overlay; }}
    .sparkle-star {{ animation: sparkle 2s infinite; transform-origin: center; }}
    .glitch-monitor {{ animation: monitor-glitch 4s infinite; }}
    .font-retro {{ font-family: 'Fira Code', 'Courier New', Courier, monospace; font-weight: 900; }}
    .font-sans-bold {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-weight: 700; }}
    .font-sans-regular {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-weight: 500; }}
    .buy-btn-text {{ pointer-events: none; }}
    
    .trigger-mult {{ animation: mult-tag-trigger 8s infinite ease-in-out; transform-origin: 53px 154px; }}
    .trigger-streak {{ animation: streak-tag-trigger 8s infinite ease-in-out; transform-origin: 53px 171px; }}
  </style>

  <rect x="5" y="5" width="590" height="240" rx="12" ry="12" fill="#11111b" stroke="#313244" stroke-width="4" />
  <rect x="12" y="12" width="576" height="226" rx="8" ry="8" fill="#181825" />
  <path d="M 190 12 L 190 238" stroke="#313244" stroke-width="2" />

  <g class="joker-card-group">
    <rect x="20" y="15" width="150" height="220" rx="12" ry="12" fill="#11111b" stroke="#7aa2f7" stroke-width="3" filter="url(#card-glow)" />
    <rect x="22" y="17" width="146" height="216" rx="10" ry="10" fill="#1e1e2e" />
    <rect x="30" y="25" width="130" height="16" rx="3" fill="#313244" />
    <text x="95" y="37" fill="#cdd6f4" font-size="8.5" text-anchor="middle" class="font-retro" letter-spacing="0.5">IBNUARD JOKER</text>

    <rect x="30" y="48" width="130" height="85" rx="6" fill="#11111b" stroke="#f5c2e7" stroke-width="1.5" />
    <rect x="31" y="49" width="128" height="83" rx="5" fill="url(#scanlines)" />

    <g class="glitch-monitor">
      <path d="M 80 112 L 110 112 L 115 122 L 75 122 Z" fill="#585b70" />
      <rect x="54" y="60" width="82" height="52" rx="4" fill="#1e1e2e" stroke="#fab387" stroke-width="1.5" />
      <rect x="57" y="63" width="76" height="38" rx="2" fill="#000000" />
      <text x="61" y="73" fill="#a6e3a1" font-size="7" class="font-retro">&gt;_ ibnuard</text>
      <text x="61" y="82" fill="#89b4fa" font-size="5.5" class="font-retro">stats: active</text>
      <text x="61" y="90" fill="#f5c2e7" font-size="5.5" class="font-retro">mindset: break</text>
      <text x="61" y="98" fill="#f9e2af" font-size="5.5" class="font-retro">ship: fast_dev</text>
      <rect x="107" y="68" width="3.5" height="6" fill="#a6e3a1">
        <animate attributeName="opacity" values="0.8;0.1;0.8" dur="0.8s" repeatCount="indefinite" />
      </rect>
    </g>

    <polygon points="38,62 39,64 42,64 40,65 41,68 38,66 35,68 36,65 34,64 37,64" fill="#f9e2af" class="sparkle-star" style="animation-delay: 0.2s;" />
    <polygon points="152,98 153,100 156,100 154,101 155,104 152,102 149,104 150,101 148,100 151,100" fill="#f9e2af" class="sparkle-star" style="animation-delay: 1.1s;" />

    <rect x="30" y="142" width="130" height="52" rx="6" fill="#11111b" stroke="#45475a" stroke-width="1" />
    <rect x="36" y="148" width="34" height="12" rx="3" fill="#f38ba8" class="trigger-mult" />
    <text x="53" y="157" fill="#11111b" font-size="7" font-weight="900" text-anchor="middle" class="font-retro">+8 Mult</text>
    <text x="76" y="157" fill="#cdd6f4" font-size="7" class="font-sans-bold">low-level hacks</text>
    <rect x="36" y="165" width="34" height="12" rx="3" fill="#89b4fa" class="trigger-streak" />
    <text x="53" y="174" fill="#11111b" font-size="7" font-weight="900" text-anchor="middle" class="font-retro">x1.5 Mult</text>
    <text x="76" y="174" fill="#cdd6f4" font-size="7" class="font-sans-bold">ship web/mobile</text>

    <text x="35" y="210" fill="#585b70" font-size="7.5" class="font-retro">#001</text>
    <text x="155" y="210" fill="#585b70" font-size="7.5" class="font-retro" text-anchor="end">v2.0.0</text>

    <g clip-path="url(#card-clip)">
      <rect x="-105" y="-75" width="400" height="400" fill="url(#holo-grad)" class="foil-overlay" />
      <rect x="-105" y="-75" width="400" height="400" fill="url(#sweep-grad)" class="sweep-overlay" />
    </g>

    <text x="95" y="120" font-size="16" class="font-retro mult-pop" text-anchor="middle" font-weight="900">+{contrib_count} Mult</text>
  </g>

  <rect x="210" y="22" width="180" height="20" rx="3" fill="#313244" />
  <text x="220" y="36" fill="#f5c2e7" font-size="9" class="font-retro">SHOP INSPECT - JOKER INFO</text>

  <rect x="210" y="50" width="360" height="116" rx="6" fill="#11111b" stroke="#45475a" stroke-width="1.5" />
  <text x="225" y="70" fill="#f38ba8" font-size="10" class="font-retro" font-weight="900">LEGENDARY JOKER (HOLOGRAPHIC)</text>
  <text x="225" y="90" fill="#cdd6f4" font-size="9.5" class="font-sans-regular">Each commit adds <tspan fill="#f38ba8" font-weight="bold">+8 Mult</tspan> to score. Active daily streaks</text>
  <text x="225" y="106" fill="#cdd6f4" font-size="9.5" class="font-sans-regular">apply a <tspan fill="#89b4fa" font-weight="bold">x1.5 Mult</tspan>. Low-level assembly/C hacks have a</text>
  <text x="225" y="122" fill="#cdd6f4" font-size="9.5" class="font-sans-regular">1 in 4 chance to trigger <tspan fill="#f9e2af" font-weight="bold">+50 Mult</tspan> and compile with zero errors.</text>
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
    <rect x="0" y="0" width="112" height="46" rx="4" fill="#f5c2e7" stroke="#11111b" stroke-width="1" class="buy-btn" />
    <text x="56" y="27" fill="#11111b" font-size="9" text-anchor="middle" class="font-retro buy-btn-text" font-weight="900">UPGRADE CARD</text>
  </g>
</svg>
"""

with open('balatro_joker.svg', 'w') as f:
    f.write(joker_svg)
print("Saved balatro_joker.svg")

# ================= BOMBERMAN SVG GENERATION =================
if len(days) > 0:
    start_date = datetime.datetime.strptime(days[0]['date'], '%Y-%m-%d')
    start_row = (start_date.weekday() + 1) % 7
else:
    start_row = 0

col = 0
row = start_row
cubes_xml = []

blast1_col, blast1_row = 44, 3
blast1_cells = []
for c in range(blast1_col - 2, blast1_col + 3):
    blast1_cells.append((c, blast1_row))
for r in range(blast1_row - 2, blast1_row + 3):
    blast1_cells.append((blast1_col, r))

blast2_col, blast2_row = 48, 1
blast2_cells = []
for c in range(blast2_col - 2, blast2_col + 3):
    blast2_cells.append((c, blast2_row))
for r in range(blast2_row - 2, blast2_row + 3):
    blast2_cells.append((blast2_col, r))

for i, day in enumerate(days):
    if col >= 53:
        break
    x = 20 + col * 12.5
    y = 30 + row * 12.5
    level = day['level']
    cell = (col, row)
    
    in_b1 = cell in blast1_cells
    in_b2 = cell in blast2_cells

    if level > 0:
        if in_b1 and in_b2:
            cubes_xml.append(f'<use href="#mini-cube" x="{x}" y="{y}" class="lvl{level} hard-block-hit-both" />')
        elif in_b1:
            cubes_xml.append(f'<use href="#mini-cube" x="{x}" y="{y}" class="lvl{level} hard-block-hit-1" />')
        elif in_b2:
            cubes_xml.append(f'<use href="#mini-cube" x="{x}" y="{y}" class="lvl{level} hard-block-hit-2" />')
        else:
            cubes_xml.append(f'<use href="#mini-cube" x="{x}" y="{y}" class="lvl{level}" />')
    else:
        if in_b1 and in_b2:
            cubes_xml.append(f'<use href="#brick-cube" x="{x}" y="{y}" class="destructible-brick-both" />')
        elif in_b1:
            cubes_xml.append(f'<use href="#brick-cube" x="{x}" y="{y}" class="destructible-brick-1" />')
        elif in_b2:
            cubes_xml.append(f'<use href="#brick-cube" x="{x}" y="{y}" class="destructible-brick-2" />')
        else:
            cubes_xml.append(f'<use href="#brick-cube" x="{x}" y="{y}" fill="#242831" />')

    row += 1
    if row == 7:
        row = 0
        col += 1

cubes_svg_content = "\n    ".join(cubes_xml)

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

    <g id="mini-cube">
      <rect x="0" y="0" width="10" height="10" rx="1.5" />
      <rect x="0.8" y="0.8" width="8.4" height="1.2" fill="#ffffff" opacity="0.4" />
      <rect x="0.8" y="0.8" width="1.2" height="8.4" fill="#ffffff" opacity="0.4" />
      <rect x="0.8" y="8.0" width="8.4" height="1.2" fill="#000000" opacity="0.5" />
      <rect x="8.0" y="0.8" width="1.2" height="8.4" fill="#000000" opacity="0.5" />
    </g>

    <g id="brick-cube">
      <rect x="0" y="0" width="10" height="10" rx="1" />
      <rect x="1" y="1" width="8" height="3" fill="#ffffff" opacity="0.15" />
      <line x1="5" y1="1" x2="5" y2="4" stroke="#000000" stroke-width="0.8" opacity="0.2" />
      <line x1="3" y1="5" x2="3" y2="9" stroke="#000000" stroke-width="0.8" opacity="0.2" />
      <line x1="7" y1="5" x2="7" y2="9" stroke="#000000" stroke-width="0.8" opacity="0.2" />
      <line x1="0" y1="4.5" x2="10" y2="4.5" stroke="#000000" stroke-width="0.8" opacity="0.3" />
      <rect x="0.5" y="0.5" width="9" height="1" fill="#ffffff" opacity="0.25" />
      <rect x="0.5" y="0.5" width="1" height="9" fill="#ffffff" opacity="0.25" />
      <rect x="0.5" y="8.5" width="9" height="1" fill="#000000" opacity="0.4" />
      <rect x="8.5" y="0.5" width="1" height="9" fill="#000000" opacity="0.4" />
    </g>
  </defs>

  <style>
    .retro-font {{ font-family: 'Fira Code', 'Courier New', Courier, monospace; font-weight: 900; }}

    .lvl1 {{ fill: #145e39; }}
    .lvl2 {{ fill: #1fb35a; }}
    .lvl3 {{ fill: #3ee27b; }}
    .lvl4 {{ fill: #9effc6; }}

    @keyframes bomberman-route {{
      0% {{ transform: translate(495px, 66px); }}
      10% {{ transform: translate(495px, 66px); }}
      20% {{ transform: translate(557px, 66px); }}
      23% {{ transform: translate(557px, 66px); }}
      30% {{ transform: translate(520px, 66px); }}
      35% {{ transform: translate(520px, 66px); }}
      45% {{ transform: translate(545px, 41px); }}
      55% {{ transform: translate(607px, 41px); }}
      58% {{ transform: translate(607px, 41px); }}
      65% {{ transform: translate(607px, 91px); }}
      70% {{ transform: translate(607px, 91px); }}
      80% {{ transform: translate(495px, 66px); }}
      100% {{ transform: translate(495px, 66px); }}
    }}
    .bomberman-char {{
      animation: bomberman-route 16s infinite ease-in-out;
      transform-style: preserve-3d;
    }}

    @keyframes bomb1-glow {{
      0%, 22% {{ opacity: 0; transform: scale(0); }}
      23% {{ opacity: 1; transform: scale(1); fill: #313244; }}
      27%, 31% {{ fill: #f38ba8; transform: scale(1.15); filter: url(#neon-glow); }}
      25%, 29% {{ fill: #313244; transform: scale(1); filter: none; }}
      34.9% {{ opacity: 1; }}
      35%, 100% {{ opacity: 0; transform: scale(0); }}
    }}
    .bomb-1 {{
      animation: bomb1-glow 16s infinite steps(1);
      transform-origin: 576.5px 72.5px;
    }}

    @keyframes bomb2-glow {{
      0%, 57% {{ opacity: 0; transform: scale(0); }}
      58% {{ opacity: 1; transform: scale(1); fill: #313244; }}
      62%, 66% {{ fill: #f38ba8; transform: scale(1.15); filter: url(#neon-glow); }}
      60%, 64% {{ fill: #313244; transform: scale(1); filter: none; }}
      69.9% {{ opacity: 1; }}
      70%, 100% {{ opacity: 0; transform: scale(0); }}
    }}
    .bomb-2 {{
      animation: bomb2-glow 16s infinite steps(1);
      transform-origin: 626.5px 47.5px;
    }}

    @keyframes blast1-expand {{
      0%, 34.9% {{ opacity: 0; transform: scale(0.1); }}
      35%, 42% {{ opacity: 1; transform: scale(1); }}
      43%, 100% {{ opacity: 0; }}
    }}
    .b1-horiz, .b1-vert {{
      animation: blast1-expand 16s infinite ease-out;
      transform-origin: 576.5px 72.5px;
    }}

    @keyframes blast2-expand {{
      0%, 69.9% {{ opacity: 0; transform: scale(0.1); }}
      70%, 77% {{ opacity: 1; transform: scale(1); }}
      78%, 100% {{ opacity: 0; }}
    }}
    .b2-horiz, .b2-vert {{
      animation: blast2-expand 16s infinite ease-out;
      transform-origin: 626.5px 47.5px;
    }}

    @keyframes brick1-clear {{
      0%, 34.9% {{ opacity: 1; }}
      35%, 37% {{ fill: #ffffff; opacity: 1; }}
      42% {{ opacity: 0; }}
      95% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
    .destructible-brick-1 {{
      animation: brick1-clear 16s infinite steps(1);
    }}

    @keyframes brick2-clear {{
      0%, 69.9% {{ opacity: 1; }}
      70%, 72% {{ fill: #ffffff; opacity: 1; }}
      77% {{ opacity: 0; }}
      95% {{ opacity: 0; }}
      100% {{ opacity: 1; }}
    }}
    .destructible-brick-2 {{
      animation: brick2-clear 16s infinite steps(1);
    }}

    .destructible-brick-both {{
      animation: brick1-clear 16s infinite steps(1);
    }}

    @keyframes hit1-flash {{
      0%, 34.9% {{ filter: none; }}
      35%, 38% {{ filter: brightness(2.5); }}
      39%, 100% {{ filter: none; }}
    }}
    .hard-block-hit-1 {{
      animation: hit1-flash 16s infinite;
    }}

    @keyframes hit2-flash {{
      0%, 69.9% {{ filter: none; }}
      70%, 73% {{ filter: brightness(2.5); }}
      74%, 100% {{ filter: none; }}
    }}
    .hard-block-hit-2 {{
      animation: hit2-flash 16s infinite;
    }}

    @keyframes hit-both-flash {{
      0%, 34.9% {{ filter: none; }}
      35%, 38% {{ filter: brightness(2.5); }}
      39%, 69.9% {{ filter: none; }}
      70%, 73% {{ filter: brightness(2.5); }}
      74%, 100% {{ filter: none; }}
    }}
    .hard-block-hit-both {{
      animation: hit-both-flash 16s infinite;
    }}

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

  {cubes_svg_content}

  <g class="bomb-1">
    <circle cx="575.0" cy="72.5" r="4.5" />
    <path d="M 575.5 68 L 577.5 65" stroke="#ffffff" stroke-width="1" />
    <circle cx="578.5" cy="64" r="1" fill="#f9e2af" />
  </g>

  <rect x="545.0" y="68.5" width="62.5" height="8" rx="2" fill="#ff7043" opacity="0" class="b1-horiz" />
  <rect x="550.0" y="69.5" width="52.5" height="6" rx="2" fill="#ffca28" opacity="0" class="b1-horiz" />
  <rect x="571.0" y="42.5" width="8" height="62.5" rx="2" fill="#ff7043" opacity="0" class="b1-vert" />
  <rect x="572.0" y="47.5" width="6" height="52.5" rx="2" fill="#ffca28" opacity="0" class="b1-vert" />

  <g class="bomb-2">
    <circle cx="625.0" cy="47.5" r="4.5" />
    <path d="M 625.5 43 L 627.5 40" stroke="#ffffff" stroke-width="1" />
    <circle cx="628.5" cy="39" r="1" fill="#f9e2af" />
  </g>

  <rect x="595.0" y="43.5" width="62.5" height="8" rx="2" fill="#ff7043" opacity="0" class="b2-horiz" />
  <rect x="600.0" y="44.5" width="52.5" height="6" rx="2" fill="#ffca28" opacity="0" class="b2-horiz" />
  <rect x="621.0" y="30.0" width="8" height="50" rx="2" fill="#ff7043" opacity="0" class="b2-vert" />
  <rect x="622.0" y="35.0" width="6" height="40" rx="2" fill="#ffca28" opacity="0" class="b2-vert" />

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

  <g transform="translate(695, 25)">
    <rect x="0" y="0" width="105" height="42" rx="4" fill="#11111b" stroke="#313244" stroke-width="1.5" />
    <text x="10" y="14" fill="#a6adc8" font-size="7.5" class="retro-font">SCORE</text>
    <text x="10" y="32" fill="#fab387" font-size="14" class="retro-font score-glowing">002388</text>
  </g>

  <g transform="translate(695, 75)">
    <rect x="0" y="0" width="105" height="42" rx="4" fill="#11111b" stroke="#313244" stroke-width="1.5" />
    <text x="10" y="14" fill="#a6adc8" font-size="7.5" class="retro-font">YEARLY</text>
    <text x="10" y="32" fill="#a6e3a1" font-size="14" class="retro-font">{contrib_count.zfill(6)}</text>
  </g>

  <circle cx="705" cy="136" r="3" fill="#f38ba8" />
  <circle cx="717" cy="136" r="3" fill="#f9e2af" />
  <circle cx="729" cy="136" r="3" fill="#a6e3a1" />
  <text x="795" y="140" fill="#585b70" font-size="8.5" class="retro-font" text-anchor="end">LVL 04</text>
</svg>
"""

with open('bomberman_contributions.svg', 'w') as f:
    f.write(bomberman_svg)
print("Saved bomberman_contributions.svg")
print("All SVGs generated successfully!")
