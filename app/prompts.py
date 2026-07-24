def build_rag_prompt(question, runbook):
    return f"""
        You are helping with Kubernetes troubleshooting.

        Use the reference context to answer the user question.
        Output only the final answer.
        Do not explain the reference context.
        Do not repeat instructions.
        Keep the answer short and practical.

        Reference context:
        {runbook}

        User question:
        {question}

        Final answer format:

        Summary:
        - Summarize the issue using only the selected runbook.

        Useful Commands:
        - Include useful kubectl commands from the reference context.

        Safe Next Steps:
        - Include safe troubleshooting steps from the reference context.

        Confidence:
        - low, medium, or high
        """