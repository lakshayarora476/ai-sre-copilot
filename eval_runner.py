from collections import Counter

from app.retrieval import select_runbook, read_runbook
from app.llm_client import call_model, model_exists
from app.eval_rules import evaluate_answer, get_rules_for_source


QUESTION = "pod stuck in pending"
RUNS = 5


def main():
    if not model_exists():
        print("Model server is not running")
        return

    runbook_path = select_runbook(QUESTION)
    runbook_path = runbook_path['selected_path']
    if runbook_path is None:
        print("No matching runbook found")
        return

    runbook = read_runbook(runbook_path)
    rules = get_rules_for_source(runbook_path.name)

    if rules is None:
        print("No eval rules found")
        return

    passed_count = 0
    missing_required_counter = Counter()
    missing_recommended_counter = Counter()
    forbidden_counter = Counter()

    for run_number in range(1, RUNS + 1):
        print(f"\nRun {run_number}/{RUNS}")

        answer = call_model(QUESTION, runbook)
        eval_result = evaluate_answer(answer, runbook_path.name, rules)

        print("Passed:", eval_result["passed"])
        print("Missing required:", eval_result["missing_items"])
        print("Missing recommended:", eval_result["missing_recommended"])
        print("Forbidden:", eval_result["forbidden_items"])

        if not eval_result["passed"]:
            print("Answer snippet:")
            print(answer[:500])

        if eval_result["passed"]:
            passed_count += 1

        missing_required_counter.update(eval_result["missing_items"])
        missing_recommended_counter.update(eval_result["missing_recommended"])
        forbidden_counter.update(eval_result["forbidden_items"])

    pass_rate = passed_count / RUNS * 100

    print("\n==== Summary ====")
    print("Question:", QUESTION)
    print("Runs:", RUNS)
    print("Passed:", passed_count)
    print(f"Pass rate: {pass_rate:.1f}%")

    print("\nCommon missing required:")
    print(dict(missing_required_counter))

    print("\nCommon missing recommended:")
    print(dict(missing_recommended_counter))

    print("\nForbidden items:")
    print(dict(forbidden_counter))


if __name__ == "__main__":
    main()