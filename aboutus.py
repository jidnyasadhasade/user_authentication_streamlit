import streamlit as st
import sqlite3

# ---------------- DATABASE ----------------
def db_connect():
    return sqlite3.connect("ngo_about_alt.db", check_same_thread=False)

conn = db_connect()
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS about_story (text TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS about_values (value TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS about_programs (program TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS about_team (name TEXT, position TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS about_impact (detail TEXT)")
conn.commit()

# ---------------- SEED DATA ----------------
def load_defaults():
    if cur.execute("SELECT COUNT(*) FROM about_story").fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO about_story VALUES ('Our organization began with a mission to uplift society.')"
        )

    if cur.execute("SELECT COUNT(*) FROM about_values").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO about_values VALUES (?)",
            [("Integrity",), ("Commitment",), ("Social Responsibility",)]
        )

    if cur.execute("SELECT COUNT(*) FROM about_programs").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO about_programs VALUES (?)",
            [("Education Assistance",), ("Medical Outreach",), ("Skill Training",)]
        )

    if cur.execute("SELECT COUNT(*) FROM about_team").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO about_team VALUES (?, ?)",
            [("Amit Kulkarni", "Founder"), ("Pooja Deshmukh", "Project Lead")]
        )

    if cur.execute("SELECT COUNT(*) FROM about_impact").fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO about_impact VALUES (?)",
            [("3,500+ beneficiaries supported",), ("45+ initiatives completed",)]
        )

    conn.commit()

load_defaults()

# ---------------- SESSION ----------------
if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False

# ---------------- NAVIGATION ----------------
st.title("NGO About Us Portal")
menu = st.radio("Navigate", ["About Us", "Admin"], horizontal=True)

# ================= ABOUT US =================
def show_about():
    st.header("About Our NGO")
    st.write("Working towards sustainable development and inclusive growth.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Mission")
        st.write("To empower communities through education and healthcare.")
    with col2:
        st.subheader("Vision")
        st.write("Equal opportunities and dignity for everyone.")

    st.subheader("Our Journey")
    st.write(cur.execute("SELECT text FROM about_story").fetchone()[0])

    st.subheader("Core Values")
    for v in cur.execute("SELECT value FROM about_values"):
        st.markdown(f"- {v[0]}")

    st.subheader("Programs")
    for p in cur.execute("SELECT program FROM about_programs"):
        st.markdown(f"- {p[0]}")

    st.subheader("Leadership Team")
    for t in cur.execute("SELECT name, position FROM about_team"):
        st.write(f"**{t[0]}** – {t[1]}")

    st.subheader("Impact")
    for i in cur.execute("SELECT detail FROM about_impact"):
        st.markdown(f"- {i[0]}")

    st.success("Support our mission")
    c1, c2 = st.columns(2)
    with c1:
        st.button("Donate")
    with c2:
        st.button("Volunteer")

# ================= ADMIN =================
def admin_panel():
    if not st.session_state.admin_ok:
        st.subheader("Admin Login")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if u == "admin" and p == "ngo@2024":
                st.session_state.admin_ok = True
                st.success("Access granted")
            else:
                st.error("Invalid credentials")

    if st.session_state.admin_ok:
        st.subheader("Admin Dashboard")

        # Story
        story_text = st.text_area(
            "Edit Story",
            cur.execute("SELECT text FROM about_story").fetchone()[0]
        )
        if st.button("Update Story"):
            cur.execute("DELETE FROM about_story")
            cur.execute("INSERT INTO about_story VALUES (?)", (story_text,))
            conn.commit()

        # Values
        new_value = st.text_input("Add Core Value")
        if st.button("Add Value"):
            cur.execute("INSERT INTO about_values VALUES (?)", (new_value,))
            conn.commit()

        # Programs
        new_prog = st.text_input("Add Program")
        if st.button("Add Program"):
            cur.execute("INSERT INTO about_programs VALUES (?)", (new_prog,))
            conn.commit()

        # Team
        name = st.text_input("Team Member Name")
        position = st.text_input("Position")
        if st.button("Add Team"):
            cur.execute(
                "INSERT INTO about_team VALUES (?, ?)",
                (name, position)
            )
            conn.commit()

        st.success("Changes saved to database")

# ---------------- ROUTER ----------------
if menu == "About Us":
    show_about()
else:
    admin_panel()