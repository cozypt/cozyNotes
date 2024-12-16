import streamlit as st
import pyperclip
import yaml
import json
import os

# File paths for storing data
BOOKMARKS_FILE = 'bookmarks.yaml'
SERVER_DETAILS_FILE = 'server_details.json'
NOTES_FOLDER = 'markdown'

# Load bookmark data from YAML file
def load_bookmarks(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Load server details from JSON file
def load_server_details(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load markdown notes from a folder
def load_notes(folder_path):
    notes = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            with open(os.path.join(folder_path, filename), 'r') as file:
                notes[filename] = file.read()
    return notes

# Helper function to copy text to clipboard
def copy_to_clipboard(text):
    pyperclip.copy(text)
    st.success(f"Copied to clipboard: {text}")

# Helper function to save YAML
def save_yaml(file_path, data):
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

# Helper function to save JSON
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Helper function to save markdown note
def save_note(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# Sidebar for navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Select an Option", ["Bookmarks", "Server Details", "Notes", "Manage Data"])

# Load data
bookmark_data = load_bookmarks(BOOKMARKS_FILE)
server_details = load_server_details(SERVER_DETAILS_FILE)
notes_data = load_notes(NOTES_FOLDER)

# Main area logic based on selection
if menu == "Bookmarks":
    st.title("Bookmarks")
    categories = list(bookmark_data.keys())
    selected_category = st.sidebar.radio("Select a Category", categories)

    # Retrieve selected category data
    category_data = bookmark_data[selected_category]

    # Display websites
    if "Websites" in category_data:
        st.subheader("Websites")
        for site in category_data["Websites"]:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{site['name']}**")
            with col2:
                if st.button(f"Copy URL ({site['name']})"):
                    copy_to_clipboard(site["url"])
            with col3:
                st.markdown(f"[Open]({site['url']})", unsafe_allow_html=True)

    # Display credentials
    if "Credentials" in category_data:
        st.subheader("Credentials")
        for cred in category_data["Credentials"]:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**{cred['name']}**")
            with col2:
                if st.button(f"Copy Credential ({cred['name']})"):
                    copy_to_clipboard(cred["credential"])

elif menu == "Server Details":
    st.title("Server Details")
    # Display server details as a table
    server_table_data = []
    for server_name, server_info in server_details.items():
        server_table_data.append({
            "Server Name": server_name,
            "Details": server_info['Details'],
            "Addnl info": server_info.get('addinfo', 'N/A')
        })

    # Display the server details table
    st.table(server_table_data)

elif menu == "Notes":
    #st.title("Notes")
    # Display a unique dropdown for note selection in the sidebar
    selected_note_name = st.sidebar.selectbox("Select Note", list(notes_data.keys()))
    
    # Display the selected note content
    if selected_note_name:
        st.subheader(selected_note_name)
        st.markdown(notes_data[selected_note_name])

elif menu == "Manage Data":
    st.title("Manage Bookmarks, Server Details, and Notes")
    
    # Manage Bookmarks
    st.subheader("Manage Bookmarks")
    new_bookmark_category = st.text_input("New Bookmark Category")
    bookmark_name = st.text_input("Bookmark Name")
    bookmark_url = st.text_input("Bookmark URL")
    
    if st.button("Add Bookmark"):
        if new_bookmark_category and bookmark_name and bookmark_url:
            if new_bookmark_category not in bookmark_data:
                bookmark_data[new_bookmark_category] = {}
            if "Websites" not in bookmark_data[new_bookmark_category]:
                bookmark_data[new_bookmark_category]["Websites"] = []
            bookmark_data[new_bookmark_category]["Websites"].append({
                "name": bookmark_name,
                "url": bookmark_url
            })
            save_yaml(BOOKMARKS_FILE, bookmark_data)
            st.success("Bookmark added successfully!")
        else:
            st.error("Please fill all fields")

    # Delete Bookmark
    st.subheader("Delete Bookmark")
    bookmark_to_delete = st.selectbox("Select Bookmark to Delete", [f"{cat} - {b['name']}" for cat, data in bookmark_data.items() for b in data.get("Websites", [])])
    if st.button("Delete Bookmark"):
        category, name = bookmark_to_delete.split(" - ")
        bookmark_data[category]["Websites"] = [b for b in bookmark_data[category]["Websites"] if b["name"] != name]
        save_yaml(BOOKMARKS_FILE, bookmark_data)
        st.success(f"Bookmark {name} deleted successfully!")

    # Manage Server Details
    st.subheader("Manage Server Details")
    server_name = st.text_input("Server Name")
    server_host = st.text_input("Server Host Name")
    server_addinfo = st.text_input("Additional Info")
    
    if st.button("Add Server"):
        if server_name and server_host:
            server_details[server_name] = {
                "HostName": server_host,
                "Details": "Details not provided",
                "addinfo": server_addinfo or "N/A"
            }
            save_json(SERVER_DETAILS_FILE, server_details)
            st.success("Server details added successfully!")
        else:
            st.error("Please fill all fields")

    # Delete Server
    st.subheader("Delete Server")
    server_to_delete = st.selectbox("Select Server to Delete", list(server_details.keys()))
    if st.button("Delete Server"):
        del server_details[server_to_delete]
        save_json(SERVER_DETAILS_FILE, server_details)
        st.success(f"Server {server_to_delete} deleted successfully!")

    # Manage Notes
    st.subheader("Manage Notes")
    note_name = st.text_input("Note Name")
    note_content = st.text_area("Note Content")
    
    if st.button("Add Note"):
        if note_name and note_content:
            note_path = os.path.join(NOTES_FOLDER, f"{note_name}.md")
            save_note(note_path, note_content)
            st.success(f"Note '{note_name}' added successfully!")
        else:
            st.error("Please fill all fields")

    # Delete Note
    st.subheader("Delete Note")
    note_to_delete = st.selectbox("Select Note to Delete", list(notes_data.keys()))
    if st.button("Delete Note"):
        os.remove(os.path.join(NOTES_FOLDER, note_to_delete))
        st.success(f"Note {note_to_delete} deleted successfully!")


