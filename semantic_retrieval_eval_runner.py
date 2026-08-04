from app.retrieval import select_runbook
from retrieval_test_cases import SEMANTIC_RETRIEVAL_TEST_CASES

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


if __name__ == "__main__":
    main()