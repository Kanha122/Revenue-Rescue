import streamlit as st

main_file=st.Page("app.py", title="Home", icon="🏠")
generator=st.Page("churn-generator.py", title="Revenue Generator", icon="🔮")
about=st.Page("about.py", title="About Us", icon="📑")

navigate=st.navigation([main_file,generator, about])

navigate.run()
