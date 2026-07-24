## flow:
- step 1: main.py is invoked
- step 2: check if model exists or not
- step 3: if yes, selects the appropritate runbook based on question asked
- step 4: read the selected runbook
- step 5: do some printing...
- step 6: call the model [prompt is built within this call]
- step 7: request is made to chat completion model
- step 8: JSON response is returned and parsed

## notes
- current model is not reliable and unstable as we can see from evaluation script.
- pass rate varies from 20% to 80%
- model is also not following the prompt completely and accurately.
- the model is weak used for experiment and learning purpose only, not a production grade model.
- model also hallucinates, core answer quality also varies accross significant runs.

## model checksum
shasum -a 256 /Users/gd06tf/Downloads/personal/models/qwen2.5-7b-instruct-q4_k_m.gguf
1875fb29e8c91c86615c00e92d8b4114e56bc24359adb5a8db8b36452fae4a49  /Users/gd06tf/Downloads/personal/models/qwen2.5-7b-instruct-q4_k_m.gguf

## new model achievements
- Qwen2.5-7B-Instruct-Q4_K_M significantly improves reliability over TinyLlama.
- For the CrashLoopBackOff eval, core correctness passed 5/5 runs.
- No forbidden hallucinations were detected.
- The only repeated quality gap is missing the recommended phrase "startup error".