class Card:
    def __init__(self, title, categories):
        self.title = title
        # categories: dict of {stat_name: value}
        self.categories = categories

    def __str__(self):
        stats = ", ".join(f"{k}: {v}" for k, v in self.categories.items())
        return f"{self.title} [{stats}]"


class CardPack:
    def __init__(self, name, stat_names, stat_units=None, lower_is_better=None):
        self.name = name
        self.stat_names = stat_names        # ordered list of 5 stat names
        self.stat_units = stat_units or {}  # optional display units per stat
        self.lower_is_better = set(lower_is_better or [])  # stats where lowest value wins
        self.cards = []

    def add_card(self, title, values):
        """Add a card.  values must be a list/tuple of 5 numbers in stat order."""
        card = Card(title, dict(zip(self.stat_names, values)))
        self.cards.append(card)

    def __len__(self):
        return len(self.cards)


# ---------------------------------------------------------------------------
# 🐾 Animals Pack  (stats: Speed km/h, Strength kg, Lifespan yrs, Size cm, Intelligence 1-10)
# ---------------------------------------------------------------------------
animals_pack = CardPack(
    name="Animals",
    stat_names=["Speed", "Strength", "Lifespan", "Size", "Intelligence"],
    stat_units={"Speed": "km/h", "Strength": "kg", "Lifespan": "yrs", "Size": "cm"},
)

_animals_data = [
    # (name,              speed, strength, lifespan, size,  intelligence)
    ("Cheetah",            120,    65,      12,    140,    5),
    ("Lion",                80,   250,      15,    210,    6),
    ("African Elephant",    40,  5000,      70,    700,    9),
    ("Blue Whale",          46, 150000,     90,   3000,    7),
    ("Peregrine Falcon",   389,     1,      15,     50,    5),
    ("Grizzly Bear",        56,   500,      25,    250,    5),
    ("Tiger",               65,   300,      20,    280,    6),
    ("Dolphin",             60,   250,      45,    250,    9),
    ("Wolf",                65,    75,      13,    160,    7),
    ("Gorilla",             40,   800,      35,    175,    8),
    ("Komodo Dragon",       20,    70,      30,    300,    4),
    ("Snow Leopard",        64,    55,      16,    155,    6),
    ("Polar Bear",          40,   800,      25,    300,    5),
    ("Chimpanzee",          40,   120,      45,    160,    9),
    ("Crocodile",           29,   900,      70,    600,    4),
    ("Jaguar",              80,   135,      15,    185,    6),
    ("Ostrich",             70,   130,      40,    270,    3),
    ("Hippopotamus",        30,  2500,      40,    430,    4),
    ("Manta Ray",           35,   200,      50,    700,    5),
    ("Brown Rat",           13,     0.3,     3,     25,    6),
    ("Octopus",              8,     5,       3,    100,    9),
    ("Orca",                56,  3000,      90,    800,    9),
    ("Bald Eagle",          48,     5,      28,    100,    5),
    ("Anaconda",             8,   130,      30,    550,    3),
    ("Emperor Penguin",     15,    40,      20,    115,    4),
    ("Kangaroo",            70,    85,      23,    200,    4),
    ("Platypus",            10,     2,      17,     55,    6),
    ("Giraffe",             60,   750,      25,    580,    4),
    ("Rhinoceros",          50,  2300,      40,    400,    4),
    ("Mantis Shrimp",       23,    10,       6,     15,    5),
    ("Hummingbird",         90,     0.003,    5,     10,    4),
    ("Leopard",             58,    90,      21,    160,    6),
    ("Wolverine",           30,    20,      13,     80,    5),
    ("Arctic Fox",          50,     7,      14,     65,    6),
    ("Meerkat",             12,     1,      12,     35,    7),
    ("Golden Eagle",        48,    10,      30,     95,    6),
    ("Coyote",              69,    20,      14,    130,    6),
    ("Giant Panda",         32,   130,      20,    180,    5),
    ("Saltwater Crocodile", 29,  1000,      70,    680,    4),
    ("Black Mamba",          20,     1.5,    11,    300,    3),
]

for _name, _spd, _str, _life, _size, _intel in _animals_data:
    animals_pack.add_card(_name, [_spd, _str, _life, _size, _intel])


