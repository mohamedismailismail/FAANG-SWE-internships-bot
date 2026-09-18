import uuid
from typing import List, Dict
try:
    from scrapers.base_scraper import BaseScraper
except ImportError:
    from base_scraper import BaseScraper


class UnifiedScraper(BaseScraper):
    TARGET_COMPANIES = {"google", "meta", "amazon", "apple", "microsoft", "netflix"}

    # Software Engineering keywords to match
    SOFTWARE_KEYWORDS = {
        "software", "swe", "sde", "developer", "backend"
        "frontend", "full stack", "fullstack", "step", "sre", 
        "site reliability", "cloud", "devops", "systems software"
    }

    # Irrelevant disciplines to explicitly reject
    EXCLUDE_KEYWORDS = {
        "hardware", "mechanical", "electrical", "silicon", "optical", 
        "analog", "acoustic", "rf", "pmu", "materials", "instrumentation"
    }

    def __init__(self):
        super().__init__(
            company_name="TechAggregator",
            base_url="https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/.github/scripts/listings.json"
        )

    def _is_pure_software(self, title: str) -> bool:
        """Ensures the job is strictly a Software Engineering internship."""
        title_lower = title.lower()

        # Reject hardware & non-software engineering disciplines
        if any(bad_word in title_lower for bad_word in self.EXCLUDE_KEYWORDS):
            return False

        # Match approved software keywords
        return any(good_word in title_lower for good_word in self.SOFTWARE_KEYWORDS)

    def scrape_jobs(self) -> List[Dict[str, str]]:
        response = self.fetch_page(self.base_url)
        if not response:
            return []

        try:
            postings = response.json()
        except ValueError:
            return []

        extracted_jobs = []

        for item in postings:
            if not item.get("active", True):
                continue

            company = item.get("company_name", "").strip()
            is_target_company = any(target in company.lower() for target in self.TARGET_COMPANIES)
            if not is_target_company:
                continue

            title = item.get("title", "")
            
            # Apply strict software filtering
            if not self._is_pure_software(title):
                continue

            url = item.get("url", "")
            raw_id = item.get("id") or str(uuid.uuid5(uuid.NAMESPACE_URL, url))

            extracted_jobs.append({
                "job_id": f"job-{raw_id[:16]}",
                "company": company,
                "title": title,
                "link": url
            })

        print(f"[{self.company_name}] Extracted {len(extracted_jobs)} strict Software Engineering internships.")
        return extracted_jobs