# v7.1 Fix

Fixed Streamlit/Pandas compatibility issue:

- Replaced deprecated `Styler.applymap()` usage with `Styler.map()` fallback logic.
- Prevents AttributeError on Streamlit Cloud deployments using newer pandas versions.