# ---------------------------------------------------------------------------
# 🎬 Movies Pack  (stats: Budget $M, Box Office $M, Runtime min, IMDb rating, Year)
# ---------------------------------------------------------------------------
movies_pack = CardPack(
    name="Movies",
    stat_names=["Budget", "Box Office", "Runtime", "IMDb", "Year"],
    stat_units={"Budget": "$M", "Box Office": "$M", "Runtime": "min"},
)

_movies_data = [
    # (title,                       budget, box_office, runtime, imdb, year)
    ("Avatar",                         237,   2923,       162,  7.8, 2009),
    ("Titanic",                        200,   2264,       194,  7.9, 1997),
    ("Avengers: Endgame",              356,   2799,       181,  8.4, 2019),
    ("Star Wars: The Force Awakens",   245,   2068,       138,  7.8, 2015),
    ("Avengers: Infinity War",         325,   2048,       149,  8.4, 2018),
    ("Jurassic World",                 150,   1672,       124,  7.0, 2015),
    ("The Lion King (2019)",           260,   1656,       118,  6.9, 2019),
    ("The Avengers",                   220,   1519,       143,  8.0, 2012),
    ("Furious 7",                      190,   1516,       137,  7.1, 2015),
    ("Frozen II",                      150,   1450,       103,  6.8, 2019),
    ("Avengers: Age of Ultron",        365,   1402,       141,  7.3, 2015),
    ("Black Panther",                  200,   1347,       134,  7.3, 2018),
    ("Harry Potter: Deathly Hallows 2",125,   1342,       130,  8.1, 2011),
    ("Star Wars: The Last Jedi",       200,   1332,       152,  7.0, 2017),
    ("Jurassic World: Fallen Kingdom", 170,   1310,       128,  6.2, 2018),
    ("Frozen",                         150,   1281,       102,  7.4, 2013),
    ("Beauty and the Beast (2017)",    160,   1264,       129,  7.1, 2017),
    ("Incredibles 2",                  200,   1243,       118,  7.6, 2018),
    ("The Fate of the Furious",        250,   1236,       136,  6.6, 2017),
    ("Iron Man 3",                     200,   1215,       130,  7.1, 2013),
    ("Minions",                         74,   1159,        91,  6.4, 2015),
    ("Captain America: Civil War",     250,   1153,       147,  7.8, 2016),
    ("Aquaman",                        160,   1148,       143,  6.9, 2018),
    ("Spider-Man: Far From Home",      160,   1132,       129,  7.4, 2019),
    ("Captain Marvel",                 152,   1128,       124,  6.8, 2019),
    ("Transformers: Dark of the Moon", 195,   1124,       154,  6.3, 2011),
    ("The Dark Knight Rises",          250,   1085,       164,  8.4, 2012),
    ("Toy Story 4",                    200,   1073,       100,  7.8, 2019),
    ("Toy Story 3",                    200,   1067,       103,  8.3, 2010),
    ("Pirates of the Caribbean: DMC",  225,   1066,       151,  7.3, 2006),
    ("Rogue One: A Star Wars Story",   200,   1056,       133,  7.8, 2016),
    ("Aladdin (2019)",                 183,   1051,       128,  6.9, 2019),
    ("The Dark Knight",                185,   1005,       152,  9.0, 2008),
    ("Zootopia",                       150,    1024,       108,  8.0, 2016),
    ("The Hunger Games: Mockingjay P2", 160,   658,       137,  6.6, 2015),
    ("Doctor Strange",                 165,    677,       115,  7.5, 2016),
    ("Guardians of the Galaxy",        232,    774,       121,  8.0, 2014),
    ("Thor: Ragnarok",                 180,    854,       130,  7.9, 2017),
    ("Shrek 2",                        150,    919,        93,  7.2, 2004),
    ("Finding Nemo",                    94,    940,       100,  8.1, 2003),
]

for _t, _bud, _bo, _rt, _imdb, _yr in _movies_data:
    movies_pack.add_card(_t, [_bud, _bo, _rt, _imdb, _yr])


