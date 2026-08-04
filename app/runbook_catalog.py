from pathlib import Path


RUNBOOK_CATALOG = {
    "crashloopbackoff.md": {
        "path": Path("docs/crashloopbackoff.md"),
        "description": "A Kubernetes container starts, crashes, exits, and Kubernetes restarts it repeatedly with backoff delay.",
    },
    "imagepullbackoff.md": {
        "path": Path("docs/imagepullbackoff.md"),
        "description": "Kubernetes cannot pull or download a container image from a registry due to image name, tag, authentication, or imagePullSecret issues.",
    },
    "oomkilled.md": {
        "path": Path("docs/oomkilled.md"),
        "description": "A Kubernetes container uses too much memory or RAM and is terminated because it exceeds memory limits.",
    },
    "pending-pod.md": {
        "path": Path("docs/pending-pod.md"),
        "description": "A Kubernetes pod is stuck in Pending because the scheduler cannot place it on a suitable node due to resources, taints, affinity, PVC, or quota issues.",
    },
}