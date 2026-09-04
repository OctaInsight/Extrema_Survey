"""EXTREMA partner needs survey — content definitions.

Everything a coordinator might want to edit lives here, so app.py stays structural.
"""

PROJECT = "EXTREMA"
CALL = "HORIZON-MISS-2026-01-CLIMA-05"
DEADLINE = "23 September 2026"

# --------------------------------------------------------------------------
# Beneficiaries. group drives which question blocks appear and how the
# coordinator page splits the means.
#   authority  = demonstration or replicating regional/local authority
#   technical  = university, RTO, SME bringing a toolkit component
#   support    = engagement, dissemination, business-support partner
# --------------------------------------------------------------------------
PARTNERS = [
    ("HMU",       "Hellenic Mediterranean University",                 "GR", "technical"),
    ("FORTH",     "Foundation for Research and Technology Hellas",     "GR", "technical"),
    ("CHANIA",    "Municipality of Chania",                            "GR", "authority"),
    ("GORTYNA",   "Municipality of Gortyna",                           "GR", "authority"),
    ("RDFCM",     "Regional Development Fund of Central Macedonia",    "GR", "authority"),
    ("OCTA",      "Octa Insight",                                      "NO", "technical"),
    ("ENVOLVE",   "Envolve Entrepreneurship",                          "CY", "support"),
    ("ASOFUER",   "Asociacion de Empresarios de Fuerteventura",        "ES", "support"),
    ("LAOLIVA",   "Ayuntamiento de La Oliva",                          "ES", "authority"),
    ("LAPINAMK",  "Lapland University of Applied Sciences",            "FI", "technical"),
    ("ROVANIEMI", "City of Rovaniemi / Regional Museum of Lapland",    "FI", "authority"),
    ("UdA",       "Universita degli Studi G. d'Annunzio Chieti-Pescara","IT", "technical"),
    ("UO",        "Universite d'Orleans",                              "FR", "technical"),
    ("CVL",       "Region Centre-Val de Loire",                        "FR", "authority"),
    ("CHAMBORD",  "Domaine national de Chambord",                      "FR", "authority"),
    ("ABE",       "Association of Business Entities",                  "RS", "support"),
    ("UNS-TF",    "University of Novi Sad, Faculty of Technology",     "RS", "technical"),
    ("PSC-VOJ",   "Provincial Secretariat for Culture, Vojvodina",     "RS", "authority"),
    ("SME-RS",    "Serbian SME partner (to be confirmed)",             "RS", "technical"),
    ("DRAC",      "Direcao Regional da Cultura dos Acores",            "PT", "authority"),
    ("RVB",       "Region Vasterbotten",                               "SE", "authority"),
    ("RRCK",      "Regional Development Centre Koper",                 "SI", "authority"),
    ("AUC",       "American University in Cairo",                      "EG", "technical"),
    ("NVG",       "New Valley Governorate",                            "EG", "authority"),
]

PARTNER_LOOKUP = {p[0]: {"name": p[1], "country": p[2], "group": p[3]} for p in PARTNERS}

