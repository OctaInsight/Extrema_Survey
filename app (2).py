"""EXTREMA partner needs survey.

Run:    streamlit run app.py
Deploy: push to a repo and connect it to Streamlit Community Cloud.

Responses go to data/responses.csv by default. On Streamlit Community Cloud that
file is wiped on every restart, so set up the Google Sheets backend before
sending the link to partners — see README.md.
"""

from __future__ import annotations

import datetime as dt
import io
import uuid

import pandas as pd
import streamlit as st

import db

from content import (
    CALL,
    CAPACITIES,
    DEADLINE,
    FUNDING_ROUTES,
    HAZARDS,
    HERITAGE_TYPES,
    NEEDS,
    PARTNER_LOOKUP,
    PARTNERS,
    PROJECT,
    SCALE,
)

st.set_page_config(
    page_title=f"{PROJECT} partner survey",
    page_icon="◵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Styling. Verdigris accent, slate ink, serif headings against a sans form.
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
      :root {
        --ink:      #16232E;
        --verdi:    #2D6A73;
        --verdi-lo: #E8F0F0;
        --oxide:    #A85419;
        --rule:     #D7DEE1;
        --muted:    #5C6B75;
      }
      .block-container { max-width: 46rem; padding-top: 2.4rem; padding-bottom: 4rem; }
      html, body, [class*="css"] { color: var(--ink); }

      h1, h2, h3 {
        font-family: Georgia, "Iowan Old Style", "Source Serif 4", serif !important;
        color: var(--ink) !important; letter-spacing: -0.01em;
      }
      h1 { font-size: 1.9rem !important; line-height: 1.2; margin-bottom: .2rem !important; }
      h2 { font-size: 1.3rem !important; margin-top: 2.2rem !important; }

      .standfirst { color: var(--muted); font-size: .95rem; line-height: 1.55; max-width: 40rem; }

      .qcard {
        border-left: 3px solid var(--verdi);
        background: #FBFBFA;
        padding: .85rem 1rem .35rem 1rem;
        margin: 1.1rem 0 .2rem 0;
      }
      .qcard .qid {
        font-family: Georgia, serif; font-weight: 700; color: var(--verdi);
        font-size: .95rem; margin-right: .45rem;
      }
      .qcard .qtext { font-size: .97rem; line-height: 1.5; }
      .lands { color: var(--muted); font-size: .78rem; margin-top: .45rem; }

      .note {
        border: 1px solid var(--rule); background: #fff;
        padding: .75rem .9rem; font-size: .88rem; color: var(--muted);
        line-height: 1.5; margin: 1rem 0;
      }
      .flag { border-color: var(--oxide); color: var(--oxide); }

      div.stButton > button[kind="primary"] {
        background: var(--verdi); border: 1px solid var(--verdi);
        border-radius: 2px; font-weight: 600; padding: .55rem 1.4rem;
      }
      div.stButton > button[kind="primary"]:hover { background: #24565D; border-color: #24565D; }

      hr { border-color: var(--rule); }
      [data-testid="stMetricValue"] { font-family: Georgia, serif; color: var(--verdi); }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Survey page
# ---------------------------------------------------------------------------
def survey_page() -> None:
    st.title("How ready is your organisation?")
    st.markdown(
        f'<p class="standfirst">This survey establishes the baseline for the '
        f'{PROJECT} proposal to {CALL}, closing {DEADLINE}. It takes about ten minutes. '
        f'Answer for your <strong>organisation as it is today</strong>, not for what the project '
        f'will make possible — an honest low score is more useful than a generous one, '
        f'because the work plan assigns support to whoever needs it.</p>',
        unsafe_allow_html=True,
    )

    st.markdown("## Who is answering")
    col1, col2 = st.columns([3, 2])
    with col1:
        codes = ["— select —"] + [p[0] for p in PARTNERS]
        code = st.selectbox(
            "Your organisation",
            codes,
            format_func=lambda c: c if c == "— select —"
            else f"{c} — {PARTNER_LOOKUP[c]['name']} ({PARTNER_LOOKUP[c]['country']})",
        )
    with col2:
        respondent = st.text_input("Your name")

    role = st.text_input("Your role", placeholder="e.g. Head of heritage service")
    email = st.text_input("Email", placeholder="for follow-up questions only")

    if code == "— select —":
        st.markdown(
            '<div class="note">Select your organisation to continue.</div>',
            unsafe_allow_html=True,
        )
        return

    meta = PARTNER_LOOKUP[code]
    group = meta["group"]

    with st.form("survey", clear_on_submit=False):
        st.markdown("## The seven capability areas")
        st.markdown(
            '<p class="standfirst">Rate your organisation from 1 (none) to 5 (strong). '
            'If an area is outside your remit entirely, choose 1 and say so in the comment '
            'box at the end.</p>',
            unsafe_allow_html=True,
        )

        need_scores: dict[str, int] = {}
        for n in NEEDS:
            st.markdown(
                f'<div class="qcard"><span class="qid">{n["id"]}</span>'
                f'<span class="qtext">{n["prompt"]}</span>'
                f'<div class="lands">{n["lands"]}</div></div>',
                unsafe_allow_html=True,
            )
            need_scores[n["id"]] = st.select_slider(
                n["short"], options=[1, 2, 3, 4, 5], value=3,
                format_func=lambda v: SCALE[v], help=n["help"], key=f"need_{n['id']}",
            )

        st.markdown("## Organisational capacity")
        cap_scores: dict[str, int] = {}
        for c in CAPACITIES:
            cap_scores[c["id"]] = st.select_slider(
                c["short"], options=[1, 2, 3, 4, 5], value=3,
                format_func=lambda v: SCALE[v], help=c["prompt"], key=c["id"],
            )

        st.markdown("## Continuity after funding ends")
        financing = st.radio(
            "Do you have an identified funding line to keep climate or heritage monitoring "
            "running after a project ends?",
            ["Yes, secured", "Partly — a route exists but is not committed", "No"],
            index=2,
        )
        funding_routes = st.multiselect(
            "Which funding routes are realistically open to you?", FUNDING_ROUTES,
        )
        discontinued = st.radio(
            "Has your organisation hosted a heritage or climate pilot that stopped when its "
            "funding ended?",
            ["Yes", "No", "Not sure"],
            index=1,
        )
        discontinued_why = st.text_area(
            "If yes, what stopped it?", height=70,
            placeholder="e.g. no budget line for sensor maintenance after the grant",
        )

        # ------------------------------------------------------------------
        # Authority-only block
        # ------------------------------------------------------------------
        assets = hazards = permit_body = plans = charter = staff = ""
        heritage_types: list[str] = []
        if group == "authority":
            st.markdown("## Your heritage and your hazards")
            assets = st.text_area(
                "Which assets would you put forward for work in this project?",
                height=90,
                placeholder="Name them: e.g. Torre del Toston (c.1700, coastal masonry); "
                            "aljibes of the Ruta del Agua",
            )
            heritage_types = st.multiselect("Types of heritage you are responsible for", HERITAGE_TYPES)
            hazards = st.multiselect("Hazards already affecting these assets", HAZARDS)
            permit_body = st.text_input(
                "Which body must authorise physical work on them?",
                placeholder="e.g. Ephorate of Antiquities of Chania",
            )
            plans = st.text_area(
                "Existing climate, adaptation or emergency plans that cover this heritage",
                height=70,
                placeholder="Title, year, and whether heritage is named in it",
            )
            charter = st.radio(
                "Has your authority signed the Mission Charter on Adaptation to Climate Change?",
                ["Yes", "No", "Not sure"], index=2, horizontal=True,
            )
            staff = st.text_input(
                "Approximate staff time available for heritage management (FTE)",
                placeholder="e.g. 2.5",
            )

        # ------------------------------------------------------------------
        # Technical-partner block
        # ------------------------------------------------------------------
        components = trl = prior = ""
        if group in ("technical", "support"):
            st.markdown("## What you bring")
            components = st.text_area(
                "Which components or methods will you contribute?", height=90,
                placeholder="One per line, with its current maturity",
            )
            trl = st.text_input(
                "Technology readiness level of your main component today (1–9)",
                placeholder="e.g. TRL 6",
            )
            prior = st.text_area(
                "Where has it been demonstrated already?", height=70,
                placeholder="Project, site, year, and what was measured",
            )

        st.markdown("## Last question")
        barrier = st.text_area(
            "What is the single biggest thing stopping your organisation from protecting its "
            "heritage against climate impacts?",
            height=90,
        )
        comments = st.text_area("Anything else the coordinator should know", height=70)
        consent = st.checkbox(
            "I agree that these answers may be used in aggregate form in the EXTREMA proposal "
            "and that my organisation may be named as a respondent.",
        )

        submitted = st.form_submit_button("Submit answers", type="primary")

    if submitted:
        if not respondent.strip():
            st.error("Add your name before submitting.")
            return
        if not consent:
            st.error("Tick the consent box to submit.")
            return

        row = {
            "response_id": str(uuid.uuid4())[:8],
            "submitted_at": db.stamp(),
            "partner_code": code,
            "partner_name": meta["name"],
            "country": meta["country"],
            "group": group,
            "respondent": respondent.strip(),
            "role": role.strip(),
            "email": email.strip(),
            **{n["id"]: need_scores[n["id"]] for n in NEEDS},
            **cap_scores,
            "financing": financing,
            "funding_routes": "; ".join(funding_routes),
            "discontinued_pilot": discontinued,
            "discontinued_why": discontinued_why.strip(),
            "assets": assets.strip() if isinstance(assets, str) else "",
            "heritage_types": "; ".join(heritage_types),
            "hazards": "; ".join(hazards) if isinstance(hazards, list) else "",
            "permit_body": permit_body.strip() if isinstance(permit_body, str) else "",
            "existing_plans": plans.strip() if isinstance(plans, str) else "",
            "mission_charter": charter,
            "heritage_fte": staff.strip() if isinstance(staff, str) else "",
            "components": components.strip(),
            "trl": trl.strip(),
            "prior_demonstration": prior.strip(),
            "biggest_barrier": barrier.strip(),
            "comments": comments.strip(),
        }
        try:
            db.save_response(row)
        except db.StorageError as exc:
            st.error(str(exc))
            return
        st.success(f"Recorded for {code}. Thank you — reference {row['response_id']}.")
        st.balloons()


# ---------------------------------------------------------------------------
# Coordinator page
# ---------------------------------------------------------------------------
def coordinator_page() -> None:
    st.title("Coordinator view")

    expected = st.secrets.get("coordinator_password", "extrema")
    if st.text_input("Password", type="password") != expected:
        st.markdown(
            '<div class="note">Enter the coordinator password to see responses.</div>',
            unsafe_allow_html=True,
        )
        return

    ok, msg = db.connection_check()
    st.markdown(
        f'<div class="note{"" if ok else " flag"}">{msg}</div>',
        unsafe_allow_html=True,
    )

    df = db.fetch_responses()
    if st.button("Refresh"):
        db.fetch_responses.clear()
        st.rerun()

    if df.empty:
        st.markdown(
            '<div class="note">No responses yet.</div>', unsafe_allow_html=True,
        )
        return

    need_ids = [n["id"] for n in NEEDS]
    cap_ids = [c["id"] for c in CAPACITIES]
    for col in need_ids + cap_ids:
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    responded = df["partner_code"].nunique()
    total = len(PARTNERS)

    a, b, c = st.columns(3)
    a.metric("Responses", f"{responded} / {total}")
    b.metric("Authorities", int((df["group"] == "authority").sum()))
    c.metric("Technical & support", int((df["group"] != "authority").sum()))

    missing = sorted({p[0] for p in PARTNERS} - set(df["partner_code"]))
    if missing:
        st.markdown(
            f'<div class="note flag"><strong>Still to respond:</strong> {", ".join(missing)}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("## Mean capability by need")
    by_group = df.groupby("group")[need_ids].mean().round(2).T
    by_group["all"] = df[need_ids].mean().round(2).values
    by_group.index = [f'{n["id"]} {n["short"]}' for n in NEEDS]
    st.dataframe(by_group, use_container_width=True)
    st.bar_chart(df[need_ids].mean().round(2))

    st.markdown("## Capacity dimensions")
    caps = df[cap_ids].mean().round(2)
    caps.index = [c["short"] for c in CAPACITIES]
    st.dataframe(caps.to_frame("mean"), use_container_width=True)

    st.markdown("## Work-package leadership check")
    st.markdown(
        '<p class="standfirst">The strongest scorer on each need is the defensible '
        'candidate to lead the corresponding work package. Compare this against the '
        'assignments in Section 3.1.</p>',
        unsafe_allow_html=True,
    )
    rows = []
    for n in NEEDS:
        sub = df[["partner_code", n["id"]]].dropna().sort_values(n["id"], ascending=False)
        if sub.empty:
            continue
        def fmt(frame: pd.DataFrame) -> str:
            return ", ".join(
                f"{code} ({score:.0f})"
                for code, score in zip(frame["partner_code"], frame[n["id"]])
            )

        rows.append({
            "Need": f'{n["id"]} {n["short"]}',
            "Strongest": fmt(sub.head(3)),
            "Greatest need": fmt(sub.tail(3).sort_values(n["id"])),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("## Evidence for need N7")
    no_fin = (df["financing"] == "No").sum()
    stopped = (df["discontinued_pilot"] == "Yes").sum()
    x, y = st.columns(2)
    x.metric("No post-project financing", f"{no_fin} of {len(df)}")
    y.metric("Reported a discontinued pilot", f"{stopped} of {len(df)}")

    st.markdown("## Draft text for Section 1.2.1.4")
    auth = df[df["group"] == "authority"]
    tech = df[df["group"] != "authority"]
    if not auth.empty and not tech.empty:
        a_means = auth[need_ids].mean()
        weakest = a_means.nsmallest(3)
        strongest = a_means.nlargest(1)
        short = {n["id"]: n["short"].lower() for n in NEEDS}
        draft = (
            f"A partner-level assessment grounds the work plan. {len(df)} responses were returned, "
            f"one per beneficiary, each rating institutional capability against the seven need areas "
            f"and four capacity dimensions on a five-point scale. The demonstration and replicating "
            f"authorities rate themselves weakest on "
            + ", ".join(f"{short[i]} ({i}, mean {v:.1f})" for i, v in weakest.items())
            + f", and strongest on "
            + ", ".join(f"{short[i]} ({i}, {v:.1f})" for i, v in strongest.items())
            + f"; the technical partners show the inverse profile. "
            f"{no_fin} of {len(df)} respondents report no identified financing to maintain "
            f"monitoring after a project ends, and {stopped} report an earlier heritage or climate "
            f"pilot that did not continue after its funding ended, which evidences N7 directly. "
            f"Work-package leadership is therefore assigned to the beneficiary scoring strongest on "
            f"the corresponding competence, while implementing teams draw on those reporting the "
            f"greatest need."
        )
        st.code(draft, language=None)

    st.markdown("## Free-text answers")
    for label, col in [
        ("Biggest barrier", "biggest_barrier"),
        ("Assets nominated", "assets"),
        ("Why a pilot stopped", "discontinued_why"),
        ("Other comments", "comments"),
    ]:
        with st.expander(label):
            sub = df[["partner_code", col]].dropna()
            sub = sub[sub[col].astype(str).str.strip() != ""]
            for r in sub.itertuples():
                st.markdown(f"**{r.partner_code}** — {getattr(r, col)}")

    st.markdown("## Export")
    d1, d2, d3 = st.columns(3)
    d1.download_button(
        "Download CSV", df.to_csv(index=False).encode("utf-8"),
        f"extrema_survey_{dt.date.today()}.csv", "text/csv",
    )
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xl:
        df.to_excel(xl, sheet_name="responses", index=False)
        by_group.to_excel(xl, sheet_name="means_by_need")
        caps.to_frame("mean").to_excel(xl, sheet_name="capacities")
    d2.download_button(
        "Download Excel", buf.getvalue(),
        f"extrema_survey_{dt.date.today()}.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    d3.download_button(
        "Download JSON", db.export_json(df).encode("utf-8"),
        f"extrema_survey_{dt.date.today()}.json", "application/json",
    )

    with st.expander("All responses"):
        st.dataframe(df, use_container_width=True)


# ---------------------------------------------------------------------------
page = st.sidebar.radio("Page", ["Survey", "Coordinator"], label_visibility="collapsed")
st.sidebar.markdown(
    f"**{PROJECT}**  \n{CALL}  \nDeadline {DEADLINE}  \n\n"
    f"<span style='font-size:.78rem;color:#5C6B75'>Storage: {db.backend_name()}</span>",
    unsafe_allow_html=True,
)

if page == "Survey":
    survey_page()
else:
    coordinator_page()
