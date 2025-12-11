# Data Folder

This folder contains the CSV exports used across all parts of the assessment:

- `campaign_leads.csv`: one row per lead, with campaign_id, lead_status, added_date, user_id, project_name…
- `campaigns.csv`: campaign metadata, including daily_budget and project_name.
- `insights.csv`: daily performance metrics (spend, impressions, clicks) per campaign.
- `lead_status_changes.csv` (optional): historical lead status transitions.

All notebooks assume these files are located under `data/`.
