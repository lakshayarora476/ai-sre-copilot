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
        
        retrieval_result = select_runbook(question)
        if retrieval_result is None:
            print("No matching runbook found for this question")
            return        
        runbook_path = retrieval_result['selected_path']
        llm_confidence = retrieval_result['confidence']
        status = retrieval_result['status']
        scores = retrieval_result['scores']
        crashloopbackoffScore = scores['crashloopbackoff.md']
        imagepullbackoffScore = scores['imagepullbackoff.md']
        oomkilled_score = scores['oomkilled.md']

        print("Retrieval scores:")
        print("- crashloopbackoff.md: ",crashloopbackoffScore)
        print("- imagepullbackoff.md: ",imagepullbackoffScore)
        print("- oomkilled.md: ",oomkilled_score)

        print(f"Retrieval status: ",status)
        print("Retrieval confidence: ",llm_confidence)
        print(f"Selected runbook = {runbook_path}")
        
        if runbook_path is None:
            return
        runbook = read_runbook(runbook_path)
        
        #print("Model found.....\n")
        #print("Question received:\n")
        #print(question)
        #print()
        #print(f"Source: {runbook_path.name}")
        #print()
        
        final_result = call_model(question, runbook)
        # print(final_result)
        # print("Evaluation:")
        rules = get_rules_for_source(runbook_path.name)

        if rules is not None:
            eval_result = evaluate_answer(final_result,runbook_path.name, rules)
            # print(eval_result)
        else:
            print ("no evalulation rules found")
    else:
        print("Please provide a question.")
        print('Example: uv run python main.py "What is CrashLoopBackOff?"')

if __name__ == "__main__":
    main()
