from app.retrieval import select_runbook
from retrieval_test_cases import SEMANTIC_RETRIEVAL_TEST_CASES
from app.semantic_retrieval import semantic_retrieve

TEST_CASES = [
    {
        "question": "image cannot be pulled from registry",
        "expected_status": "selected",
        "expected_path": "docs/imagepullbackoff.md",
    },
    {
        "question": "how to renew ssl certificate",
        "expected_status": "no_match",
        "expected_path": None,
    },
    {
        "question": "my pod keeps restarting again and again",
        "expected_status": "ambiguous",
        "expected_path": "docs/crashloopbackoff.md",  # maybe flexible later
    },
]

def main():
    passed_count = 0
    total = len(SEMANTIC_RETRIEVAL_TEST_CASES)

    for index, test_case in enumerate(SEMANTIC_RETRIEVAL_TEST_CASES, start=1):
        question = test_case["question"]
        expected_runbook = test_case["expected_runbook"]

        result = select_runbook(question)
        selected_path = result["selected_path"]

        actual_runbook = selected_path.name if selected_path else None

        passed = actual_runbook == expected_runbook

        if passed:
            passed_count += 1

        print(f"\nTest {index}")
        print("Question:", question)
        print("Expected:", expected_runbook)
        print("Actual:", actual_runbook)
        print("Status:", result["status"])
        print("Confidence:", result["confidence"])
        print("Scores:", result["scores"])
        print("Passed:", passed)

    pass_rate = passed_count / total * 100

    print("\n==== Semantic Retrieval Eval Summary ====")
    print("Total tests:", total)
    print("Passed:", passed_count)
    print(f"Pass rate: {pass_rate:.1f}%")

for test_case in TEST_CASES:
    print("=============================================")
    result = semantic_retrieve(test_case['question'])
    print("Question: ",test_case['question'])
    print("Expected status: ",test_case['expected_status'])
    print("Actual Status: ",result['status'])
    print("Expected path: ",test_case['expected_path'])
    print("Actual path: ",result['selected_path'])
    print("=============================================")

    if test_case['expected_status'] == "selected":
        if test_case['expected_status'] == result['status'] and test_case['expected_path'] == result['selected_path']:
            pass_fail = "PASSED"
            print(pass_fail)
        else:
            pass_fail = "FAILED"
            print(pass_fail)

    elif test_case['expected_status'] == "no_match":
        if test_case['expected_status'] == result['status'] == "no_match" and test_case['expected_path'] == result['selected_path'] == None:
            pass_fail = "PASSED"
            print(pass_fail)
        else:
            pass_fail = "FAILED"
            print(pass_fail)
    elif test_case['expected_status'] == "ambiguous":
        if test_case['expected_status'] == result['status'] == "ambiguous":
            pass_fail = "PASSED"
            print(pass_fail)
        else:
            pass_fail = "FAILED"
            print(pass_fail)       

## calculating pass rate
counter = 0
for test_case in range(len(TEST_CASES)):
    if pass_fail == "PASSED":
        counter += 1
print("Total tests: ",len(TEST_CASES))
print("Passed tests: ",counter)
print("Failed tests: ", len(TEST_CASES) - counter)
print("Pass rate %: ", (counter/len(TEST_CASES))*100)


if __name__ == "__main__":
    main()