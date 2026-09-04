# EXTREMA partner needs survey

Collects the partner-level capability data behind **Section 1.2.1.4** of the EXTREMA
proposal (HORIZON-MISS-2026-01-CLIMA-05, closing 23 September 2026), so that section
rests on evidence rather than an assumption.

Stack: **GitHub → Streamlit Community Cloud → Supabase Postgres**.

| File | Purpose |
|---|---|
| `app.py` | Survey form and coordinator dashboard |
| `content.py` | Partner roster, the seven needs, hazard and funding lists — edit here |
| `db.py` | Storage layer: Supabase, falling back to local CSV |
| `supabase_schema.sql` | Adds `extrema_needs_survey` to an existing project |

---

## 1. Supabase — add one table to the project you already have

This runs alongside `harmonia_needs_survey` in the same project. Everything the
script creates is namespaced `extrema_` and every statement is idempotent, so the
HARMONIA table, its policies and its data are untouched.

**Create the table.** Open **SQL Editor -> New query**, paste the whole of
`supabase_schema.sql`, and Run. It creates `extrema_needs_survey`, two indexes, an
RLS policy and an `extrema_survey_means` view.

**Choose the RLS option before you run it.** The file contains two; delete the one
you do not want.

| | Option A (active by default) | Option B (matches HARMONIA) |
|---|---|---|
| anon key can | INSERT only | INSERT and SELECT |
| Secrets needed | `key` **and** `service_key` | `key` only |
| If the anon key leaks | nothing is exposed | every response readable, names and emails included |

Option A is recommended and costs one extra line in secrets. The anon key ships to
the Streamlit server and would be readable by anyone who ever saw the repo with a
committed secrets file; under Option A that key can write and nothing else. Get the
service-role key from **Settings -> API Keys**.

Option B reproduces your existing HARMONIA behaviour. To use it, delete the Option A
policy block and uncomment the Option B block.

**Verify nothing else changed.** At the foot of the SQL file are two commented
queries listing the project's tables and policies. Run them after the migration and
confirm `harmonia_needs_survey` still appears with its own policies intact.

> **Free-tier projects pause after about a week without activity.** With a September
> deadline, either open the dashboard every few days or upgrade before you send the
> link. A paused project returns connection errors and partners lose their answers.

## 2. GitHub

```bash
cd extrema_survey
git init
git add .
git commit -m "EXTREMA partner needs survey"
git branch -M main
git remote add origin https://github.com/YOUR-ORG/extrema-survey.git
git push -u origin main
```

`.gitignore` already excludes `.streamlit/secrets.toml` and `data/`. Check with
`git status` before the first push that neither appears. A private repo works with
Streamlit Cloud and is the better choice here.

---

## 3. Streamlit Community Cloud

1. [share.streamlit.io](https://share.streamlit.io) → **Create app** → **Deploy a
   public app from GitHub**.
2. Repository `YOUR-ORG/extrema-survey`, branch `main`, main file `app.py`.
3. **Advanced settings → Secrets**, paste the contents of
   `.streamlit/secrets.toml.example` with your real values:

```toml
coordinator_password = "something-only-the-coordinator-knows"

[supabase]
url = "https://YOUR-PROJECT-REF.supabase.co"
key = "your-anon-public-key"

# Only if you kept Option A in the schema.
service_key = "your-service-role-key"
```

The `[supabase]` block uses the same `url` / `key` names as your HARMONIA app, so you
can copy that app's secrets and add `service_key`.

4. Deploy. First build takes two or three minutes.

Confirm it worked: open the app, go to **Coordinator**, enter the password. The status
line names the table, which key it read with, and the row count. Two failure modes:

- *No Supabase secrets found* — the secrets did not save. Re-paste them, keeping the
  `[supabase]` header.
- *Could not reach `extrema_needs_survey`* — usually Option A without `service_key`.
  Either add the key, or switch the schema to Option B.

Send partners the app URL. Nothing to install, no login.

---

## 4. Run locally

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then edit
streamlit run app.py
```

Without a `[supabase]` section the app writes to `data/responses.csv`, so you can test
the form without touching the live database.

---

## What the coordinator page gives you

- Response tracker naming which of the 24 beneficiaries have not yet replied
- Mean capability per need, split into authorities vs technical and support partners
- Mean score per capacity dimension
- Strongest and weakest scorer per need — the defensible basis for work-package
  leadership, to be checked against Section 3.1
- Counts for the two N7 evidence claims: no post-project financing, and pilots that
  stopped when funding ended
- **A generated draft of the Section 1.2.1.4 paragraph** with your real numbers
  substituted, ready to paste into Part B
- All free-text answers grouped by question
- Export to CSV, Excel and JSON

---

## Editing the survey after launch

Change `content.py`, commit, push. Streamlit Cloud redeploys automatically in about a
minute. Adding a question needs no database migration: any field not in `DB_COLUMNS`
is stored in the `raw` JSONB column and reappears in the coordinator export. Only add
a real column (`alter table public.survey_responses add column ...`) if you want to
query it in SQL.

`PARTNERS` entries are `(code, name, country, group)`. The `group` value decides which
extra block a respondent sees:

| group | extra questions |
|---|---|
| `authority` | assets nominated, heritage types, hazards, permitting body, existing plans, Mission Charter status, heritage FTE |
| `technical` / `support` | components contributed, current TRL, prior demonstration |

---

## Data protection

Names, roles and email addresses are personal data under the GDPR. Before the link
goes out, settle four things: who the controller is (normally the coordinating
beneficiary), the lawful basis, the retention period, and where the data sits — which
is why the EU region above is not optional. The consent line in the form covers use in
aggregate and naming the *organisation*, not the individual.

If your DPO wants pseudonymised responses, delete `respondent` and `email` from the
row dictionary in `app.py`; everything downstream still works. To honour an erasure
request, delete the row in the Supabase table editor by `response_ref`. The EXTREMA and
HARMONIA tables are separate objects in one database, so a retention policy or
erasure request applied to one does not affect the other.

---

## Known limits

- One response per person, not enforced per organisation. Two submissions from the
  same partner are both counted — deduplicate on `partner_code` before quoting means.
- The coordinator password is a shared secret, not authentication. Adequate for a
  consortium, not for anything sensitive.
- If Supabase rejects a write, the app keeps a local CSV copy and tells the respondent
  to contact the coordinator. On Streamlit Cloud that copy is lost at the next
  restart, so act on the error rather than ignoring it.
- The generated Section 1.2.1.4 draft is a starting point. Check every number against
  the table above it before it enters Part B.
