import streamlit as st
import sqlite3
import os
from datetime import date

# ================= DATABASE CONNECTION =================
def get_connection():
    return sqlite3.connect("ngo_v2.db", check_same_thread=False)

conn = get_connection()
cur = conn.cursor()

# ================= CREATE TABLES =================
cur.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    status TEXT,
    start_date TEXT,
    end_date TEXT,
    location TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS project_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    image_path TEXT
)
""")

conn.commit()

# ================= UPLOAD DIRECTORY =================
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# ================= SIDEBAR =================
st.sidebar.title("NGO Management System")
page = st.sidebar.selectbox("Navigation", ["Projects", "Admin Dashboard"])
st.sidebar.info("Internship Project – Streamlit & SQLite")

# =====================================================
# ================= PROJECT DISPLAY ===================
# =====================================================
if page == "Projects":
    st.title("🌱 Our NGO Projects")
    st.caption("Creating positive impact through meaningful initiatives")

    status = st.selectbox(
        "Filter Projects by Status",
        ["All", "Ongoing", "Completed", "Upcoming"]
    )

    if status == "All":
        cur.execute("SELECT * FROM projects")
    else:
        cur.execute("SELECT * FROM projects WHERE status=?", (status,))

    data = cur.fetchall()

    if not data:
        st.warning("No projects available")
    else:
        for p in data:
            st.subheader(p[1])
            st.write(p[2])
            st.write(f"📍 **Location:** {p[6]}")
            st.write(f"📅 **Status:** {p[3]}")
            st.write(f"🗓️ **Duration:** {p[4]} to {p[5]}")

            cur.execute(
                "SELECT image_path FROM project_images WHERE project_id=?",
                (p[0],)
            )
            imgs = cur.fetchall()

            for img in imgs:
                st.image(img[0], width=280)

            st.divider()

# =====================================================
# ================= ADMIN DASHBOARD ===================
# =====================================================
if page == "Admin Dashboard":
    st.title("🔐 Admin Dashboard")

    tab1, tab2, tab3 = st.tabs(["➕ Add Project", "🖼 Upload Images", "🗑 Manage Projects"])

    # ---------- ADD PROJECT ----------
    with tab1:
        with st.form("project_form"):
            title = st.text_input("Project Title")
            desc = st.text_area("Project Description")
            status = st.selectbox("Project Status", ["Ongoing", "Completed", "Upcoming"])
            start_date = st.date_input("Start Date", date.today())
            end_date = st.date_input("End Date", date.today())
            location = st.text_input("Project Location")

            submit = st.form_submit_button("Save Project")

            if submit:
                cur.execute(
                    "INSERT INTO projects VALUES (NULL,?,?,?,?,?,?)",
                    (title, desc, status, str(start_date), str(end_date), location)
                )
                conn.commit()
                st.success("Project added successfully")

    # ---------- UPLOAD IMAGES ----------
    with tab2:
        cur.execute("SELECT id, title FROM projects")
        projects = cur.fetchall()

        if projects:
            project_map = {p[1]: p[0] for p in projects}
            selected_project = st.selectbox("Select Project", project_map.keys())
            image = st.file_uploader("Upload Project Image", type=["jpg", "png", "jpeg"])

            if st.button("Upload"):
                if image:
                    img_path = os.path.join(UPLOAD_DIR, image.name)
                    with open(img_path, "wb") as f:
                        f.write(image.read())

                    cur.execute(
                        "INSERT INTO project_images VALUES (NULL,?,?)",
                        (project_map[selected_project], img_path)
                    )
                    conn.commit()
                    st.success("Image uploaded successfully")
        else:
            st.info("Add projects first")

    # ---------- DELETE PROJECT ----------
    with tab3:
        cur.execute("SELECT id, title FROM projects")
        projects = cur.fetchall()

        if projects:
            delete_map = {p[1]: p[0] for p in projects}
            del_project = st.selectbox("Select Project to Delete", delete_map.keys())

            if st.button("Delete Project"):
                cur.execute("DELETE FROM project_images WHERE project_id=?", (delete_map[del_project],))
                cur.execute("DELETE FROM projects WHERE id=?", (delete_map[del_project],))
                conn.commit()
                st.success("Project deleted successfully")
        else:
            st.info("No projects to manage")
