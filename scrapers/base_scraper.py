from abc import ABC, abstractmethod    # ABC ==> Abstract base classes(design by contract)
from typing import List, Dict
import requests

class BaseScraper(ABC):
    """
    Abstract Base Class for all company scrapers.
    Enforces a standardized contract across different job portals.
    """
    
    def __init__(self, company_name: str, base_url: str):    # init constructor
        self.company_name = company_name
        self.base_url = base_url
        # Standard headers to emulate a legitimate browser request
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "        # OS type
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

    def fetch_page(self, url: str, params: dict = None) -> requests.Response:    #params ==> Query parameters Ex => (role : intern & location : Dublin)
        """
        Executes a safe GET request with configured headers and timeout.
        """
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as error:
            print(f"[{self.company_name}] Network error during fetch: {error}")
            return None

    @abstractmethod     # Contract inforcement
    def scrape_jobs(self) -> List[Dict[str, str]]:
        """
        Abstract method must be implemented by subclasses.
        Should return a list of dicts: [{'job_id': ..., 'company': ..., 'title': ..., 'link': ...}]
        """
        pass