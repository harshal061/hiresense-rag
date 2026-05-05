from llm_engine import evaluate_candidate
import json
import re


# GROUP CHUNKS BY CANDIDATE
def group_by_candidate(results):
    grouped = {}

    for r in results:
        name = r["candidate_name"]

        if name not in grouped:
            grouped[name] = []

        grouped[name].append(r["chunk_text"])

    return grouped


# BUILD CONTEXT (combine chunks)
def build_candidate_context(grouped_data):
    candidate_contexts = {}

    for name, chunks in grouped_data.items():
        combined_text = " ".join(chunks[:3])  # limit size
        candidate_contexts[name] = combined_text

    return candidate_contexts


# EXTRACT SCORE FROM LLM OUTPUT
def extract_score(analysis):
    try:
        json_match = re.search(r"\{.*\}", analysis, re.DOTALL)
        data = json.loads(json_match.group())
        return data.get("score", 0)
    except:
        return 0


# RANK CANDIDATES
def rank_candidates(query, candidate_contexts):

    results = []

    for name, context in candidate_contexts.items():

        response = evaluate_candidate(query, context)

        results.append({
            "candidate": name,
            "analysis": response
        })

    # SORT BY SCORE 
    results.sort(key=lambda x: extract_score(x["analysis"]), reverse=True)

    return results