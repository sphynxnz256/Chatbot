import sqlite3

# Function to connect to (or create) chatbot.db and ensure the conversations table exists
def initialize_database():
    conn = sqlite3.connect("chatbot.db") # Creates or opens chatbot.db
    cursor = conn.cursor()

    # Create a table to store conversations
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS conversations (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   content TEXT
                   )
                   ''')
    
    conn.commit()
    conn.close()

# Function to save a conversation into the database
def save_conversation(title, history):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    # Add a new conversation to the conversation table
    cursor.execute('''
        INSERT INTO conversations (title, content)
        VALUES (?, ?)
    ''', (title, history))

    conn.commit()
    conn.close()

# Function to update the content of an existing conversation
def update_conversation(conversation_id, new_content):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    # Update content of a conversaton with given id
    cursor.execute('''
        UPDATE conversations
        SET content = ?
        WHERE id = ?
        ''', (new_content, conversation_id))
    
    conn.commit()
    conn.close()
    
# Funtion to retrieve a list of all the conversation ids + titles.
def fetch_all_conversation_titles():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    # Fetch all the titles + ids from the conversation table
    cursor.execute("Select id, title FROM conversations")
    conversations = cursor.fetchall()

    conn.close()

    return conversations

# Function to retrieve the full content of a single conversation
def fetch_single_conversation(conversation_id):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    # Fetch a single conversation based on given id
    cursor.execute("Select content FROM conversations WHERE id = ?", (conversation_id,))
    conversation = cursor.fetchone()

    conn.close()

    if conversation:
        return conversation[0]
    else:
        return None
    
# Function to delete a conversation from the database
def delete_conversation(conversation_id):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    # Delete a conversation for the given id
    cursor.execute('''
        DELETE FROM conversations
        WHERE id = ?
        ''', (conversation_id,))
    
    conn.commit()
    conn.close()