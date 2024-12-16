# CozyNotes

CozyNotes is a simple tool I built to track my bookmarks, server details, and notes. I chose **Streamlit** because my workplace laptop has heavy software restrictions, and Streamlit works well with limited resources. This tool helps me keep everything organized with minimal effort.

The **Manage Data** section allows quick edits, but I mainly write notes in **VS Code** using markdown.

This project is open-source. Feel free to contribute and expand it in any way you want!

## Features

- **Bookmarks**: Store and access your favorite websites and credentials.
- **Server Details**: View server information like hostname and additional details.
- **Notes**: Manage markdown-based notes.
- **Minimal Design**: A clean, distraction-free interface.

## Setup Instructions

### Prerequisites

1. **Python 3.7+**
2. Install dependencies:
   ```bash
   pip install streamlit pyperclip pyyaml
   ```


### Project Structure
```
CozyNotes/
├── bookmarks.yaml         # Bookmarks and credentials.
├── server_details.json    # Server details.
├── markdown/              # Markdown notes.
├── cozyNotes.py           # Main Streamlit app.
└── README.md              # This file.
```



### Running the App

1. Clone or download the repo.
2. Run the app:
   ```bash
   streamlit run cozyNotes.py
   ```



## How to Use

- **Viewing Data**: View bookmarks, server details, and notes from the sidebar.
- **Managing Data**: Quickly add or delete data in the **Manage Data** section.



## How to Contribute

This project is open-source. Feel free to:

- Add new features like task management.
- Improve the UI.
- Fix bugs or enhance functionality.

Fork the repo, make changes, and submit a pull request.


## License
MIT License.


```
Stay Minimal, Stay Cozy!
```
