SEMANTIC_RETRIEVAL_TEST_CASES = [
    {
        "question": "my app is running out of RAM",
        "expected_runbook": "oomkilled.md",
    },
    {
        "question": "container is being terminated due to memory",
        "expected_runbook": "oomkilled.md",
    },
    {
        "question": "scheduler cannot place my pod",
        "expected_runbook": "pending-pod.md",
    },
    {
        "question": "workload is waiting for a node",
        "expected_runbook": "pending-pod.md",
    },
    {
        "question": "pod cannot download container image",
        "expected_runbook": "imagepullbackoff.md",
    },
    {
        "question": "registry login is failing",
        "expected_runbook": "imagepullbackoff.md",
    },
    {
        "question": "app starts and exits immediately",
        "expected_runbook": "crashloopbackoff.md",
    },
    {
        "question": "pod restarts again and again",
        "expected_runbook": "crashloopbackoff.md",
    },
]