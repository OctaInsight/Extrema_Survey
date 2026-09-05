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
        title="Knowing which hazards act together on a specific asset",
        prompt=(
            "Your organisation can identify which climate hazards act **together** on a "
            "specific monument, wall or site, and describe how that combination causes damage."
        ),
        meaning=(
            "Climate hazards rarely damage heritage one at a time. Salt arrives with heat, "
            "moisture with frost, dust with rain — and the combination does more harm than "
            "either hazard alone. Assessing hazards separately therefore understates the risk. "
            "What is needed is not a risk score but a written chain: this hazard, arriving by "
            "this route, acting on this material, producing this kind of damage."
        ),
        example=(
            "Weak: *the area is hot and coastal, so the fort is at risk.*  \n"
            "Strong: *wind-blown salt is deposited on the seaward wall, summer heat drives "
            "crystallisation inside the pores, and the resulting stress detaches the surface "
            "layer — which is why loss concentrates on the south-west elevation.*"
        ),
        anchors={
            1: "We know the general climate of our area but have not analysed hazards for individual assets.",
            3: "We have identified the main hazards affecting our heritage, but one hazard at a time.",
            5: "For named assets we have written down which hazards combine and the physical chain by which the combination causes damage.",
        },
        lands="Need N1 · challenge C1 · objective SO1 · toolkit Module 1",
    ),
    dict(
        id="N2",
        short="Climate data at the asset",
        title="Climate information at the scale you actually manage",
        prompt=(
            "Your organisation can obtain climate information at the scale it actually manages — "
            "the individual wall, facade or drainage line — rather than only regional averages."
        ),
        meaning=(
            "Climate projections are normally produced on a grid of about ten kilometres. "
            "Conservation decisions are taken at the scale of a single elevation. A grid cell "
            "cannot tell you that one facade swings more than twenty degrees in a day while the "
            "one behind it does not. Heritage users have formally recorded a need for products "
            "at one to five metres; this question asks how close you can currently get."
        ),
        example=(
            "This includes both directions in time: a local record of what has already happened "
            "(a weather station at or near the site, event archives, past damage), and projections "
            "for 2050 or 2080 that someone has downscaled to your location rather than your region."
        ),
        anchors={
            1: "We rely on general weather reports or national climate summaries.",
            3: "We have regional climate projections, but nothing at the scale of an individual building or site.",
            5: "We have local measurements at or near our assets and downscaled projections we can use in a conservation decision.",
        },
        lands="Need N2 · challenge C2 · objective SO1, SO2 · toolkit Modules 1 and 2",
    ),
    dict(
        id="N3",
        short="Monitoring in daily use",
        title="Monitoring that survives the project that installed it",
        prompt=(
            "Your organisation operates monitoring of its heritage that staff use in their normal "
            "work, and that would continue running if an external project ended tomorrow."
        ),
        meaning=(
            "Monitoring platforms built for cultural heritage have a poor record of outliving "
            "their funding. Equipment is installed, a dashboard is delivered, and two years later "
            "nobody has an account or a maintenance budget. This question is about ownership as "
            "much as technology: is there a named person, a maintenance route, and a decision "
            "that the data actually changes?"
        ),
        example=(
            "Sensors, condition surveys on a fixed cycle, repeat photography or a monitoring "
            "platform all count. What does not count is equipment installed by a past project "
            "that nobody now opens, or a report produced once and filed."
        ),
        anchors={
            1: "No monitoring beyond occasional visual inspection.",
            3: "Some sensors or surveys exist, but they were installed by a project and nobody has clear responsibility for them now.",
            5: "Monitoring runs continuously, a named member of staff is responsible for it, and what it shows changes what we do.",
        },
        lands="Need N3 · challenge C3 · objective SO2 · toolkit Module 2",
    ),
    dict(
        id="N4",
        short="Conservation for outdoor fabric",
        title="Treatments proven on outdoor heritage, not only in the laboratory",
        prompt=(
            "Your organisation has access to conservation materials and protocols suitable for "
            "**outdoor** heritage exposed to several hazards at once, with evidence they work."
        ),
        meaning=(
            "Most work on environmentally sound conservation materials has been done for museum "
            "collections and interiors, where conditions are stable. Outdoor fabric under "
            "combined heat, salt, frost and rain is a much harder case, and promising materials "
            "such as bacteria-based consolidants have largely stayed in the laboratory or on "
            "test walls. This question asks what you can actually specify today for a wall "
            "exposed to weather."
        ),
        example=(
            "Evidence means a record of how a treatment performed after application: what was "
            "measured, when, and whether it held. A supplier's data sheet is not evidence; a "
            "documented outcome on comparable material in a comparable climate is."
        ),
        anchors={
            1: "We commission conservation work case by case, with no documented protocol.",
            3: "We follow established conservation practice, but have no evidence about how it performs under our specific hazards.",
            5: "We use documented protocols chosen for our materials and hazards, and hold records of how earlier treatments performed.",
        },
        lands="Need N4 · challenge C4 · objective SO3 · toolkit Module 4",
    ),
    dict(
        id="N5",
        short="Screening and measurement",
        title="Checking a measure before it goes in, and measuring it afterwards",
        prompt=(
            "Before a protective measure is installed, your organisation screens it for the harm "
            "it might cause, and afterwards measures whether it actually worked against a baseline."
        ),
        meaning=(
            "Two habits are missing across the sector, and both are needed. **Before:** a written "
            "check that the measure will not shift risk elsewhere, lock in a solution a warmer "
            "climate will defeat, or damage the heritage values it is meant to protect — "
            "adaptation can itself cause harm. **After:** a measurement against a baseline "
            "recorded before the work, so the effect can be told apart from the weather that "
            "happened to follow."
        ),
        example=(
            "A drainage channel that keeps a wall drier but sends water towards an archaeological "
            "deposit has succeeded on one measure and failed overall. Only an advance screen "
            "catches that, and only a baseline plus a comparison surface or period shows whether "
            "the wall really did get drier."
        ),
        anchors={
            1: "We install what is specified and do not measure the result.",
            3: "We record the work carried out, but without a measurement beforehand or anything to compare against.",
            5: "We record a baseline before work, keep a comparison surface or period, screen for possible harm in advance, and measure the outcome afterwards.",
        },
        lands="Need N5 · challenge C5 · objective SO3, SO5 · toolkit Modules 4 and 6",
    ),
    dict(
        id="N6",
        short="Values and governance",
        title="Deciding with the people who own, permit and live with the heritage",
        prompt=(
            "Your organisation has a working way to decide **with** owners, residents, conservators "
            "and permitting bodies what may be changed on a heritage asset, and records those decisions."
        ),
        meaning=(
            "Whether a measure gets installed is decided as much by values and governance as by "
            "physics. What the community would accept losing, who owns the asset, who issues the "
            "permit and who pays for maintenance afterwards will stop a technically sound measure "
            "if they are not settled first. Heritage professionals across Europe name governance "
            "and knowledge, not technology, as the binding constraints on adaptation."
        ),
        example=(
            "Recording matters as much as consulting. If an objection changed a design, or a "
            "permitting body refused an option, that should be written down — it is the evidence "
            "that explains why the final measure looks as it does, and it is what allows another "
            "authority to judge whether the same measure would pass with them."
        ),
        anchors={
            1: "Decisions are taken internally, with consultation only where the law requires it.",
            3: "We consult owners and the permitting body, but the process is informal and not recorded.",
            5: "We have an established process involving owners, residents, conservators and permitting bodies, and decisions and objections are documented.",
        },
        lands="Need N6 · challenge C6 · objective SO4 · toolkit Module 3",
    ),
    dict(
        id="N7",
        short="Replication and financing",
        title="Taking up a solution proven elsewhere, and paying for it",
        prompt=(
            "Your organisation can take a solution proven elsewhere, judge whether it applies to "
            "your own assets, and identify a funding line that would pay for it."
        ),
        meaning=(
            "Two capabilities together. **Judgement:** deciding whether a measure that worked on "
            "someone else's material, climate and governance will work on yours — which requires "
            "knowing the conditions under which it held. **Money:** naming an instrument that "
            "exists and a budget cycle you can enter. Guidance documents without a funding route "
            "are the usual reason replication stops."
        ),
        example=(
            "ERDF and the regional operational programme, LIFE, Interreg, a national heritage or "
            "culture budget, or your own capital budget all count. What matters is whether you "
            "know the cycle, the conditions and who inside your organisation would prepare the bid."
        ),
        anchors={
            1: "We have no route to fund heritage adaptation beyond emergency repair.",
            3: "We could identify a funding route with effort, but have not done so for climate adaptation of heritage.",
            5: "We have used or applied to a specific instrument for heritage adaptation and know its cycle and conditions.",
        },
        lands="Need N7 · challenge C7 · objective SO5, SO6 · toolkit Module 6",
    ),
]

