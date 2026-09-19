# FAANG SWE Internship Autonomous Alert Pipeline

An autonomous, cloud-native scraping and alert engine designed to track Software Engineering (SWE) internship postings across FAANG and top-tier tech companies, broadcasting real-time updates directly to a Telegram channel.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?logo=githubactions)
![SQLite](https://img.shields.io/badge/SQLite-Data%20Persistence-003B57?logo=sqlite)
![Telegram API](https://img.shields.io/badge/Telegram-Bot%20API-2CA5E0?logo=telegram)
![License](https://img.shields.io/badge/License-MIT-green)

---

## System Architecture

```text
[Scheduled Trigger (Cron: 0 * * * *)]
                  │
                  ▼
       [GitHub Actions Cloud Runner]
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
 [Scraper Engine]     [SQLite State Engine]
 (Extract & Parse)     (Deduplicate via jobs.db)
        │                   │
        └─────────┬─────────┘
                  ▼
     [New SWE Postings Detected?]
         ├─► YES: [Telegram Broadcast API] ──► [Public Channel]
         │        [Commit & Push State back to Repository]
         └─► NO:  [Graceful Shutdown]
