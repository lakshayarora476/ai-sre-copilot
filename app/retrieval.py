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

    crashloop_score = calculate_keyword_score(question_lower, crashloop_keywords)
    imagepull_score = calculate_keyword_score(question_lower, imagepull_keywords)

    if crashloop_score > imagepull_score:
        print("CrashLoop score:", crashloop_score)
        print("ImagePull score:", imagepull_score)
        return Path("docs/crashloopbackoff.md")
    
    if imagepull_score > crashloop_score:
        print("CrashLoop score:", crashloop_score)
        print("ImagePull score:", imagepull_score)
        return Path("docs/imagepullbackoff.md")
    
    if (imagepull_score == crashloop_score) and (imagepull_score != 0) and (crashloop_score != 0):
        print("CrashLoop score:", crashloop_score)
        print("ImagePull score:", imagepull_score)
        return None
    
    if imagepull_score == 0 and crashloop_score == 0:
        print("CrashLoop score:", crashloop_score)
        print("ImagePull score:", imagepull_score)
        return None


def calculate_keyword_score(question, keywords):
    score = 0
    question_lower = question.lower()
    for item in keywords:
        if item.lower() in question_lower:
            score+=1
    return score