import streamlit as st
import os
import uuid
import requests
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Api Configuration
# Use environment variable for deployment, default to localhost for dev
API_URL = os.getenv("API_URL", "http://localhost:8000")

# System Prompt
SYSTEM_PROMPT = "You are a helpful AI assistant."

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# --- Global Custom CSS ---
st.markdown("""
<style>
    /* --- General App Styling --- */
    
    /* Reduce main content width for better readability */
    .main > div {
        max-width: 800px;
        margin: auto;
    }

    /* --- Sidebar Polish --- */
    section[data-testid="stSidebar"] {
        padding-top: 2rem;
        background-color: #121212; /* Darker background */
    }
    
    /* Sidebar Buttons: Rounded & Softer Borders */
    div[data-testid="stSidebar"] button {
        border-radius: 12px !important;
        border: 1px solid #333 !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stSidebar"] button:hover {
        border-color: #555 !important;
        background-color: #262730 !important;
    }

    /* --- Chat Bubbles (User & Assistant) --- */
    
    /* User Message Bubble */
    div[data-testid="chat-message-user"] {
        background-color: #2b2c34 !important; /* Slightly lighter than bg */
        color: #ffffff !important;
        padding: 1rem;
        border-radius: 15px 15px 0 15px !important; /* Rounded with one sharp corner */
        margin-bottom: 1rem;
        border: 1px solid #3d3d3d;
        width: fit-content;
        margin-left: auto; /* Align right */
        max-width: 80%;
    }
    
    /* Assistant Message Bubble */
    div[data-testid="chat-message-assistant"] {
        background-color: #1e1e1e !important;
        color: #eeeeee !important;
        padding: 1rem;
        border-radius: 15px 15px 15px 0 !important;
        margin-bottom: 1rem;
        border: 1px solid #333;
        width: fit-content;
        margin-right: auto; /* Align left */
        max-width: 80%;
    }
    
    /* Avatar adjustments if needed */
    div[data-testid="stChatMessageAvatar"] {
        margin-top: auto;
        margin-bottom: 10px;
    }

    /* Input Fields (Login Page & Chat Input) */
    div[data-testid="stTextInput"] input {
        background-color: #1E1E1E !important;
        color: #E0E0E0 !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border: 1px solid #FF4B4B !important;
        box-shadow: none !important;
    }
    
    /* Buttons (General) */
    div[data-testid="stButton"] button {
        border-radius: 8px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-right: 20px;
    }
    
    /* Active Tab Underline */
    div[data-baseweb="tab-highlight"] {
        background-color: #FF4B4B !important;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "user" not in st.session_state:
    st.session_state.user = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "user_chats" not in st.session_state:
    st.session_state.user_chats = {} # Client-side cache for sidebar

# --- AUTHENTICATION FLOW ---
if not st.session_state.user:
    
    # --- Native Streamlit UI (No Custom CSS) ---
    
    # 50/50 Split Layout
    c1, c2 = st.columns([1, 1], gap="large")
    
    # --- Left Column: Hero Visuals ---
    with c1:
        # Title using Streamlit native component
        st.title("☺ Welcome - AI ChatRobo")
        
        # Hero Section: Text + Image
        # Using columns to place Text left and Robot right
        hero_text_col, hero_img_col = st.columns([1.5, 1], vertical_alignment="center")
        
        with hero_text_col:
            # Right-aligned text to look like speech directed at the robot
            st.markdown(
                """
                <h1 style='text-align: right; margin-right: 10px; font-size: 50px; line-height: 1.2;'>
                ASK ME<br>ANYTHING
                </h1>
                """, 
                unsafe_allow_html=True
            )
            
        with hero_img_col:
            st.image("assets/robot_saying.png", use_container_width=True)

    # --- Right Column: Auth Forms ---
    with c2:
        # Centered Robot Logo using columns
        logo_l, logo_c, logo_r = st.columns([1, 2, 1]) # Wider middle column for bigger logo
        with logo_c:
             # Process Image to be Circular using PIL (No CSS)
             from PIL import Image, ImageDraw, ImageOps
             
             try:
                 # Open Image
                 original_image = Image.open("assets/logo_circle.jpg")
                 
                 # Create Circular Mask
                 mask = Image.new("L", original_image.size, 0)
                 draw = ImageDraw.Draw(mask)
                 draw.ellipse((0, 0) + original_image.size, fill=255)
                 
                 # Apply Mask to a copy converted to RGBA
                 circular_logo = ImageOps.fit(original_image, mask.size, centering=(0.5, 0.5))
                 circular_logo.putalpha(mask)
                 
                 # Display Larger and Circular
                 st.image(circular_logo, width=220)
             except Exception as e:
                 st.error(f"Logo Error: {e}")
                 st.image("assets/logo_circle.jpg", width=220) # Fallback
        
        # Tabs
        tab_login, tab_signup = st.tabs(["Login", "Sign Up"])
        
        with tab_login:
            st.subheader("Login")
            with st.form("login_form"):
                user_login = st.text_input("Username", placeholder="Enter your username")
                pass_login = st.text_input("Password", type="password", placeholder="Enter your password")
                
                # Type='primary' uses the Red color from config
                submitted_login = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submitted_login:
                if not user_login or not pass_login:
                    st.error("Please enter credentials.")
                else:
                    try:
                        resp = requests.post(f"{API_URL}/login", json={"username": user_login, "password": pass_login})
                        if resp.status_code == 200:
                            st.session_state.user = user_login
                            st.session_state.logged_in = True
                            try:
                                h_resp = requests.get(f"{API_URL}/history/{user_login}")
                                st.session_state.user_chats = h_resp.json() if h_resp.status_code == 200 else {}
                            except:
                                st.session_state.user_chats = {}
                            st.rerun()
                        else:
                            st.error(resp.json().get('detail', 'Login failed'))
                    except Exception as e:
                        st.error(f"Connection error: {e}")

        with tab_signup:
            st.subheader("Sign Up")
            with st.form("signup_form"):
                new_user = st.text_input("New Username")
                new_pass = st.text_input("New Password", type="password")
                
                st.write("")
                submitted_signup = st.form_submit_button("Sign Up", type="primary", use_container_width=True)
                
            if submitted_signup:
                if not new_user or not new_pass:
                    st.error("Please fill out all fields.")
                else:
                    try:
                        resp = requests.post(f"{API_URL}/register", json={"username": new_user, "password": new_pass})
                        if resp.status_code == 200:
                            st.success("Account created! Please log in.")
                        else:
                            st.error(resp.json().get('detail', 'Sign up failed'))
                    except Exception as e:
                        st.error(f"Connection error: {e}")

else:
    # --- MAIN APP FLOW ---
    user = st.session_state.user
    
    # Sidebar
    with st.sidebar:
        st.title(f"👤 {user}")
        
        col_new, col_clear_btn = st.columns(2)
        with col_new:
            # New Chat Button
            if st.button("➕ New Chat", use_container_width=True, type="primary"):
                st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]
                st.session_state.current_chat_id = str(uuid.uuid4())
                st.session_state.confirm_clear = False
                st.rerun()
        with col_clear_btn:
            # Clear History Logic (Button)
            if st.button("Clear History", use_container_width=True):
                st.session_state.confirm_clear = True
        
        if st.session_state.get("confirm_clear", False):
            st.warning("Are you sure?", icon="⚠️")
            col_conf1, col_conf2 = st.columns(2)
            with col_conf1:
                if st.button("Yes", type="primary", use_container_width=True, key="confirm_yes"):
                    try:
                        requests.delete(f"{API_URL}/history/{user}")
                        st.session_state.messages = []
                        st.session_state.current_chat_id = None
                        st.session_state.user_chats = {} # Clear local cache
                        st.session_state.confirm_clear = False
                        st.rerun()
                    except:
                        st.error("Failed to clear history")
            with col_conf2:
                if st.button("No", use_container_width=True, key="confirm_no"):
                    st.session_state.confirm_clear = False
                    st.rerun()
            
        st.divider()
        st.subheader("Chat History")
        
        # Use Cached Chats (Sync on load if empty)
        if not st.session_state.user_chats and st.session_state.current_chat_id is None:
             try:
                resp = requests.get(f"{API_URL}/history/{user}")
                if resp.status_code == 200:
                    st.session_state.user_chats = resp.json()
             except: pass

        chats = st.session_state.user_chats

        # Sort chats (Reverse order for simplified LIFO visualization)
        # Using list(chats.items()) to avoid runtime changes during iteration
        for chat_id, chat_data in list(chats.items())[::-1]: 
            title = chat_data.get("title", "New Chat")
            # Highlight current chat
            if st.button(title, key=chat_id, use_container_width=True, type="secondary" if chat_id != st.session_state.current_chat_id else "primary"):
                st.session_state.current_chat_id = chat_id
                st.session_state.messages = chat_data["messages"]
                st.session_state.confirm_clear = False
                st.rerun()

        # Logout at bottom
        st.divider()
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.messages = []
            st.session_state.user_chats = {}
            st.session_state.current_chat_id = None
            st.rerun()

    # Chat Interface
    st.title("💬 Chat")
    
    # Initialize new chat if needed
    if not st.session_state.current_chat_id:
        st.session_state.current_chat_id = str(uuid.uuid4())
        # Default welcome message if completely empty
        if not st.session_state.messages:
             st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

    # Display chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            try:
                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT}
                    ] + [
                        {"role": m["role"], "content": m["content"]} 
                        for m in st.session_state.messages
                    ],
                    stream=True
                )
                
                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                # --- IMMEDIATE TITLE UPDATE & SYNC LOGIC ---
                
                # 1. Update Local Cache Immediately
                if st.session_state.current_chat_id not in st.session_state.user_chats:
                     st.session_state.user_chats[st.session_state.current_chat_id] = {"title": "New Chat", "messages": []}
                
                st.session_state.user_chats[st.session_state.current_chat_id]["messages"] = st.session_state.messages
                
                # 2. Check for Title Generation (On 1st turn)
                current_title = st.session_state.user_chats[st.session_state.current_chat_id].get("title", "New Chat")
                
                if current_title == "New Chat" and len(st.session_state.messages) >= 2:
                    # Generate Title
                    first_msg = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), "")
                    if first_msg:
                        new_title = (first_msg[:20] + '..') if len(first_msg) > 20 else first_msg
                        
                        # Update Local
                        st.session_state.user_chats[st.session_state.current_chat_id]["title"] = new_title
                        
                        # Save Async-ish (requests is sync, but we do it before rerun)
                        requests.post(f"{API_URL}/history/save", json={
                            "username": user,
                            "chat_id": st.session_state.current_chat_id,
                            "title": new_title,
                            "messages": st.session_state.messages
                        })
                        
                        # RERUN to update Sidebar Title Instantly
                        st.rerun()
                
                # 3. Save Context (If not rerunning)
                requests.post(f"{API_URL}/history/save", json={
                    "username": user,
                    "chat_id": st.session_state.current_chat_id,
                    "title": st.session_state.user_chats[st.session_state.current_chat_id].get("title", "New Chat"),
                    "messages": st.session_state.messages
                })

            except Exception as e:
                placeholder.error(f"Error: {str(e)}")
