from pathlib import Path

def read_runbook(runbook_path):
    return runbook_path.read_text()

def select_runbook(question):
    question_lower = question.lower()

    crashloop_keywords = [
        "crashloop",
        "crash loop",
        "pod keeps restarting",
        "container keeps restarting",
        "container crashing",
        "pod crashing",
        "restart backoff",
    ]

    imagepull_keywords = [
        "imagepull",
        "image pull",
        "cannot pull image",
        "can't pull image",
        "image download",
        "pull image",
        "image tag",
        "image registry",
        "imagepullsecret",
        "registry auth",
    ]

    for keyword in crashloop_keywords:
        if keyword in question_lower:
            return Path("docs/crashloopbackoff.md")
    
    for keyword in imagepull_keywords:
        if keyword in question_lower:
            return Path("docs/imagepullbackoff.md")
    
    return None