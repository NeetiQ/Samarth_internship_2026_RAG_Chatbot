import asyncio
import os
import sys

from dotenv import load_dotenv
load_dotenv(".env")

sys.path.append("backend")

from app.database.session import AsyncSessionLocal
from app.services.rag.rag_service import RagService

async def test():
    async with AsyncSessionLocal() as db:
        rag = RagService(db)
        ans, cit = await rag.generate_response("what is the scope of section 319 CrPC", [], [])
        print("Answer:", ans.content)
        print("Citations:", len(cit))

if __name__ == "__main__":
    asyncio.run(test())
