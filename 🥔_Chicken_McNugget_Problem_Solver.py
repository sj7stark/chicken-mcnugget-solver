"""Entry-point shim for the existing Streamlit Community Cloud deployment.

The deployed app on share.streamlit.io was originally created with this exact
file as its "main module," and Streamlit Cloud does not allow changing an
app's main file after creation. This shim keeps that deployment working by
importing :mod:`streamlit_app` and explicitly calling its ``main()``
function, so both entry points show the identical app.

Why the explicit call matters: Streamlit reruns the main script on every
interaction and page load, but Python caches imported modules. A bare
``import streamlit_app`` whose module-level code rendered the page would
therefore only render on the FIRST run of the server process — every rerun
after that would find the module already in ``sys.modules``, skip its code,
and produce a blank page. Calling ``streamlit_app.main()`` renders fresh on
every rerun.

For local runs, prefer:

    streamlit run streamlit_app.py

If you ever delete the Streamlit Cloud app and redeploy it with
``streamlit_app.py`` as the main file (the cleaner long-term setup), this
shim can be removed.
"""

import streamlit_app

streamlit_app.main()
