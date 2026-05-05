from parser import extract_text, clean_text
from chunker import chunk_text

def process_resume(pdf_file, candidate_name, resume_id):
    
    # Step 1: Extract
    text = extract_text(pdf_file)

    # Step 2: Clean
    text = clean_text(text)

    # Step 3: Chunk
    chunks = chunk_text(text)




    IMPORTANT_KEYWORDS = ["python", "django", "sql", "aws", "testing", "selenium", "pytest"]

    processed_data = []

    for chunk in chunks:

        # skip very small chunks
        if len(chunk.split()) < 30:
            continue

        # keep only meaningful chunks
        if not any(word in chunk for word in IMPORTANT_KEYWORDS):
            continue

        processed_data.append({
            "candidate_name": candidate_name,
            "resume_id": resume_id,
            "chunk_text": chunk
        })

    return processed_data