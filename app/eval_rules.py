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
        "CRBO"
    ],
}

imagepull_rules = {
    "expected_source": "imagepullbackoff.md",
    "must_include": [
        "cannot pull image",
        "wrong image",
        "image does not exist",
        "wrong image tag",
        "imagePullSecret",
        "registry",
        "authentication",
        "kubectl describe pod",
        "kubectl get events",
    ],
    "should_include": [
        "imagePullSecret",
        "registry",
        "authentication",
        "kubectl describe pod",
        "kubectl get events"
    ],
    "must_not_include": [
        "operator",
        "SRE assistant",
        "delete namespace",
        "delete cluster",
        "photo editing",
        "external URL",
        "CrLF",
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

# sample_answer = """
# CrashLoopBackOff means a container crashes and Kubernetes restarts it repeatedly.
# A startup error or bad configuration can cause it.
# Useful commands include kubectl logs and kubectl describe pod.
# """

# result = evaluate_answer(
#     sample_answer,
#     "crashloopbackoff.md",
#     crashloop_rules,
# )

# print(result)

def get_rules_for_source(source):
    if source == "crashloopbackoff.md":
        return crashloop_rules
        
    elif source == "imagepullbackoff.md":
        return imagepull_rules
        
    else:
        return None