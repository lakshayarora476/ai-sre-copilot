from pathlib import Path


def read_runbook(runbook_path):
    return runbook_path.read_text()


def calculate_keyword_score(question, keywords):
    score = 0
    question_lower = question.lower()

    for item in keywords:
        if item.lower() in question_lower:
            score += 1

    return score


def get_confidence(top_score, second_score, status):
    if status in ["no_match", "ambiguous"]:
        return "low"

    if second_score > 0:
        return "medium"

    if top_score >= 2:
        return "high"

    if top_score == 1:
        return "medium"

    return "low"


def select_runbook(question):
    crashloop_keywords = [
        "crashloop",
        "crash loop",
        "pod keeps restarting",
        "container keeps restarting",
        "container crashing",
        "pod crashing",
        "restart backoff",
        "crashing repeatedly",
        "keeps restarting",
    ]

    imagepull_keywords = [
        "imagepull",
        "image pull",
        "cannot pull image",
        "can't pull image",
        "image download",
        "image tag",
        "image registry",
        "imagepullsecret",
        "registry auth",
    ]

    oomkilled_keywords = [
        "oomkilled",
        "oom killed",
        "out of memory",
        "memory limit",
        "exit code 137",
        "pod killed",
        "container killed",
        "memory usage",
        "memory leak",
        "kubectl top pod",
        "too much memory",
    ]

    pending_keywords = [
        "pending",
        "pod pending",
        "stuck pending",
        "failed scheduling",
        "failedscheduling",
        "cannot schedule",
        "not scheduled",
        "insufficient cpu",
        "insufficient memory",
        "node selector",
        "node affinity",
        "taint",
        "toleration",
        "pvc pending",
        "persistentvolumeclaim",
        "resource quota",
        "unschedulable",
    ]

    scores = {
        "crashloopbackoff.md": calculate_keyword_score(question, crashloop_keywords),
        "imagepullbackoff.md": calculate_keyword_score(question, imagepull_keywords),
        "oomkilled.md": calculate_keyword_score(question, oomkilled_keywords),
        "pending-pod.md": calculate_keyword_score(question, pending_keywords),
    }

    max_score = max(scores.values())

    if max_score == 0:
        return {
            "selected_path": None,
            "scores": scores,
            "status": "no_match",
            "confidence": "low",
        }

    top_matches = [ runbook_name for runbook_name, score in scores.items() if score == max_score ]

    if len(top_matches) > 1:
        return {
            "selected_path": None,
            "scores": scores,
            "status": "ambiguous",
            "confidence": "low",
        }

    selected_runbook = top_matches[0]

    sorted_scores = sorted(scores.values(), reverse=True)
    top_score = sorted_scores[0]
    second_score = sorted_scores[1]

    confidence = get_confidence(
        top_score=top_score,
        second_score=second_score,
        status="selected",
    )

    runbook_paths = {
        "crashloopbackoff.md": Path("docs/crashloopbackoff.md"),
        "imagepullbackoff.md": Path("docs/imagepullbackoff.md"),
        "oomkilled.md": Path("docs/oomkilled.md"),
        "pending-pod.md": Path("docs/pending-pod.md"),
    }

    return {
        "selected_path": runbook_paths[selected_runbook],
        "scores": scores,
        "status": "selected",
        "confidence": confidence,
    }