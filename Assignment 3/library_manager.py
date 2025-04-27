import streamlit as st
import json
import os

# Load and save functions
def load_library(filename="library.txt"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []

def save_library(library, filename="library.txt"):
    with open(filename, "w") as file:
        json.dump(library, file, indent=4)

# Add a book
def add_book_form(library):
    with st.form("Add Book"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.text_input("Publication Year")
        genre = st.text_input("Genre")
        read = st.selectbox("Have you read it?", ["yes", "no"])
        submitted = st.form_submit_button("Add Book")

        if submitted:
            try:
                year = int(year)
                book = {
                    "title": title,
                    "author": author,
                    "year": year,
                    "genre": genre,
                    "read": read.lower() == "yes"
                }
                library.append(book)
                save_library(library)
                st.success("✅ Book added successfully!")
            except ValueError:
                st.error("❌ Year must be a number.")

# Remove a book
def remove_book_form(library):
    titles = [book['title'] for book in library]
    if titles:
        selected = st.selectbox("Select book to remove", titles)
        if st.button("Remove Book"):
            for book in library:
                if book["title"] == selected:
                    library.remove(book)
                    save_library(library)
                    st.success(f"✅ Removed: {selected}")
                    break
    else:
        st.info("Library is empty.")

# Search books
def search_books(library):
    st.subheader("🔍 Search Books")
    option = st.radio("Search by", ("Title", "Author"))
    keyword = st.text_input("Enter keyword")
    if keyword:
        if option == "Title":
            matches = [b for b in library if keyword.lower() in b["title"].lower()]
        else:
            matches = [b for b in library if keyword.lower() in b["author"].lower()]
        
        if matches:
            st.write("### 📚 Matching Books")
            for idx, book in enumerate(matches, 1):
                display_book(book, idx)
        else:
            st.warning("No matching books found.")

# Display all books
def display_books(library):
    st.subheader("📚 Your Library")
    if not library:
        st.info("Library is empty.")
    for idx, book in enumerate(library, 1):
        display_book(book, idx)

# Display a single book
def display_book(book, idx):
    read_status = "✅ Read" if book["read"] else "📖 Unread"
    st.markdown(f"**{idx}. {book['title']}** by *{book['author']}* ({book['year']}) — *{book['genre']}* — {read_status}")

# Display statistics
def display_statistics(library):
    st.subheader("📊 Library Statistics")
    total = len(library)
    if total == 0:
        st.info("No books in library.")
    else:
        read_count = sum(1 for b in library if b["read"])
        percent = (read_count / total) * 100
        st.metric("Total Books", total)
        st.metric("Books Read", f"{read_count} ({percent:.1f}%)")

# Main Streamlit app
def main():
    st.title("📘 Personal Library Manager")

    # Load session state library
    if 'library' not in st.session_state:
        st.session_state.library = load_library()

    menu = st.sidebar.radio("Menu", [
        "Add Book",
        "Remove Book",
        "Search",
        "View All Books",
        "Statistics"
    ])

    if menu == "Add Book":
        add_book_form(st.session_state.library)
    elif menu == "Remove Book":
        remove_book_form(st.session_state.library)
    elif menu == "Search":
        search_books(st.session_state.library)
    elif menu == "View All Books":
        display_books(st.session_state.library)
    elif menu == "Statistics":
        display_statistics(st.session_state.library)

# Run app
if __name__ == "__main__":
    main()
