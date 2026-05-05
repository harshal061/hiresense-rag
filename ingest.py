from resume_processor import process_resume
from embeddings.embedder import get_embedding
from vector_store.faiss_index import FAISSIndex
from vector_store.metadata_store import MetadataStore


def ingest_resume(pdf_file, candidate_name, resume_id, faiss_index, metadata_store):

    processed_data = process_resume(pdf_file, candidate_name, resume_id)

    vectors = []

    for item in processed_data:
        print("ADDING CHUNK:", item["chunk_text"][:150])
        embedding = get_embedding(item["chunk_text"])
        vectors.append(embedding)

        metadata_store.add(item)

    if faiss_index is None:
        dim = len(vectors[0])
        faiss_index = FAISSIndex(dim)

    faiss_index.add_vectors(vectors)

    return faiss_index, metadata_store