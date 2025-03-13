# 📚 Library Management System (LMS)

The **Library Management System (LMS)** is a Python-based desktop application built using **PyQt5** for the graphical
user interface (UI) and **PostgreSQL** as the backend database. This application helps users manage a library by keeping
track of books, members, and borrowing transactions.

The application follows a **three-layer architecture** for better modularity and maintainability.

---

## 🏛 Application Architecture

The project is structured based on the **three-layer architecture**, consisting of:

1. **UI Layer**:
    - Contains the graphical user interface built using **PyQt5**.
    - Responsible for handling user interaction and displaying data.

2. **Controller Layer**:
    - Acts as the bridge between the UI and the repository layer.
    - Contains the application’s business logic, processes user inputs, and interacts with the repository.

3. **Repository Layer**:
    - Handles data storage and retrieval using **PostgreSQL**.
    - Provides a clean interface for data operations (CRUD) on the database.

---

## 📋 Features

- Add, update, and delete books and members.
- Track borrowing and return history.
- Simple and intuitive PyQt5-based user interface.
- PostgreSQL database for persistent data storage.
- Modular architecture for scalability and easy maintenance.



