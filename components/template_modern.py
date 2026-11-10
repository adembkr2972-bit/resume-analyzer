import streamlit as st


def render_modern(text):

    st.markdown("""
<style>

.resume{

background:white;

padding:50px;

border-radius:18px;

box-shadow:0 5px 30px rgba(0,0,0,.15);

max-width:850px;

margin:auto;

font-family:Arial;

line-height:1.8;

white-space:pre-wrap;

color:#222;

}

</style>
""",
unsafe_allow_html=True)

    st.markdown(
        f"""
<div class="resume">

{text}

</div>
""",
unsafe_allow_html=True
    )