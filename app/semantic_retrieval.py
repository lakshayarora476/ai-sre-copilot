from pathlib import Path
import math
from app.embedding_client import get_embedding

DOCS_DIR = Path("docs")
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

def cosine_similarity(a, b):
    result_dot_product = math.sumprod(a,b)

    length_a = math.hypot(*a)
    length_b = math.hypot(*b)
    if length_a == 0 or length_b == 0:
        return 0.0
    similarity = result_dot_product / (length_a * length_b)
    return similarity


def load_runbooks():
    runbooks = []
    for path in DOCS_DIR.glob("*.md"):
        content = path.read_text(encoding="utf-8")
        runbooks.append(
            {
                "path": str(path),
                "content": content,
            }
        )

    return runbooks


def retrieve_semantic(question):
    question_embedding = get_embedding(question)
    runbooks = load_runbooks()

    results = []

    for runbook in runbooks:
        file_name = Path(runbook["path"]).name
        retrieval_text = RUNBOOK_RETRIEVAL_TEXT[file_name]
        doc_embedding = get_embedding(retrieval_text)
        score = cosine_similarity(question_embedding, doc_embedding)

        results.append(
            {
                "path": runbook["path"],
                "score": score,
            }
        )

    results.sort(key=lambda item: item["score"], reverse=True)

    best = results[0]

    return {
        "selected_path": best["path"],
        "score": best["score"],
        "status": "selected",
        "results": results,
    }