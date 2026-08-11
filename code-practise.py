import math
from pathlib import Path
from app.embedding_client import get_embedding

RUNBOOK_RETRIEVAL_TEXT = {
    "crashloopbackoff.md": """
    CrashLoopBackOff.
    Crash loop.
    Kubernetes pod crash loop.
    Pod keeps restarting.
    Pod keeps restarting again and again.
    Container repeatedly crashes after starting.
    Container starts and exits repeatedly.
    Application fails during startup.
    CrashLoopBackOff troubleshooting.
    Check container logs, previous logs, exit code, command, probes, missing environment variables, config, secrets, and application startup errors.
    """,

    "imagepullbackoff.md": """
    Kubernetes pod cannot pull container image.
    Image download from registry fails.
    ImagePullBackOff troubleshooting.
    Check image name, tag, registry access, image pull secret, and authentication.
    """,

    "oomkilled.md": """
    OOMKilled.
    Kubernetes container killed because of memory.
    Container exceeded memory limit.
    Container ran out of memory.
    Process was terminated due to memory usage.
    Pod failed because container used too much memory.
    Check memory limits, memory requests, memory leaks, application memory usage, and resource configuration.
    """,

    "pending-pod.md": """
    Pending Pod.
    Kubernetes Pending Pod.
    Pod scheduling problem.
    Pod is not scheduled.
    Pod is unscheduled.
    Pod is waiting for node assignment.
    Pod is waiting to be assigned to a node.
    Workload is waiting for node assignment.
    Scheduler cannot place the pod on any node.
    Scheduler cannot find a suitable node.
    Pod cannot start because no node was assigned.
    Check insufficient CPU, insufficient memory, taints, tolerations, node selectors, affinity, PVC binding, and node availability.
    """,
}

def cosine_similarity(a, b):
    result_dot_product = math.sumprod(a,b)

    length_a = math.hypot(*a)
    length_b = math.hypot(*b)
    if length_a == 0 or length_b == 0:
        return 0.0
    similarity = result_dot_product / (length_a * length_b)
    return similarity


def load_runbooks():
    doc_path = Path('docs')
    result = []
    for files in doc_path.rglob("*.md"):
        text = files.read_text(encoding="utf-8")
        result.append({"path" : str(files), "content" : text})
    return result

def convert_to_embedding(question):
    vector = get_embedding(question)
    return vector
#convert_to_embedding("what is k8s pod crash")

def practice_semantic_flow(question):
    question_embedding = convert_to_embedding(question)
    runbooks = load_runbooks()
    result_list = []
    for runbook in runbooks:
        result_list.append(runbook['path'])
    print("Embedding length: ",(len(question_embedding)))
    print("Runbooks path: ", result_list)
#practice_semantic_flow("what is k8s pod crash")

def embed_one_runbook():
    runbook_data = load_runbooks()
    first_runbook = runbook_data[0]
    first_runbook_content = first_runbook['content'][:1000]
    embedding = convert_to_embedding(first_runbook_content)
    print("First runbook path: ",first_runbook['path'])
    print("First runbook embedding length: ",len(embedding))
    return first_runbook['path'], embedding
#embed_one_runbook()

def compare_question_with_one_runbook(question):
    embedded_question = convert_to_embedding(question)
    runbook_path, embedded_first_runbook = embed_one_runbook()
    score = cosine_similarity(embedded_question,embedded_first_runbook)
    print("Runbook path:", runbook_path)
    print("similarity score: ", score)

#compare_question_with_one_runbook("what is crashloop")

def compare_question_with_all_runbooks(question):
    results = []
    embedded_question = convert_to_embedding(question)
    all_runbooks = load_runbooks()
    for runbook in all_runbooks:
        runbook_path = runbook['path']
        file_name = Path(runbook['path']).name
        retrieval_text = RUNBOOK_RETRIEVAL_TEXT[file_name]
        embedded_filtered_runbook = convert_to_embedding(retrieval_text)
        score = cosine_similarity(embedded_question,embedded_filtered_runbook)
        results.append({
            "path": runbook_path,
            "score": score
        })
    results = sorted(results, key=lambda item: item["score"], reverse=True)
    best = results[0]
    second_best = results[1]
    score_gap = best['score'] - second_best['score']
    minimum_score = 0.60
    if best['score'] < minimum_score:
        status = "no_match"
        confidence = "low"
    elif score_gap < 0.03:
        status = "ambiguous"
        confidence = "low"
    else:
        status = "selected"
        confidence = "high"
    selected_path = None if status == "no_match" else best["path"]
    return {
        "selected_path": selected_path,
        "status": status,
        "confidence": confidence,
        "score_gap": score_gap,
        "scores": results,
    }    
result = compare_question_with_all_runbooks("my pod keeps restarting again and again")
print(result)
