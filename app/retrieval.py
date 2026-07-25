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

    crashloop_score = calculate_keyword_score(question_lower, crashloop_keywords)
    imagepull_score = calculate_keyword_score(question_lower, imagepull_keywords)
    oomkilled_score = calculate_keyword_score(question_lower, oomkilled_keywords)

    highest_score = high_score(crashloop_score,imagepull_score,oomkilled_score)
    if highest_score != None:
        if highest_score >= 2:
            confidence = "high"
        if highest_score == 1:
            confidence = "medium"
        if highest_score == 0:
            confidence = "low"
    else:
        confidence = "low"

   #if max(crashloop_score,imagepull_score,oomkilled_score) == crashloop_score and crashloop_score != 0:
    if crashloop_score > imagepull_score and crashloop_score > oomkilled_score:
        return {
            "selected_path": Path("docs/crashloopbackoff.md"),
            "scores" : {
                "crashloopbackoff.md" : crashloop_score,
                "imagepullbackoff.md" : imagepull_score,
                "oomkilled.md" : oomkilled_score
            },
            "status": "selected",
            "confidence": confidence
        }
            
    
    #if max(crashloop_score,imagepull_score,oomkilled_score) == imagepull_score and imagepull_score != 0:
    if imagepull_score > crashloop_score and imagepull_score > oomkilled_score:
        return {
            "selected_path": Path("docs/imagepullbackoff.md"),
            "scores" : {
                "imagepullbackoff.md" : imagepull_score,
                "crashloopbackoff.md" : crashloop_score,
                "oomkilled.md" : oomkilled_score
            },
            "status": "selected",
            "confidence": confidence
        }

    #if max(crashloop_score,imagepull_score,oomkilled_score) == oomkilled_score and oomkilled_score != 0:
    if oomkilled_score > crashloop_score and oomkilled_score > imagepull_score:
        return {
            "selected_path": Path("docs/oomkilled.md"),
            "scores" : {
                "oomkilled.md" : oomkilled_score,
                "imagepullbackoff.md" : imagepull_score,
                "crashloopbackoff.md" : crashloop_score
            },
            "status": "selected",
            "confidence": confidence
        }        
    
    if (imagepull_score == crashloop_score == oomkilled_score) and all([crashloop_score, imagepull_score, oomkilled_score]):
        return {
            "selected_path": None,
            "scores": {
                "crashloopbackoff.md": crashloop_score,
                "imagepullbackoff.md": imagepull_score,
                "oomkilled.md" : oomkilled_score
            },
            "status": "ambiguous",
            "confidence": "low",
            "comparison": "ambiguous"
        }
    
    if imagepull_score == 0 and crashloop_score == 0 and oomkilled_score == 0:
        return {
            "selected_path": None,
            "scores": {
                "crashloopbackoff.md": crashloop_score,
                "imagepullbackoff.md": imagepull_score,
                "oomkilled.md" : oomkilled_score
            },
            "status": "no_match",
            "confidence": "low",
            "comparison": "no match"
        }


def calculate_keyword_score(question, keywords):
    score = 0
    question_lower = question.lower()
    for item in keywords:
        if item.lower() in question_lower:
            score+=1
    return score

def high_score(crashloop_score,imagepull_score,oomkilled_score):
    if crashloop_score == 0 and imagepull_score == 0 and oomkilled_score == 0:
        return None
    else:
        return max(crashloop_score, imagepull_score, oomkilled_score)