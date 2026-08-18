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
        "expected_path": "docs/crashloopbackoff.md",
    },
    {
        "question": "pod cannot download container image",
        "expected_status": "selected",
        "expected_path": "docs/imagepullbackoff.md",
    },
    {
        "question": "scheduler cannot place my pod",
        "expected_status": "ambiguous",
        "expected_path": "docs/pending-pod.md",
    },
    {
        "question": "container is being terminated because of memory",
        "expected_status": "selected",
        "expected_path": "docs/oomkilled.md",
    },
]


def main():
    passed_tests = 0
    total_tests = len(TEST_CASES)

    for index, test_case in enumerate(TEST_CASES, start=1):
        result = semantic_retrieve(test_case["question"])

        actual_status = result["status"]
        actual_path = result["selected_path"]

        if test_case["expected_status"] == "ambiguous":
            passed = actual_status == test_case["expected_status"]
        else:
            passed = (
                actual_status == test_case["expected_status"]
                and actual_path == test_case["expected_path"]
            )

        if passed:
            passed_tests += 1

        print("=============================================")
        print("Test:", index)
        print("Question:", test_case["question"])
        print("Expected status:", test_case["expected_status"])
        print("Actual status:", actual_status)
        print("Expected path:", test_case["expected_path"])
        print("Actual path:", actual_path)
        print("Scores:", result["scores"])
        print("Passed:", passed)
        print("=============================================")

    failed_tests = total_tests - passed_tests
    pass_rate = (passed_tests / total_tests) * 100

    print("\n==== Semantic Retrieval Eval Summary ====")
    print("Total tests:", total_tests)
    print("Passed tests:", passed_tests)
    print("Failed tests:", failed_tests)
    print(f"Pass rate %: {pass_rate:.1f}")


if __name__ == "__main__":
    main()