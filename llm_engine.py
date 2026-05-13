import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def evaluate_candidate(query, context):

    prompt = f"""
    You are an AI recruiter evaluating a candidate.

    Return ONLY valid JSON.
    Do NOT include any explanation before or after the JSON.
    Do NOT include markdown.

    Job Requirement:
    {query}

    Candidate Information:
    {context}

    Instructions:
    - Strengths should be concise (1 short sentence each, no long descriptions).
    - Evaluate strictly based on the provided candidate information.
    - Do NOT assume or infer skills that are not explicitly mentioned.
    - Only mention weaknesses if they are clearly missing from the context.
    - Limit strengths to the top 3 most relevant points.
    - Be precise and concise.
    - Do not mention strengths that are not relevant to the role in the summary.

    Scoring Guidelines:
    - 9–10: Excellent match (strong alignment with all key requirements)
    - 7–8: Good match (most relevant skills present)
    - 5–6: Moderate match (some relevant skills missing)
    - below 5: Weak match

    If a critical requirement (like specific technology mentioned in the job requirement) is missing,
    you MUST reduce the score significantly.
    Missing critical skills should prevent scores above 7.
    If critical skills are missing, clearly state that the candidate is not a strong fit.
    Return strictly in this JSON format:

    {{
        "score": 0,
        "strengths": [],
        "weaknesses": [],
        "summary": ""
    }}

    Summary Rules:
    - 2–3 sentences maximum
    - Must justify the score clearly
    - Must reference actual skills from the candidate information
    - Ensure summary wording matches the score classification (Weak/Moderate/Strong).
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content
