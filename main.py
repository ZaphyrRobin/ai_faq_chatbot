import argparse
import asyncio
import logging
from db.database import init_db, clear_all_embeddings
from services.chatbot import get_answer
from utils.faq_crawler import AsyncWebCrawler


async def main():
    parser = argparse.ArgumentParser(description="Pass the question")
    parser.add_argument("-q", "--question", help="Input: question text", required=True)
    parser.add_argument("-u", "--urls", help="Input: web page url to crawl from, split by comma")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose (DEBUG) logging")
    args = parser.parse_args()
    
    # Setup logging based on --verbose
    if args.verbose:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        # Completely disable logging if not verbose
        logging.disable(logging.CRITICAL)
    
    logger = logging.getLogger(__name__)

    args = parser.parse_args()
    question = args.question # e.g "How to list NFT?"
    urls = args.urls # e.g "https://makersplace.com/faq/"

    init_db() # run only once actually
    clear_all_embeddings() # clear all embeddings

    # Web crawler
    if urls:
        faq_crawler = AsyncWebCrawler(urls.split(","))
        await faq_crawler.embed_all()

    # Calling LLM to get the answer
    answer = get_answer(question)
    logger.info(f"\nQuestion: {question} \n\nAnswer: {answer}")


if __name__ == "__main__":
    asyncio.run(main())
