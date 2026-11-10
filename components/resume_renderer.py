import streamlit as st

from .template_modern import render_modern


def render_resume(resume_text, template="Modern"):

    if template == "Modern":
        render_modern(resume_text)