CAPACITIES = [
    dict(id="CAP_TECH", short="Technical and scientific capacity",
         prompt="Staff with the technical or scientific skills this project needs from you.",
         meaning="People, not equipment. Whether someone in your organisation could take on "
                 "the work your partners will expect of you, alongside their existing duties."),
    dict(id="CAP_DATA", short="Data and digital infrastructure",
         prompt="Systems, storage, connectivity and data management your contribution depends on.",
         meaning="Includes network coverage at your sites, somewhere to keep data safely, and "
                 "whoever administers it. Poor connectivity at a remote site belongs here."),
    dict(id="CAP_INST", short="Institutional and leadership support",
         prompt="A decision-maker who backs this work and can commit the organisation to it.",
         meaning="Whether someone senior enough to allocate staff time and sign commitments has "
                 "already agreed to this, or whether it still rests on individual goodwill."),
    dict(id="CAP_EU",   short="EU project management and reporting",
         prompt="Experience running or reporting a Horizon Europe or comparable EU grant.",
         meaning="Timesheets, cost claims, deliverable formats and periodic reports. A low score "
                 "here is common and is planned for, not penalised."),
]

# Organisation types. Determines which extra questions a respondent sees.
ORG_TYPES = [
    ("authority", "Regional or local authority, or a heritage body under one"),
    ("technical", "University, research organisation or technology company"),
    ("support",   "Association, network, chamber or other support organisation"),
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
