import time
from database.db import init_db, is_job_seen, save_job
from scrapers.unified_scraper import UnifiedScraper
from bot import send_telegram_alert


def format_job_message(company: str, title: str, link: str) -> str:
    return (
        f"🚨 *New FAANG Software Internship!* 🚨\n\n"
        f"🏢 *Company:* `{company}`\n"
        f"💼 *Role:* {title}\n"
        f"🔗 [Apply Directly Here]({link})\n\n"
        f"⚡ _Status: Verified SWE Posting_"
    )


def run_pipeline():
    init_db()
    scraper = UnifiedScraper()
    job_postings = scraper.scrape_jobs()

    if not job_postings:
        print("⚠️ [PIPELINE] No jobs found.")
        return

    new_jobs_count = 0

    for job in job_postings:
        job_id = job["job_id"]
        company = job["company"]
        title = job["title"]
        link = job["link"]

        if is_job_seen(job_id):
            continue

        if save_job(job_id, company, title, link):
            new_jobs_count += 1
            print(f"✨ [NEW SWE] {company} - {title}")
            message_text = format_job_message(company, title, link)
            
            if send_telegram_alert(message_text):
                time.sleep(1)

    print(f"✅ Pipeline run complete. Dispatched {new_jobs_count} new postings.\n")



if __name__ == "__main__":
    run_pipeline()