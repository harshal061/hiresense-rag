from embeddings.embedder import get_embedding



def search_candidates(query, faiss_index, metadata_store, top_k=5):

    query_vector = get_embedding(query)

    indices = faiss_index.search(query_vector, k=top_k)

    results = metadata_store.get_multiple(indices)

    # Remove duplicates
    seen = set()
    unique_results = []

    for r in results:
        text = r["chunk_text"]

        if text not in seen:
            seen.add(text)
            unique_results.append(r)

    return unique_results