import sys

from app.retrieval import read_runbook, select_runbook
from app.llm_client import call_model, model_exists
from app.eval_rules import evaluate_answer, get_rules_for_source


def main():
    if len(sys.argv) <= 1:
        print("Please provide a question.")
        print('Example: uv run python main.py "What is CrashLoopBackOff?"')
        return

    question = " ".join(sys.argv[1:])

    if not model_exists():
        print("Model server is not running")
        return

    retrieval_result = select_runbook(question)

    runbook_path = retrieval_result["selected_path"]
    scores = retrieval_result["scores"]
    status = retrieval_result["status"]
    confidence = retrieval_result["confidence"]

    print("Retrieval scores:")
    print("- crashloopbackoff.md:", scores["crashloopbackoff.md"])
    print("- imagepullbackoff.md:", scores["imagepullbackoff.md"])
    print("- oomkilled.md:", scores["oomkilled.md"])
    print("- pending-pod.md:", scores["pending-pod.md"])
    print()
    print("Retrieval status:", status)
    print("Retrieval confidence:", confidence)
    print("Selected runbook:", runbook_path)
    print()

    if runbook_path is None:
        return

    runbook = read_runbook(runbook_path)
    final_result = call_model(question, runbook)

    print("Answer:")
    print(final_result)
    print()

    rules = get_rules_for_source(runbook_path.name)

    if rules is not None:
        eval_result = evaluate_answer(final_result, runbook_path.name, rules)
        print("Evaluation:")
        print(eval_result)
    else:
        print("No evaluation rules found")


if __name__ == "__main__":
    main()