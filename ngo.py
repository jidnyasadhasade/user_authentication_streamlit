import streamlit as st

st.set_page_config(page_title="Care & Support NGO", layout="wide")

# ---------------- DEFAULT CONTENT ----------------
vision = "To support communities and promote social well-being."
mission = "Providing education, health support, and basic needs."

statistics = [
    ("Families Supported", "900+"),
    ("Volunteers Joined", "120+"),
    ("Programs Conducted", "25+")
]

initiatives = [
    "Child Education Support",
    "Health Awareness Programs",
    "Food Donation Drives"
]

# ---------------- SIDEBAR ----------------
page = st.sidebar.selectbox(
    "Navigation",
    ["Home Page", "Admin Dashboard"]
)

# ---------------- HOME PAGE ----------------
if page == "Home Page":
    st.title("Care & Support NGO")

    st.subheader("Vision")
    st.write(vision)

    st.subheader("Mission")
    st.write(mission)

    st.subheader("Our Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric(statistics[0][0], statistics[0][1])
    col2.metric(statistics[1][0], statistics[1][1])
    col3.metric(statistics[2][0], statistics[2][1])

    st.subheader("Our Initiatives")
    for item in initiatives:
        st.write("•", item)

    st.markdown("---")
    st.write("📧 Contact: caresupport@ngo.org")

# ---------------- ADMIN DASHBOARD ----------------
elif page == "Admin Dashboard":
    st.title("Admin Dashboard")

    st.subheader("Edit Vision & Mission")
    new_vision = st.text_area("Vision", vision)
    new_mission = st.text_area("Mission", mission)

    if st.button("Update Vision & Mission"):
        vision = new_vision
        mission = new_mission
        st.success("Vision and Mission updated (runtime only)")

    st.subheader("Update Statistics")
    for i in range(len(statistics)):
        statistics[i] = (
            statistics[i][0],
            st.text_input(statistics[i][0], statistics[i][1])
        )

    if st.button("Save Statistics"):
        st.success("Statistics updated (runtime only)")

    st.subheader("Add New Initiative")
    new_init = st.text_input("Initiative Name")

    if st.button("Add Initiative"):
        if new_init:
            initiatives.append(new_init)
            st.success("Initiative added (runtime only)")