import sys

from app.retrieval import read_runbook, select_runbook
from app.llm_client import call_model, model_exists

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
    else:
        print("Please provide a question.")
        print('Example: uv run python main.py "What is CrashLoopBackOff?"')

if __name__ == "__main__":
    main()