# ---------------------------------------------------------------------------
# 🌍 Countries Pack  (stats: Population M, Area km², GDP $B, Life Expectancy yrs, Languages)
# ---------------------------------------------------------------------------
countries_pack = CardPack(
    name="Countries",
    stat_names=["Population", "Area", "GDP", "Life Expectancy", "Languages"],
    stat_units={"Population": "M", "Area": "km²", "GDP": "$B", "Life Expectancy": "yrs"},
)

_countries_data = [
    # (name,                  pop_M, area_km2,    gdp_B,  life_exp, languages)
    ("China",                 1412,  9596960,    17734,    77.4,    1),
    ("India",                 1380,  3287263,     3385,    69.7,   22),
    ("United States",          331,  9833517,    25464,    78.9,    1),
    ("Indonesia",              273,  1904569,     1391,    71.7,    2),
    ("Pakistan",               225,   881913,      348,    67.3,    6),
    ("Brazil",                 213,  8515767,     1920,    75.9,    1),
    ("Nigeria",                211,   923768,      477,    55.2,   10),
    ("Bangladesh",             169,   147570,      460,    72.6,    1),
    ("Russia",                 146, 17098242,     1779,    72.4,   35),
    ("Ethiopia",               117,  1104300,      127,    66.2,   90),
    ("Mexico",                 127,  1964375,     1294,    75.1,    1),
    ("Japan",                  126,   377975,     4231,    84.3,    1),
    ("Philippines",            110,   300000,      412,    71.4,    2),
    ("Egypt",                  102,  1002450,      477,    72.0,    1),
    ("DR Congo",                92,  2344858,       60,    60.7,    4),
    ("Tanzania",                60,   945087,       74,    65.5,  126),
    ("Kenya",                   53,   580367,      116,    66.7,   68),
    ("South Africa",            60,  1219090,      419,    64.1,   11),
    ("Germany",                 83,   357114,     4072,    80.6,    1),
    ("United Kingdom",          67,   243610,     3131,    80.4,    2),
    ("France",                  67,   551695,     2937,    82.7,    1),
    ("Italy",                   60,   301340,     2058,    83.5,    1),
    ("Canada",                  38,  9984670,     1988,    82.3,    2),
    ("South Korea",             52,    99720,     1799,    83.5,    1),
    ("Australia",               25,  7692024,     1693,    83.4,    1),
    ("Spain",                   47,   505990,     1397,    83.6,    4),
    ("Argentina",               45,  2780400,      641,    76.7,    1),
    ("Algeria",                 44,  2381741,      191,    77.0,    2),
    ("Saudi Arabia",            34,  2149690,     1061,    75.5,    1),
    ("Turkey",                  84,   783562,      906,    77.7,    1),
    ("Poland",                  38,   312696,      679,    77.4,    1),
    ("Netherlands",             17,    41543,     1012,    81.8,    1),
    ("Switzerland",              8,    41285,      807,    83.8,    4),
    ("Sweden",                  10,   450295,      585,    82.4,    1),
    ("Norway",                   5,   323802,      579,    83.2,    2),
    ("Singapore",                6,      733,      397,    83.2,    4),
    ("New Zealand",              5,   268021,      249,    82.3,    3),
    ("Israel",                   9,    20770,      521,    82.8,    2),
    ("UAE",                     10,    83600,      499,    78.0,    2),
    ("Portugal",                10,    92212,      254,    81.1,    1),
]

for _n, _pop, _area, _gdp, _life, _lang in _countries_data:
    countries_pack.add_card(_n, [_pop, _area, _gdp, _life, _lang])


# ---------------------------------------------------------------------------
# 💻 Technology Pack  (stats: Revenue $B, Employees K, Founded yr, Market Cap $B, Patents K)
# ---------------------------------------------------------------------------
technology_pack = CardPack(
    name="Technology",
    stat_names=["Revenue", "Employees", "Founded", "Market Cap", "Patents"],
    stat_units={"Revenue": "$B", "Employees": "K", "Market Cap": "$B", "Patents": "K"},
    lower_is_better=["Founded"],
)

