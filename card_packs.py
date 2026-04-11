class Card:
    def __init__(self, title, categories):
        self.title = title
        # categories: dict of {stat_name: value}
        self.categories = categories

    def __str__(self):
        stats = ", ".join(f"{k}: {v}" for k, v in self.categories.items())
        return f"{self.title} [{stats}]"


class CardPack:
    def __init__(self, name, stat_names, stat_units=None):
        self.name = name
        self.stat_names = stat_names        # ordered list of 5 stat names
        self.stat_units = stat_units or {}  # optional display units per stat
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


# Convenient lookup by key
PACKS = {
    "animals":    animals_pack,
    "movies":     movies_pack,
    "countries":  countries_pack,
    "technology": technology_pack,
}