# --------------------------------------------------------------------------
# The seven needs. `prompt` is what the partner reads; `lands` tells them
# where the answer goes. Keep prompts in plain English — most respondents
# are working in a second language.
# --------------------------------------------------------------------------
NEEDS = [
    dict(
        id="N1",
        short="Compound hazard diagnosis",
        prompt=(
            "Your organisation can identify which climate hazards act **together** on a "
            "specific monument, wall or site, and describe how that combination causes damage."
        ),
        help=(
            "Example: knowing that salt spray combined with summer heat is what drives surface "
            "loss on a particular facade, rather than knowing only that the area is hot and coastal."
        ),
        lands="Need N1 · challenge C1 · objective SO1",
    ),
    dict(
        id="N2",
        short="Climate data at the asset",
        prompt=(
            "Your organisation can obtain climate information at the scale it actually manages — "
            "the individual wall, facade or drainage line — rather than only regional averages."
        ),
        help="Includes access to downscaled projections and to a local weather record.",
        lands="Need N2 · challenge C2 · objective SO1, SO2",
    ),
    dict(
        id="N3",
        short="Monitoring in daily use",
        prompt=(
            "Your organisation operates monitoring of its heritage that staff use in their normal "
            "work, and that would continue running if an external project ended tomorrow."
        ),
        help="Sensors, surveys or a platform that someone is responsible for and actually opens.",
        lands="Need N3 · challenge C3 · objective SO2",
    ),
    dict(
        id="N4",
        short="Conservation for outdoor fabric",
        prompt=(
            "Your organisation has access to conservation materials and protocols suitable for "
            "**outdoor** heritage exposed to several hazards at once, with evidence they work."
        ),
        help="Not laboratory results alone — materials applied on real fabric with a record of the outcome.",
        lands="Need N4 · challenge C4 · objective SO3",
    ),
    dict(
        id="N5",
        short="Screening and measurement",
        prompt=(
            "Before a protective measure is installed, your organisation screens it for the harm it "
            "might cause, and afterwards measures whether it actually worked against a baseline."
        ),
        help=(
            "A baseline recorded before installation, a comparison surface or period, and a written "
            "check on whether the measure could damage heritage values or shift risk elsewhere."
        ),
        lands="Need N5 · challenge C5 · objective SO3, SO5",
    ),
    dict(
        id="N6",
        short="Values and governance",
        prompt=(
            "Your organisation has a working way to decide **with** owners, residents, conservators "
            "and permitting bodies what may be changed on a heritage asset, and records those decisions."
        ),
        help="Includes the permit route, the consultation practice and who has authority to stop a measure.",
        lands="Need N6 · challenge C6 · objective SO4",
    ),
    dict(
        id="N7",
        short="Replication and financing",
        prompt=(
            "Your organisation can take a solution proven elsewhere, judge whether it applies to your "
            "own assets, and identify a funding line that would pay for it."
        ),
        help="ERDF, LIFE, Interreg, national or own budget — a route that exists and a cycle you can enter.",
        lands="Need N7 · challenge C7 · objective SO5, SO6",
    ),
]

# --------------------------------------------------------------------------
# Four capacity dimensions, asked of everyone.
# --------------------------------------------------------------------------
CAPACITIES = [
    dict(id="CAP_TECH", short="Technical and scientific capacity",
         prompt="Staff with the technical or scientific skills this project needs from you."),
    dict(id="CAP_DATA", short="Data and digital infrastructure",
         prompt="Systems, storage, connectivity and data management your contribution depends on."),
    dict(id="CAP_INST", short="Institutional and leadership support",
         prompt="A decision-maker who backs this work and can commit the organisation to it."),
    dict(id="CAP_EU",   short="EU project management and reporting",
         prompt="Experience running or reporting a Horizon Europe or comparable EU grant."),
]

SCALE = {
    1: "1 — none",
    2: "2 — limited",
    3: "3 — partial",
    4: "4 — good",
    5: "5 — strong",
}

HAZARDS = [
    "Heat waves and extreme temperature",
    "Heavy rainfall and flash flooding",
    "River or coastal flooding",
    "Drought and groundwater decline",
    "Storms and wind",
    "Sea-level rise and coastal erosion",
    "Salt spray and salt crystallisation",
    "Saharan dust or airborne particulates",
    "Freeze-thaw cycling",
    "Snow load",
    "Subsidence or ground movement",
    "Wildfire",
    "Biological growth and biodeterioration",
]

HERITAGE_TYPES = [
    "Immovable — built heritage (buildings, fortifications, harbours)",
    "Immovable — archaeological sites and landscapes",
    "Movable — museum collections and artefacts",
    "Natural heritage with cultural significance (dunes, terraces, water systems)",
    "Intangible practices tied to the above",
]

FUNDING_ROUTES = [
    "ERDF / regional operational programme",
    "National heritage or culture budget",
    "LIFE programme",
    "Interreg",
    "Own municipal or regional budget",
    "Private or philanthropic funding",
    "None identified",
]