_tech_data = [
    # (company,             rev_B, emp_K, founded, mktcap_B, patents_K)
    ("Apple",               394.3, 164.0,   1976,    2900.0,  75.4),
    ("Microsoft",           198.3, 221.0,   1975,    2600.0,  60.0),
    ("Alphabet (Google)",   282.8, 182.0,   1998,    1700.0,  50.0),
    ("Amazon",              514.0, 1541.0,  1994,    1300.0,  30.0),
    ("Meta (Facebook)",     116.6,  87.3,   2004,     700.0,  12.0),
    ("Tesla",                81.5, 127.9,   2003,     600.0,  10.0),
    ("NVIDIA",               60.9,  29.6,   1993,    1800.0,  10.0),
    ("Samsung Electronics", 244.0, 270.0,   1969,     440.0, 200.0),
    ("TSMC",                  76.1,  73.0,   1987,     500.0,  40.0),
    ("ASML",                  27.6,  40.0,   1984,     300.0,   8.0),
    ("Intel",                 63.1, 124.8,   1968,     200.0, 100.0),
    ("IBM",                   60.5, 288.3,   1911,     130.0, 110.0),
    ("Oracle",                50.0, 143.0,   1977,     340.0,  20.0),
    ("Salesforce",            31.4,  79.4,   1999,     200.0,   5.0),
    ("Adobe",                 17.6,  29.2,   1982,     250.0,   7.0),
    ("Netflix",               31.6,  12.1,   1997,     200.0,   1.5),
    ("Uber",                  31.9,  32.2,   2009,      60.0,   2.0),
    ("Airbnb",                 8.4,   6.1,   2008,      80.0,   0.5),
    ("Spotify",               13.2,  9.0,   2006,      35.0,   0.8),
    ("Twitter/X",              5.1,   2.0,   2006,      20.0,   1.0),
    ("Qualcomm",              35.8,  51.0,   1985,     170.0,  15.0),
    ("Broadcom",              33.2,  20.0,   1991,     400.0,  25.0),
    ("SAP",                   32.0,  99.5,   1972,     180.0,  12.0),
    ("Sony",                  88.7, 108.9,   1946,     120.0,  50.0),
    ("Tencent",               85.0,  85.0,   1998,     400.0,  60.0),
    ("Alibaba",               126.5, 225.0,  1999,     230.0,  30.0),
    ("Baidu",                  19.5,  45.0,   2000,      40.0,  10.0),
    ("Xiaomi",                 37.0, 35.3,   2010,      50.0,  15.0),
    ("Huawei",                92.0, 207.0,   1987,       0.0, 110.0),
    ("LG Electronics",        63.0,  74.0,   1958,      16.0,  40.0),
    ("Cisco",                 51.6,  83.3,   1984,     210.0,  25.0),
    ("HP Inc.",                63.0,  51.0,   1939,      30.0,  15.0),
    ("Dell Technologies",     101.6, 133.0,  1984,      50.0,  10.0),
    ("PayPal",                 27.5,  30.9,   1998,      70.0,   3.0),
    ("Square/Block",           17.5,  14.0,   2009,      40.0,   2.0),
    ("Shopify",                 5.6,  10.0,   2006,      70.0,   1.0),
    ("Zoom",                    4.4,   8.4,   2011,      20.0,   0.5),
    ("Palantir",                2.2,   3.7,   2003,      30.0,   0.5),
    ("Snowflake",               2.1,   5.9,   2012,      50.0,   0.5),
    ("SpaceX",                  9.0,  13.0,   2002,     180.0,   5.0),
]

for _c, _rev, _emp, _fnd, _mkt, _pat in _tech_data:
    technology_pack.add_card(_c, [_rev, _emp, _fnd, _mkt, _pat])


# ---------------------------------------------------------------------------
# 🏎️ Super Cars Pack  (stats: Top Speed km/h, 0-100 sec, Power hp, Price $M, Year)
# ---------------------------------------------------------------------------
supercars_pack = CardPack(
    name="Super Cars",
    stat_names=["Top Speed", "0-100", "Power", "Price", "Year"],
    stat_units={"Top Speed": "km/h", "0-100": "s", "Power": "hp", "Price": "$M"},
    lower_is_better=["0-100"],
)

