import sys

from app.retrieval import read_runbook, select_runbook
from app.llm_client import call_model, model_exists
from app.eval_rules import evaluate_answer, get_rules_for_source

def main():
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])

        if not model_exists():
            print("Model server is not running\n")
            return
        
        runbook_path = select_runbook(question)
        print(f"Retrieval: selected runbook = {runbook_path}\n")

        if runbook_path is None:
            print("No matching runbook found for this question")
            return
        
        runbook = read_runbook(runbook_path)
        
        print("Model found.....\n")
        print("Question received:\n")
        print(question)
        print()
        print(f"Source: {runbook_path.name}")
        print()
        
        final_result = call_model(question, runbook)
        print(final_result)
        print("Evaluation:")
        rules = get_rules_for_source(runbook_path.name)

        if rules is not None:
            eval_result = evaluate_answer(final_result,runbook_path.name, rules)
            print(eval_result)
        else:
            print ("no evalulation rules found")
    else:
        print("Please provide a question.")
        print('Example: uv run python main.py "What is CrashLoopBackOff?"')

if __name__ == "__main__":
    main()
