import asyncio
import httpx
import logging
from bs4 import BeautifulSoup
from services.embedder import embed_and_store_entries
from typing import List
from typing import Tuple

logger = logging.getLogger(__name__)

class AsyncWebCrawler:
    def __init__(self, urls: List[str]):
        self.urls = urls

    async def fetch_faq(self, client: httpx.AsyncClient, url: str) -> List[Tuple[str, str]]:
        try:
            resp = await client.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            faq_entries = []

            # NOTE: Please update this logic based on the specific page crawling
            for wrapper in soup.find_all("div", class_="question-wrapper"):
                q_tag = wrapper.find("h6")
                a_tag = wrapper.find("div", class_="answer")
                if q_tag and a_tag:
                    p_tag = a_tag.find("p")
                    if p_tag:
                        question = q_tag.get_text(strip=True)
                        answer = p_tag.get_text(strip=True)
                        faq_entries.append((question, answer))
            return faq_entries
        except Exception as e:
            logger.warning(f"Failed to fetch from {url}: {e}")
            return []

    async def fetch_all(self) -> List[Tuple[str, str]]:
        async with httpx.AsyncClient() as client:
            tasks = [self.fetch_faq(client, url) for url in self.urls]
            all_results = await asyncio.gather(*tasks)
            return [entry for result in all_results for entry in result]  # flatten

    async def embed_all(self):
        entries = await self.fetch_all()
        logger.info(f"✅ Fetched {len(entries)} entries.")
        embed_and_store_entries(entries)