_supercars_data = [
    # (name,                               top_speed, 0-100, power,  price,  year)
    ("Bugatti Chiron Super Sport 300+",         490,   2.4,  1578,   3.90, 2021),
    ("Koenigsegg Jesko Absolut",                531,   2.5,  1600,   3.00, 2022),
    ("Hennessey Venom F5",                      484,   2.6,  1817,   2.10, 2021),
    ("SSC Tuatara",                             455,   2.5,  1750,   1.90, 2020),
    ("Bugatti Veyron Super Sport",              431,   2.4,  1200,   2.60, 2010),
    ("Koenigsegg Agera RS",                     447,   2.8,  1160,   2.50, 2017),
    ("Rimac Nevera",                            412,   1.97, 1914,   2.40, 2022),
    ("Aston Martin Valkyrie",                   402,   2.5,  1155,   3.50, 2022),
    ("McLaren F1",                              386,   3.2,   627,   1.10, 1993),
    ("GMA T.50",                                370,   2.9,   663,   3.10, 2022),
    ("Pagani Huayra R",                         370,   2.8,   850,   3.10, 2022),
    ("Ferrari LaFerrari",                       350,   2.9,   950,   1.40, 2013),
    ("McLaren P1",                              350,   2.8,   916,   1.15, 2013),
    ("Lamborghini Aventador SVJ",               350,   2.8,   770,   0.52, 2018),
    ("Lamborghini Sian",                        350,   2.8,   819,   3.60, 2020),
    ("McLaren Senna",                           340,   2.8,   800,   1.00, 2018),
    ("Ferrari SF90 Stradale",                   340,   2.5,   986,   0.51, 2019),
    ("Ferrari 296 GTB",                         330,   2.9,   830,   0.32, 2022),
    ("Porsche 918 Spyder",                      345,   2.6,   887,   0.85, 2013),
    ("Bugatti Divo",                            380,   2.4,  1479,   6.00, 2019),
    ("Ford GT (2017)",                          348,   3.3,   647,   0.45, 2017),
    ("Ferrari Enzo",                            350,   3.65,  651,   0.66, 2002),
    ("Porsche Carrera GT",                      330,   3.9,   612,   0.44, 2004),
    ("Nissan GT-R NISMO",                       315,   2.5,   600,   0.21, 2022),
    ("Lamborghini Huracán STO",                 310,   3.0,   640,   0.33, 2021),
    ("Chevrolet Corvette C8 Z06",               311,   2.6,   670,   0.11, 2023),
    ("Dodge Viper ACR",                         299,   3.3,   645,   0.12, 2017),
    ("Ferrari 488 GTB",                         330,   3.0,   660,   0.28, 2015),
    ("Lamborghini Urus Performante",            306,   3.3,   666,   0.24, 2022),
    ("McLaren 765LT",                           330,   2.8,   765,   0.36, 2020),
    ("Porsche 911 GT2 RS",                      340,   2.7,   700,   0.30, 2018),
    ("Maserati MC20",                           325,   2.9,   630,   0.22, 2021),
    ("Zenvo TSR-S",                             325,   2.8,  1177,   1.19, 2018),
    ("Lotus Evija",                             320,   3.0,  2000,   2.30, 2022),
    ("Pininfarina Battista",                    350,   1.86, 1900,   2.50, 2023),
]

for _n, _spd, _acc, _pwr, _prc, _yr in _supercars_data:
    supercars_pack.add_card(_n, [_spd, _acc, _pwr, _prc, _yr])


# ---------------------------------------------------------------------------
# 🏁 F1 Cars Pack  (stats: Top Speed km/h, Power hp, Season Wins, Weight kg, Year)
# ---------------------------------------------------------------------------
f1_pack = CardPack(
    name="F1 Cars",
    stat_names=["Top Speed", "Power", "Season Wins", "Weight", "Year"],
    stat_units={"Top Speed": "km/h", "Power": "hp", "Weight": "kg"},
    lower_is_better=["Weight"],
)

