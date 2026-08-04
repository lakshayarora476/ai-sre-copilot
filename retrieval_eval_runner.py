from app.retrieval import select_runbook


TEST_CASES = [
    {
        "question": "my pod keeps restarting",
        "expected_status": "selected",
        "expected_runbook": "crashloopbackoff.md",
    },
    {
        "question": "container cannot pull image",
        "expected_status": "selected",
        "expected_runbook": "imagepullbackoff.md",
    },
    {
        "question": "pod was oomkilled",
        "expected_status": "selected",
        "expected_runbook": "oomkilled.md",
    },
    {
        "question": "container exit code 137",
        "expected_status": "selected",
        "expected_runbook": "oomkilled.md",
    },
    {
        "question": "how to debug dns issue",
        "expected_status": "no_match",
        "expected_runbook": None,
    },
    {
        "question": "node is not ready",
        "expected_status": "no_match",
        "expected_runbook": None,
    },
    {
        "question": "pod cannot pull image and keeps restarting",
        "expected_status": "ambiguous",
        "expected_runbook": None,
    },
    {
        "question": "pod stuck in pending",
        "expected_status": "selected",
        "expected_runbook": "pending-pod.md",
    },
    {
        "question": "failed scheduling insufficient cpu",
        "expected_status": "selected",
        "expected_runbook": "pending-pod.md",
    },
    {
        "question": "pod cannot schedule because of taint",
        "expected_status": "selected",
        "expected_runbook": "pending-pod.md",
    },
    {
        "question": "pvc pending and pod not scheduled",
        "expected_status": "selected",
        "expected_runbook": "pending-pod.md",
    },
    {
        "question": "resource quota exceeded pod pending",
        "expected_status": "selected",
        "expected_runbook": "pending-pod.md",
    },    
]


def main():
    passed_count = 0

    for index, test_case in enumerate(TEST_CASES, start=1):
        question = test_case["question"]
        expected_status = test_case["expected_status"]
        expected_runbook = test_case["expected_runbook"]

        result = select_runbook(question)

        actual_status = result["status"]
        selected_path = result["selected_path"]

        if selected_path is None:
            actual_runbook = None
        else:
            actual_runbook = selected_path.name
            
        passed = (
            actual_status == expected_status
            and actual_runbook == expected_runbook
        )

        if passed:
            passed_count += 1

        print(f"\nTest {index}")
        print("Question:", question)
        print("Expected status:", expected_status)
        print("Actual status:", actual_status)
        print("Expected runbook:", expected_runbook)
        print("Actual runbook:", actual_runbook)
        print("Scores:", result["scores"])
        print("Passed:", passed)

    total = len(TEST_CASES)
    pass_rate = passed_count / total * 100

    print("\n==== Retrieval Eval Summary ====")
    print("Total tests:", total)
    print("Passed:", passed_count)
    print(f"Pass rate: {pass_rate:.1f}%")


if __name__ == "__main__":
    main()