import streamlit as st

st.set_page_config(page_title="Authentication App", page_icon="🔒")

# ---------------- SESSION SETUP ----------------
if "users_db" not in st.session_state:
    st.session_state.users_db = {}

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None


# ---------------- FUNCTIONS ----------------
def signup():
    st.subheader("📝 User Signup")

    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")

    if st.button("Create Account"):
        if username == "" or password == "":
            st.warning("Please enter all details")
        elif username in st.session_state.users_db:
            st.error("Username already exists")
        else:
            st.session_state.users_db[username] = password
            st.success("Account created successfully")
            st.info("Go to Login page")


def login():
    st.subheader("🔑 User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users_db:
            if st.session_state.users_db[username] == password:
                st.session_state.is_logged_in = True
                st.session_state.username = username
                st.success("Login successful")
            else:
                st.error("Incorrect password")
        else:
            st.error("User not found")


def dashboard():
    st.subheader("🏠 Dashboard")
    st.success(f"Welcome {st.session_state.username}")

    st.write("You are successfully authenticated.")

    if st.button("Logout"):
        st.session_state.is_logged_in = False
        st.session_state.username = None
        st.success("Logged out successfully")


def about():
    st.subheader("📘 About")
    st.write("""
    This User Authentication Application is developed using:
    - Python
    - Streamlit

    Features:
    - User Signup
    - User Login
    - Session-based authentication
    - Logout functionality

    Created for internship assignment.
    """)


# ---------------- UI ----------------
st.title("🔐 User Authentication Application")

menu = st.sidebar.selectbox(
    "Select Option",
    ["Login", "Signup", "Dashboard", "About"]
)

if menu == "Signup":
    signup()

elif menu == "Login":
    login()

elif menu == "Dashboard":
    if st.session_state.is_logged_in:
        dashboard()
    else:
        st.warning("Please login first")

elif menu == "About":
    about()

st.markdown("---")
st.markdown("© Internship Project | Python & Streamlit")