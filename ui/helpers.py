import streamlit as st


def metric_card(title, value, help_text=""):
    st.metric(
        label=title,
        value=value,
        help=help_text
    )


def section(title):
    st.markdown(f"## {title}")