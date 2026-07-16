import os
import sys
import streamlit as st

from services.pipeline import run_pipeline
from ui.helpers import metric_card
# --------------------------------------------------------
# Fix Python Import Path
# --------------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services.pipeline import run_pipeline
from ui.helpers import metric_card

# --------------------------------------------------------
# Page Configuration
# --------------------------------------------------------

st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------------
# Session State
# --------------------------------------------------------

if "state" not in st.session_state:
    st.session_state.state = None

# --------------------------------------------------------
# Header
# --------------------------------------------------------

st.title("🔬 ResearchMind")

st.caption("AI-Powered Research Paper Analysis Platform")

st.markdown("""
ResearchMind automatically searches, downloads and analyzes research papers using AI.

It extracts scientific claims, builds knowledge graphs,
computes semantic similarity, discovers research gaps,
detects contradictions and generates novel research ideas.
""")

# --------------------------------------------------------
# Search Box
# --------------------------------------------------------

st.divider()

col1, col2 = st.columns([5, 1])

with col1:
    topic = st.text_input(
        "🔍 Research Topic",
        value="Multilingual OCR"
    )

with col2:
    st.write("")
    st.write("")
    analyze = st.button(
        "🚀 Analyze",
        use_container_width=True
    )

# --------------------------------------------------------
# Run Pipeline
# --------------------------------------------------------

if analyze:

    with st.spinner("Running ResearchMind Pipeline..."):

        state = run_pipeline(topic)

        st.session_state.state = state

    st.success("✅ Analysis Completed Successfully!")

# --------------------------------------------------------
# Dashboard
# --------------------------------------------------------

if st.session_state.state:

    state = st.session_state.state

    graph = state["knowledge_graph"]

    stats = graph.statistics()

    papers = len(state["ranked_papers"])
    ideas = len(state["research_ideas"])
    gaps = len(state["research_gaps"])
    contradictions = len(state["contradictions"])

    st.divider()

    st.subheader("📊 Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("📄 Papers", papers, "Analyzed Papers")

    with c2:
        metric_card("🕸 Nodes", stats["nodes"], "Knowledge Graph Nodes")

    with c3:
        metric_card("💡 Ideas", ideas, "Generated Ideas")

    with c4:
        metric_card("🔍 Gaps", gaps, "Detected Research Gaps")

    # --------------------------------------------------------

    st.divider()

    left, right = st.columns([2, 1])

    with left:

        st.subheader("📈 Pipeline Summary")

        st.success(f"""
✅ Papers Retrieved : {papers}

✅ Graph Nodes : {stats['nodes']}

✅ Graph Edges : {stats['edges']}

✅ Research Ideas : {ideas}

✅ Research Gaps : {gaps}

✅ Contradictions : {contradictions}
""")

    with right:

        st.subheader("⚙️ System Status")

        st.success("Backend\n\n✅ Operational")

        st.success("Pipeline\n\n✅ Completed")

        st.info(f"Current Topic\n\n{topic}")

    # --------------------------------------------------------

    st.divider()

    st.subheader("💡 Generated Research Ideas")

    if not state["research_ideas"]:

        st.warning("No research ideas generated.")

    else:

        for idea in state["research_ideas"]:

            with st.expander(idea.title):

                st.markdown(f"**Motivation**\n\n{idea.motivation}")

                st.markdown(f"**Method**\n\n{idea.proposed_method}")

                st.markdown(f"**Dataset**\n\n{idea.potential_dataset}")

                st.markdown(f"**Evaluation Metric**\n\n{idea.evaluation_metric}")

                st.markdown(f"**Contribution**\n\n{idea.expected_contribution}")

                st.progress(float(idea.confidence))

                st.caption(f"Confidence : {idea.confidence:.2f}")

    # --------------------------------------------------------

    st.divider()

    st.subheader("🔍 Research Gaps")

    if not state["research_gaps"]:

        st.success("No research gaps detected.")

    else:

        for gap in state["research_gaps"]:

            with st.expander(gap.research_area):

                st.markdown(f"**Observation**\n\n{gap.observation}")

                st.markdown(f"**Gap**\n\n{gap.gap}")

                st.markdown(f"**Opportunity**\n\n{gap.opportunity}")

                st.progress(float(gap.confidence))

                st.caption(f"Confidence : {gap.confidence:.2f}")

    # --------------------------------------------------------

    st.divider()

    st.subheader("⚠️ Contradictions")

    if contradictions == 0:

        st.success("🎉 No contradictions detected.")

    else:

        for contradiction in state["contradictions"]:

            st.error(str(contradiction))

# --------------------------------------------------------
# Footer
# --------------------------------------------------------

st.divider()

st.caption("ResearchMind v2.0 | AI-Powered Research Paper Analysis Platform")