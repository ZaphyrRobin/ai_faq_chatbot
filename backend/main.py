import argparse
import asyncio
import logging
from api.logics import router
from db.database import clear_all_embeddings
from db.database import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.chatbot import get_answer
from utils.web_crawler import AsyncWebCrawler

# For APIs
app = FastAPI()
app.include_router(router, prefix="/api")
origins = [
    "http://localhost:5173", # Vite dev server
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    # Web crawler
    if urls:
        clear_all_embeddings() # Optional: clear all embeddings

        web_crawler = AsyncWebCrawler(urls.split(","))
        await web_crawler.embed_all()

    # Calling LLM to get the answer
    answer = get_answer(question)
    logger.info(f"\nQuestion: {question} \n\nAnswer: {answer}")


if __name__ == "__main__":
    asyncio.run(main())
