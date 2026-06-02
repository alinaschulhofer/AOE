# Visitor IP Logger — Setup Guide

You will do 3 things, in order:
1. Create the Google Sheet + Apps Script (5 min)
2. Create a free Cloudflare account + deploy the Worker (10 min)
3. Update one line in your GitHub repo (1 min)

---

## Step 1 — Google Sheet + Apps Script

1. Go to https://sheets.google.com and create a new blank spreadsheet.
   Name it something like **AOE Visitor Log**.

2. In that spreadsheet, click **Extensions → Apps Script**.

3. Delete all the default code in the editor.

4. Open `visitor-logger/google-apps-script.js` from your repo and paste the entire contents in.

5. Click **Save** (the floppy disk icon).

6. Click **Deploy → New deployment**.
   - Click the gear icon next to "Select type" and choose **Web app**.
   - Description: `Visitor Logger`
   - Execute as: **Me**
   - Who has access: **Anyone** ← this is required so the Worker can post to it
   - Click **Deploy**.

7. Google will ask you to authorize — click through and allow it.

8. **Copy the Web app URL** — it looks like:
   `https://script.google.com/macros/s/LONG_RANDOM_STRING/exec`
   You'll need this in Step 2.

---

## Step 2 — Cloudflare Worker

1. Go to https://cloudflare.com and create a free account.

2. From the dashboard, click **Workers & Pages** in the left sidebar.

3. Click **Create** → **Create Worker**.

4. Give it a name like `aoe-visitor-logger`.

5. Click **Deploy** (don't worry about the default code yet).

6. After deploying, click **Edit code**.

7. Delete all the default code and paste in the entire contents of
   `visitor-logger/worker.js` from your repo.

8. Click **Deploy**.

9. Now set the environment variable:
   - Go back to your Worker's page and click **Settings → Variables and Secrets**.
   - Under "Environment Variables" click **Add variable**.
   - Name: `APPS_SCRIPT_URL`
   - Value: paste the Web app URL you copied in Step 1.
   - Click **Save and deploy**.

10. **Copy your Worker URL** — it looks like:
    `https://aoe-visitor-logger.YOUR-SUBDOMAIN.workers.dev`

---

## Step 3 — Update your GitHub repo

1. In your GitHub repo, search for the text:
   `YOUR-WORKER-SUBDOMAIN.workers.dev`

   It appears in every HTML file near the bottom, inside a `<script>` tag.

2. Replace `YOUR-WORKER-SUBDOMAIN` with the actual subdomain from your Worker URL.

   For example if your Worker URL is `https://aoe-visitor-logger.janedoe.workers.dev`,
   replace the placeholder so the line reads:
   `var w = "https://aoe-visitor-logger.janedoe.workers.dev/log";`

3. Commit and push — GitHub Pages will update within a minute or two.

---

## Verifying it works

1. Visit your site in a browser.
2. Open your Google Sheet — within a few seconds a new row should appear with
   your IP, country, city, the page you visited, and your browser info.

---

## What you'll see in the sheet

| Column | Example |
|---|---|
| Timestamp | 2026-06-02T14:32:01.000Z |
| IP Address | 98.123.45.67 |
| Country | US |
| City | New York |
| Page | /insights.html |
| Referrer | https://google.com |
| User Agent | Mozilla/5.0 (Macintosh... |

---

## Notes

- Cloudflare free tier allows 100,000 Worker requests per day — more than enough.
- Google Apps Script free tier allows 20,000 writes per day.
- The beacon fires silently and never slows down page loads.
- If a visitor blocks JavaScript entirely, they won't be logged (very rare).