_f1_data = [
    # (name,                          top_speed, power, wins, weight, year)
    ("Red Bull RB19",                      360,  1000,   21,    798, 2023),
    ("Mercedes W11",                       374,  1000,   13,    746, 2020),
    ("Ferrari F2004",                      369,   900,   15,    600, 2004),
    ("McLaren MP4/4",                      320,   685,   15,    540, 1988),
    ("Mercedes W07",                       360,   900,   19,    702, 2016),
    ("Red Bull RB9",                       330,   800,   13,    642, 2013),
    ("Red Bull RB6",                       335,   780,   15,    620, 2010),
    ("Mercedes W05",                       355,   900,   16,    691, 2014),
    ("Mercedes W06",                       358,   950,   16,    701, 2015),
    ("Red Bull RB7",                       320,   790,   12,    640, 2011),
    ("Williams FW14B",                     320,   780,   10,    505, 1992),
    ("McLaren MP4/6",                      310,   700,    8,    505, 1991),
    ("McLaren MP4/13",                     330,   780,    9,    600, 1998),
    ("Ferrari F1-2000",                    350,   840,   10,    600, 2000),
    ("Renault R25",                        340,   870,    8,    605, 2005),
    ("Ferrari 248 F1",                     355,   870,    9,    605, 2006),
    ("Brawn BGP001",                       320,   750,    8,    605, 2009),
    ("Williams FW15C",                     325,   750,   10,    505, 1993),
    ("McLaren MP4/2",                      295,   750,   12,    540, 1984),
    ("Ferrari 312T2",                      295,   500,    9,    575, 1976),
    ("McLaren M23",                        290,   480,   16,    590, 1974),
    ("Lotus 72D",                          280,   450,    8,    530, 1970),
    ("Red Bull RB8",                       320,   790,   12,    642, 2012),
    ("Mercedes W08",                       360,   950,   12,    728, 2017),
    ("Red Bull RB16B",                     365,   1000,  11,    798, 2021),
    ("Ferrari F14 T",                      340,   870,    2,    691, 2014),
    ("McLaren MP4/23",                     330,   780,    8,    605, 2008),
    ("Williams FW18",                      330,   720,    8,    505, 1996),
    ("Lotus 49B",                          290,   415,    5,    508, 1968),
    ("Tyrrell P34",                        285,   465,    3,    595, 1976),
]

for _n, _spd, _pwr, _wins, _wgt, _yr in _f1_data:
    f1_pack.add_card(_n, [_spd, _pwr, _wins, _wgt, _yr])


# ---------------------------------------------------------------------------
# 🚀 Space Pack  (stats: Diameter km, Moons, Gravity m/s², Avg Temp °C, Discovery Year)
# ---------------------------------------------------------------------------
space_pack = CardPack(
    name="Space",
    stat_names=["Diameter", "Moons", "Gravity", "Avg Temp", "Discovery Year"],
    stat_units={"Diameter": "km", "Gravity": "m/s²", "Avg Temp": "°C"},
    lower_is_better=["Discovery Year"],
)

_space_data = [
    # (name,              diameter_km, moons, gravity, avg_temp, discovery_year)
    # discovery_year: negative = known in antiquity
    ("Sun",               1391000,       8,  274.0,    5500,  -3000),
    ("Jupiter",            139820,      95,   24.8,    -110,  -3000),
    ("Saturn",             116460,     146,   10.4,    -140,  -3000),
    ("Uranus",              50724,      28,    8.7,    -195,   1781),
    ("Neptune",             49244,      16,   11.2,    -200,   1846),
    ("Earth",               12742,       1,    9.8,      15,  -3000),
    ("Venus",               12104,       0,    8.9,     464,  -3000),
    ("Mars",                 6779,       2,    3.7,     -65,  -3000),
    ("Ganymede",             5268,       0,    1.4,    -163,   1610),
    ("Titan",                5150,       0,    1.4,    -179,   1655),
    ("Mercury",              4879,       0,    3.7,     167,  -3000),
    ("Callisto",             4821,       0,    1.2,    -139,   1610),
    ("Io",                   3636,       0,    1.8,    -130,   1610),
    ("Moon",                 3474,       0,    1.6,     -20,  -3000),
    ("Europa",               3122,       0,    1.3,    -160,   1610),
    ("Triton",               2707,       0,    0.78,   -235,   1846),
    ("Pluto",                2376,       5,    0.62,   -225,   1930),
    ("Eris",                 2326,       1,    0.82,   -238,   2005),
    ("Titania",              1578,       0,    0.38,   -203,   1787),
    ("Haumea",               1560,       2,    0.44,   -241,   2004),
    ("Oberon",               1523,       0,    0.35,   -198,   1787),
    ("Rhea",                 1527,       0,    0.26,   -220,   1672),
    ("Iapetus",              1469,       0,    0.22,   -143,   1671),
    ("Makemake",             1430,       1,    0.40,   -239,   2005),
    ("Charon",               1212,       0,    0.29,   -220,   1978),
    ("Umbriel",              1169,       0,    0.25,   -208,   1851),
    ("Ariel",                1158,       0,    0.27,   -210,   1851),
    ("Dione",                1123,       0,    0.23,   -186,   1684),
    ("Tethys",               1062,       0,    0.15,   -187,   1684),
    ("Ceres",                 945,       0,    0.28,   -105,   1801),
    ("Enceladus",             504,       0,    0.11,   -198,   1789),
    ("Miranda",               472,       0,    0.08,   -187,   1948),
]

