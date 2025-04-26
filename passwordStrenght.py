import streamlit as st  # This is used to create the app (UI)
import sqlite3  # This is used to store books in a small database

# 🟢 Step 1: Create or connect to a database (library.db)
conn = sqlite3.connect("library.db", check_same_thread=False)
cursor = conn.cursor()  # This helps us talk to the database

# 🟢 Step 2: Create a "books" table (only if it doesn't exist)
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  
                    title TEXT,  
                    author TEXT,  
                    year TEXT,  
                    genre TEXT,  
                    read_status TEXT  
                )''')
conn.commit()  # Save this table inside the database

# 🟢 Step 3: Add a new book to the database
def add_book():
    st.title("📚 Add a New Book")  

    title = st.text_input("Enter book title")  
    author = st.text_input("Enter author name")  
    year = st.text_input("Enter year of publication")  
    genre = st.text_input("Enter genre")  
    read_status = st.selectbox("Have you read it?", ["True", "False"])  

    if st.button("Save Book"):  
        cursor.execute("INSERT INTO books (title, author, year, genre, read_status) VALUES (?, ?, ?, ?, ?)", 
                       (title, author, year, genre, read_status))  
        conn.commit()  
        st.success(f"✅ '{title}' added successfully!")  

# 🟢 Step 4: Remove a book from the database
def remove_book():
    st.title("🗑️ Remove a Book")

    title = st.text_input("Enter book title to remove")  

    if st.button("Remove Book"):  
        cursor.execute("DELETE FROM books WHERE title = ?", (title,))  
        conn.commit()  
        st.success(f"✅ '{title}' removed successfully!")  

# 🟢 Step 5: Show all books from the database
def show_books():
    st.title("📖 All Books in Library")

    cursor.execute("SELECT * FROM books")  
    books = cursor.fetchall()  

    if books:  
        st.table(books)  
    else:
        st.info("No books found.")  

# 🟢 Step 6: Search for a book in the database
def search_book():
    st.title("🔍 Search for a Book")

    search_by = st.selectbox("Search by", ["Title", "Author", "Genre"])  
    search_term = st.text_input("Enter search term")  

    if search_term:  
        query = f"SELECT * FROM books WHERE {search_by.lower()} LIKE ?"  
        cursor.execute(query, ('%' + search_term + '%',))  
        results = cursor.fetchall()  

        if results:  
            st.table(results)  
        else:
            st.warning("No matching books found.")  

# 🟢 Step 7: Show Library Statistics (Total books & Read books)
def show_stats():
    st.title("📊 Library Statistics")

    cursor.execute("SELECT COUNT(*) FROM books")  
    total_books = cursor.fetchone()[0]  

    cursor.execute("SELECT COUNT(*) FROM books WHERE read_status = 'True'")  
    read_books = cursor.fetchone()[0]  

    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0  

    st.metric("📚 Total Books", total_books)  
    st.metric("✅ Read Books", f"{read_percentage:.1f}%")  

# 🟢 Step 8: Sidebar for navigation
st.sidebar.title("📌 Menu")
option = st.sidebar.radio("Choose an option:", [
    "Add Book", "Remove Book", "View Books", "Search Book", "Statistics"
])

# Show the correct page based on what user selected
if option == "Add Book":
    add_book()
elif option == "Remove Book":
    remove_book()
elif option == "View Books":
    show_books()
elif option == "Search Book":
    search_book()
elif option == "Statistics":
    show_stats()