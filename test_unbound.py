import asyncio
import os
from app.service import UnboundService, ModelType
from dotenv import load_dotenv

load_dotenv()

async def test_llm():
    print("Testing Unbound API Connection...")
    api_key = os.environ.get("UNBOUND_API_KEY")
    print(f"API Key present: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"API Key (last 4 chars): ...{api_key[-4:]}")

    service = UnboundService()
    try:
        print("Sending request to Unbound (Kimi K2P5)...")
        response = await service.call_llm(
            ModelType.KIMI_K2P5, 
            "Hello, say 'API Working' if you can hear me."
        )
        print("\n✅ SUCCESS!")
        print("Response:", response['choices'][0]['message']['content'])
    except Exception as e:
        print("\n❌ FAILED!")
        print("Error details:", str(e))

if __name__ == "__main__":
    asyncio.run(test_llm())