for _n, _dia, _moons, _grav, _temp, _yr in _space_data:
    space_pack.add_card(_n, [_dia, _moons, _grav, _temp, _yr])


# ---------------------------------------------------------------------------
# ⛰️ Mountains Pack  (stats: Height m, Prominence m, First Ascent yr, Difficulty 1-10, Latitude °)
# ---------------------------------------------------------------------------
mountains_pack = CardPack(
    name="Mountains",
    stat_names=["Height", "Prominence", "First Ascent", "Difficulty", "Latitude"],
    stat_units={"Height": "m", "Prominence": "m", "Latitude": "°"},
    lower_is_better=["First Ascent"],
)

_mountains_data = [
    # (name,                  height_m, prominence_m, first_ascent, difficulty, latitude)
    ("Mount Everest",            8849,       8849,       1953,         9,     28),
    ("K2",                       8611,       4017,       1954,        10,     36),
    ("Kangchenjunga",            8586,       3922,       1955,         9,     27),
    ("Lhotse",                   8516,        610,       1956,         8,     28),
    ("Makalu",                   8485,       2386,       1955,         9,     28),
    ("Cho Oyu",                  8188,       2340,       1954,         7,     28),
    ("Dhaulagiri I",             8167,       3357,       1960,         9,     29),
    ("Manaslu",                  8163,       3092,       1956,         9,     29),
    ("Nanga Parbat",             8126,       4608,       1953,        10,     35),
    ("Annapurna I",              8091,       2984,       1950,        10,     29),
    ("Gasherbrum I",             8080,       2155,       1958,         8,     36),
    ("Broad Peak",               8051,       1701,       1957,         7,     36),
    ("Gasherbrum II",            8035,       1523,       1956,         7,     36),
    ("Shishapangma",             8027,       2897,       1964,         7,     29),
    ("Aconcagua",                6961,       6961,       1897,         7,    -33),
    ("Denali",                   6190,       6140,       1913,         8,     63),
    ("Chimborazo",               6263,       6310,       1880,         6,     -2),
    ("Mount Logan",              5959,       5250,       1925,         7,     61),
    ("Kilimanjaro",              5895,       5885,       1889,         5,     -3),
    ("Pico de Orizaba",          5636,       4922,       1848,         6,     19),
    ("Elbrus",                   5642,       5642,       1874,         5,     43),
    ("Popocatépetl",             5426,       3020,       1519,         7,     19),
    ("Mount Kenya",              5199,       3825,       1899,         7,      0),
    ("Margherita Peak",          5109,       3952,       1906,         7,      0),
    ("Vinson Massif",            4892,       4892,       1966,         7,    -78),
    ("Puncak Jaya",              4884,       4884,       1962,         7,     -4),
    ("Mont Blanc",               4808,       4696,       1786,         6,     46),
    ("Mount Rainier",            4392,       4026,       1870,         6,     47),
    ("Mount Whitney",            4421,       3072,       1873,         4,     37),
    ("Matterhorn",               4478,       1042,       1865,         8,     46),
    ("Mount Fuji",               3776,       3776,        663,         3,     35),
    ("Olympus (Greece)",         2918,       2355,       1913,         4,     40),
]

for _n, _h, _p, _fa, _diff, _lat in _mountains_data:
    mountains_pack.add_card(_n, [_h, _p, _fa, _diff, _lat])


# Convenient lookup by key
PACKS = {
    "animals":    animals_pack,
    "movies":     movies_pack,
    "countries":  countries_pack,
    "technology": technology_pack,
    "supercars":  supercars_pack,
    "f1":         f1_pack,
    "space":      space_pack,
    "mountains":  mountains_pack,
}
