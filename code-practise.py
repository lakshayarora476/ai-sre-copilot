import math
from pathlib import Path
from app.embedding_client import get_embedding

RUNBOOK_RETRIEVAL_TEXT = {
    "crashloopbackoff.md": """
    Kubernetes pod keeps restarting repeatedly.
    Container starts then crashes again and again.
    CrashLoopBackOff troubleshooting.
    Check container logs, exit code, command, probes, and application startup errors.
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

vector1 = [1, 2, 3]
vector2 = [4, 5, 6]

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
convert_to_embedding("what is k8s pod crash")

def practice_semantic_flow(question):
    question_embedding = convert_to_embedding(question)
    runbooks = load_runbooks()
    result_list = []
    for runbook in runbooks:
        result_list.append(runbook['path'])
    print("Embedding length: ",(len(question_embedding)))
    print("Runbooks path: ", result_list)
practice_semantic_flow("what is k8s pod crash")



