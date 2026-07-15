## flow:
- step 1: main.py is invoked
- step 2: check if model exists or not
- step 3: if yes, selects the appropritate runbook based on question asked
- step 4: read the selected runbook
- step 5: do some printing...
- step 6: call the model [prompt is built within this call]
- step 7: request is made to chat completion model
- step 8: JSON response is returned and parsed