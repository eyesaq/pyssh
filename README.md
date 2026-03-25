# pyssh

A lightweight Python toolkit for SSH automation paired with a modern GUI built using **CustomTkinter**.  
`pyssh` provides a simple interface for connecting to remote hosts, executing commands, and managing SSH workflows — all wrapped in an accessible desktop application.

---

## 🚀 Features

- 🔐 **SSH Connection Handling** using Paramiko  
- 🖥️ **Remote Command Execution** with stdout/stderr capture  
- 🎨 **Modern GUI** built with CustomTkinter  
- 🧩 Modular structure for easy extension  
- 📁 Ready for future enhancements like SFTP, host inventories, and CLI tools  

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/pyssh.git
cd pyssh
```

Install dependencies:

```bash
pip install -r requirements.txt
```

    Note:  
    tkinter is part of Python’s standard library.
    On Linux, you may need to install it via your package manager:

    ```bash
    sudo apt install python3-tk
    ```

▶️ Usage

Run the main application:

```bash
python main.py
```

This launches the GUI, where you can:

    - Enter host, username, and password
    - Connect via SSH
    - Execute commands
    - View output in real time

📁 Project Structure
Code

pyssh/
│
├── app/               # Core application logic
├── data/              # Configs or future host inventories
├── main.py            # Application entry point
├── requirements.txt   # Python dependencies
├── setup.py           # Packaging configuration
└── CHANGELOG.md       # Version history

🛠️ Requirements:

    - Python 3.10+
    - customtkinter
    - paramiko
    - Pillow

All installable via:

```bash
pip install -r requirements.txt
```