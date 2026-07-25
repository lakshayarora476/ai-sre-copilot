def build_rag_prompt(question, runbook):
    return f"""
        You are helping with Kubernetes troubleshooting.

        Use only the reference context below to answer the user question.
        Do not use outside knowledge.
        Do not describe yourself.
        Do not describe the reference context.
        Do not repeat these instructions.
        Do not invent tools, URLs, operators, commands, or concepts.
        Keep the answer short, practical, and grounded in the reference context.

        Reference context:
        {runbook}

        User question:
        {question}

        Write the final answer in this format:

        Summary:
        - Summarize the issue using only the reference context.

        Useful Commands:
        - List relevant kubectl commands from the reference context.

        Safe Next Steps:
        - List safe troubleshooting steps from the reference context.
        """