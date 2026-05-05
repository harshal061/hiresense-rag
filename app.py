import streamlit as st
import json
import re

from ingest import ingest_resume
from retrieval.retriever import search_candidates
from rag.ranker import group_by_candidate, build_candidate_context, rank_candidates

st.title("HireSense AI – RAG Prototype")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if "faiss_index" not in st.session_state:
    st.session_state.faiss_index = None

if "metadata_store" not in st.session_state:
    from vector_store.metadata_store import MetadataStore
    st.session_state.metadata_store = MetadataStore()

if uploaded_file:
    st.info("Ingesting resume...")

    faiss_index, metadata_store = ingest_resume(
        uploaded_file,
        "candidate_1",
        "res_001",
        st.session_state.faiss_index,
        st.session_state.metadata_store
    )

    st.session_state.faiss_index = faiss_index
    st.session_state.metadata_store = metadata_store

    st.success("Resume stored successfully!")

# Query input
query = st.text_input("Search Candidates (e.g. Python AWS backend)")


if st.button("Search"):

    if st.session_state.faiss_index is None:
        st.error("Upload resume first!")
    else:
        results = search_candidates(
            query,
            st.session_state.faiss_index,
            st.session_state.metadata_store
        )

        grouped = group_by_candidate(results)
        contexts = build_candidate_context(grouped)

        final_results = rank_candidates(query, contexts)

        st.subheader("Ranked Candidates")



        for i, r in enumerate(final_results):
            st.write(f"### Rank #{i+1} — {r['candidate']}")

            try:
                # Extract JSON only
                json_match = re.search(r"\{.*\}", r["analysis"], re.DOTALL)
                data = json.loads(json_match.group())

                st.progress(data["score"] / 10)
                st.metric("Score", f"{data['score']} / 10")
                if data["score"] >= 8:
                    st.success("Strong Match")
                elif data["score"] >= 6:
                    st.warning("Moderate Match")
                else:
                    st.error("Weak Match")
                st.write("**Strengths:**")
                for s in data["strengths"]:
                    st.write(f"- {s}")

                st.write("**Weaknesses:**")
                if data["weaknesses"]:
                    for w in data["weaknesses"]:
                        st.write(f"- {w}")
                else:
                    st.write("No significant weaknesses identified based on the provided context.")

                st.write("**Summary:**")
                st.write(data["summary"])

            except:
                st.write(r["analysis"])

            st.write("---")