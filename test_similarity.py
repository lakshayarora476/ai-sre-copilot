from app.semantic_retrieval import retrieve_semantic


questions = [
    "my pod keeps restarting again and again",
    "container exceeded its memory limit",
    "image cannot be downloaded from registry",
    "workload is waiting for node assignment",
]

for question in questions:
    result = retrieve_semantic(question)

    print()
    print("Question:", question)
    print("Selected:", result["selected_path"])
    print("Score:", result["score"])

    print("All scores:")
    for item in result["results"]:
        print(" ", item["path"], item["score"])