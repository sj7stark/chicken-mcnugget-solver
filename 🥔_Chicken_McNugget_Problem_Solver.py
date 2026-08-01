"""Entry-point shim for the existing Streamlit Community Cloud deployment.

The deployed app on share.streamlit.io was originally created with this exact
file as its "main module," and Streamlit Cloud does not allow changing an
app's main file after creation. This shim keeps that deployment working by
simply importing :mod:`streamlit_app`, whose module-level code configures the
page and renders the landing page — so both entry points show the identical
app.

For local runs, prefer:

    streamlit run streamlit_app.py

If you ever delete the Streamlit Cloud app and redeploy it with
``streamlit_app.py`` as the main file (the cleaner long-term setup), this
shim can be removed.
"""

import streamlit_app  # noqa: F401  (importing executes the landing page)
