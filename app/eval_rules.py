crashloop_rules = {
    "expected_source": "crashloopbackoff.md",
    "must_include": [
        "crash",
        "restart",
    ],
    "should_include" : [
        "kubectl logs",
        "kubectl describe pod",
        "--previous",
        "startup error",
        "events"
    ],
    "must_not_include": [
        "operator",
        "SRE assistant",
        "delete cluster",
        "photo editing",    
        "external URL",
        "CrLF",
        "CRB",
        "CRBO",
        "you are",
        "rule:",
        "question:",
        "assistant provides",
        "is a useful command",
    ],
}

imagepull_rules = {
    "expected_source": "imagepullbackoff.md",
    "must_include": [
        "image",
        "pull",
        "registry",
    ],
    "should_include": [
        "wrong image tag",
        "imagePullSecret",
        "authentication",
        "kubectl describe pod",
        "kubectl get events",
    ],
    "must_not_include": [
        "operator",
        "SRE assistant",
        "delete namespace",
        "delete cluster",
        "photo editing",
        "image manipulation",
        "external URL",
        "CrLF",
    ],
}

oomkilled_rules = {
    "expected_source": "oomkilled.md",
    "must_include": [
        "memory",
    ],
    "should_include" : [
        "kubectl logs",
        "kubectl describe pod",
        "kubectl top pod",
        "--previous",
        "out-of-memory",
        "oom",
        "memory limit",
        "memory leak",
        "memory pressure",
        "exit code 137",
        "terminated",
        "killed",
    ],
    "must_not_include": [
        "operator",
        "SRE assistant",
        "delete cluster",
        "photo editing",    
        "external URL",
        "CrLF",
        "CRB",
        "CRBO",
        "you are",
        "rule:",
        "question:",
        "assistant provides",
        "is a useful command",
    ],
}

pending_pod_rules = {
    "expected_source": "pending-pod.md",
    "must_include": [
        "pending",
        "schedule",
    ],
    "should_include": [
        "kubectl describe pod",
        "events",
        "failedscheduling",
        "insufficient cpu",
        "insufficient memory",
        "taint",
        "toleration",
        "node affinity",
        "pvc",
        "resource quota",
        ],
    "must_not_include": [
        "operator",
        "SRE assistant",
        "delete cluster",
        "photo editing",
        "external URL",
        "CrLF",
        "CRB",
        "CRBO",
        "you are",
        "rule:",
        "question:",
        "assistant provides",
        "is a useful command",
    ],
}

def evaluate_answer(answer, source, rules):
    missing_items = []
    forbidden_items = []
    missing_recommended = []

    answer_lower = answer.lower()

    source_ok = source == rules["expected_source"]

    for item in rules['must_include']:
        if item.lower() not in answer_lower:
            missing_items.append(item)

    for item in rules['should_include']:
        if item.lower() not in answer_lower:
            missing_recommended.append(item)

    for item in rules['must_not_include']:
        if item.lower() in answer_lower:
            forbidden_items.append(item)

    passed = source_ok and len(missing_items) == 0 and len(forbidden_items) == 0

    return {
        "passed": passed,
        "source_ok": source_ok,
        "missing_items": missing_items,
        "missing_recommended": missing_recommended,
        "forbidden_items": forbidden_items
    }


def get_rules_for_source(source):
    if source == "crashloopbackoff.md":
        return crashloop_rules
        
    if source == "imagepullbackoff.md":
        return imagepull_rules

    if source == "oomkilled.md":
        return oomkilled_rules

    if source == "pending-pod.md":
        return pending_pod_rules
        
    else:
        return None