# Running the Gemini batches

You do not need the Gemini CLI. Use the Gemini chat (web or app). This takes about 2 hours in total for about 33 batches.

For each file `batch_NN_*.md` in this folder:
1. Open a **new** Gemini chat (a fresh chat each time keeps the style varied).
2. Paste the **entire** file and send it.
3. Gemini replies with a JSON array. Copy the **whole reply** and save it, unedited, as
   `data/fragments/gemini/raw/batch_NN.json` (same NN as the prompt; create the folder if needed). Do not fix or tidy it.
4. If Gemini stops part-way, reply "continue" and append the rest to the same file, or tell Claude the batch number.

When all are saved, tell Claude. Claude validates every file, names any excerpts to re-ask, and builds the blind labelling sheet.

Please do not open `data/review/gemini_cards.json`: it states what each excerpt was meant to show. Labelling is only a fair test if you have not seen it.
The `polite_call_*` batches ask for four full-length polite calls each; they are used to measure Rapport false positives on whole calls.
