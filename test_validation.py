import asyncio
from app.service import UnboundService
from app.models import CompletionCriteria

async def test_validation():
    print("Testing Validation Logic...")
    service = UnboundService()
    
    # Test Case 1: Exact Match
    criteria1 = CompletionCriteria(type="contains", value="Mars")
    output1 = "This is a fact about Mars."
    result1 = await service.validate_output(output1, criteria1)
    print(f"Test 1 (Exact 'Mars'): {'✅ PASSED' if result1 else '❌ FAILED'}")

    # Test Case 2: Case Mismatch (The Bug Fix)
    criteria2 = CompletionCriteria(type="contains", value="mars")
    output2 = "This is a fact about Mars."
    result2 = await service.validate_output(output2, criteria2)
    print(f"Test 2 (Case 'mars' in 'Mars'): {'✅ PASSED' if result2 else '❌ FAILED (Fix not working)'}")

    # Test Case 3: Partial Word
    criteria3 = CompletionCriteria(type="contains", value="fail")
    output3 = "This checks for success."
    result3 = await service.validate_output(output3, criteria3)
    print(f"Test 3 (Should Fail): {'✅ PASSED (Correctly Failed)' if not result3 else '❌ FAILED (Should have failed)'}")

if __name__ == "__main__":
    asyncio.run(test_validation())
