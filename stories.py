# stories.py — the world news of Thursday 26 November 2026, as reported
# that day (Daily Summary of World, Business Recorder, Reuters via
# BusinessWorld, NDTV, Moneycontrol). Every line below is baked in at
# build time; the program runs with no network.
#
# All poster copy is UPPER CASE because the 5x7 font covers capitals,
# digits and a little punctuation. Lines are hand-broken to fit their
# columns: lead headline lines fit 26 chars at scale 4, lead deck lines
# 53 chars at scale 2, panel headline lines 22 chars at scale 3, panel
# deck lines 38 chars at scale 2, strip lines 80 chars at scale 2.

MASTHEAD_TITLE = "THE WORLD IN ONE PICTURE"
MASTHEAD_DATE = "THURSDAY 26 NOVEMBER 2026"

# Lead story: the Gulf war widens on Thursday 26 November. A hostile
# aerial projectile strikes the Jazan refinery in Saudi Arabia, killing
# a Nepalese worker and halting operations; the Houthis claim strikes on
# the Saudi ports of Jeddah and Jazan. Iran's Revolutionary Guards say
# two oil tankers hit sea mines near Oman's Khasab while crossing the
# Strait of Hormuz. In Kuwait, shrapnel from intercepted Iranian drones
# kills two Italian technicians.
LEAD = {
    "kicker": "THE GULF WAR",
    "headline": [
        "HOUTHI STRIKE HITS",
        "SAUDI REFINERY;",
        "TANKERS HIT MINES",
        "AT HORMUZ",
    ],
    "deck": [
        "A hostile projectile kills one worker at the Jazan",
        "refinery and halts operations; Houthis claim strikes",
        "on Saudi ports Jeddah and Jazan. Two oil tankers hit",
        "sea mines near Oman's Khasab. Iranian drone shrapnel",
        "kills two Italian technicians in Kuwait.",
    ],
}

# Panel 1: Brazil and China denounce the new US tariff proposals, first
# reported on 25 November and answered on the 26th. China faces the
# highest capped rate, 20%, which could stack with other taxes to reach
# 45%; Brazil calls the levies on sugar and aircraft unacceptable.
PANEL_TARIFFS = {
    "kicker": "TRADE",
    "headline": [
        "BRAZIL, CHINA",
        "DENOUNCE NEW US",
        "TARIFF PROPOSALS",
    ],
    "deck": [
        "China faces the highest capped rate of",
        "20%, which could stack with other taxes",
        "to reach 45%. Brazil calls the levies",
        "on sugar and aircraft unacceptable.",
    ],
}

# Panel 2: eurozone leaders choose Spain's former central bank head
# Pablo Hernandez de Cos as the next European Central Bank president.
# Spain heads to snap parliamentary elections on Sunday 29 November
# after Prime Minister Pedro Sanchez calls the vote eight months early.
PANEL_EUROPE = {
    "kicker": "EUROPE",
    "headline": [
        "DE COS CHOSEN AS",
        "NEXT ECB CHIEF;",
        "SPAIN TO VOTE SUNDAY",
    ],
    "deck": [
        "Eurozone leaders pick Spain's Pablo",
        "Hernandez de Cos to head the European",
        "Central Bank. Sanchez calls a snap",
        "election for Sunday 29 November.",
    ],
}

# Panel 3: Kim Jong Un inspects atomic warheads and a bomb plant and
# says North Korea should deploy tactical nuclear weapons across more
# domains, calling its nuclear status absolutely inviolable — days after
# Pyongyang leaves Donald Trump's offer of a meeting unanswered.
PANEL_KOREA = {
    "kicker": "NORTH KOREA",
    "headline": [
        "KIM SHOWS OFF",
        "NUCLEAR WARHEADS",
        "AND SNUBS TRUMP",
    ],
    "deck": [
        "Kim Jong Un inspects atomic warheads",
        "and a bomb plant, vowing never to give",
        "up nuclear status. He accuses the US of",
        "enabling South Korea's submarines.",
    ],
}

# Panel 4: Russian forces strike residential buildings and an
# educational institution in Kharkiv overnight with ballistic missiles
# and 113 drones, killing at least three; NATO deploys an AWACS radar
# aircraft to monitor Polish airspace after Russian missiles crashed
# in Poland on 20 November.
PANEL_UKRAINE = {
    "kicker": "UKRAINE",
    "headline": [
        "RUSSIAN STRIKES",
        "KILL THREE IN",
        "KHARKIV AND KYIV",
    ],
    "deck": [
        "Ballistic missiles and 113 drones hit",
        "Ukraine overnight; Kyiv and Kharkiv are",
        "struck. NATO sends an AWACS radar plane",
        "to watch over Polish airspace.",
    ],
}

# Bottom strip: four more stories from the same day.
# - A fuel tanker overturns and catches fire on the Cairo ring road in
#   Giza, killing at least 31 people and injuring 21.
# - Organisers postpone the 100th Macy's Thanksgiving Day Parade in New
#   York from Thursday to Saturday as an East Coast storm brings winds
#   gusting to 97 km/h.
# - Myanmar's leader Min Aung Hlaing says the country will not comply
#   with parts of the ICJ genocide ruling against the Rohingya.
# - Guinea-Bissau's military government postpones elections from
#   6 December to 26 November 2028, extending its transition by two years.
STRIP_LABEL = "ALSO TODAY"
STRIP_LINES = [
    "CAIRO TANKER FIRE KILLS 31 - MACY'S PARADE POSTPONED BY STORM",
    "MYANMAR DEFIES ICJ RULING - GUINEA-BISSAU DELAYS VOTE TO 2028",
]
