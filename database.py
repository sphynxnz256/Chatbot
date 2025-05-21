import sqlite3
import json

# Function to connect to (or create) chatbot.db and ensure the conversations table exists
def initialize_database():
    try:
        conn = sqlite3.connect("chatbot.db") # Creates or opens chatbot.db
        cursor = conn.cursor()

        # Create a table to store conversations
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        model_history TEXT NOT NULL)
                        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database Error: {e}")        
    finally:
        if conn:
            conn.close()

# Function to save a conversation into the database
def save_conversation(title, history, model_history):
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        # Add a new conversation to the conversation table
        cursor.execute('''
            INSERT INTO conversations (title, content, model_history)
            VALUES (?, ?, ?)
        ''', (title, history, json.dumps(model_history)))

        conversation_id = cursor.lastrowid
        conn.commit()
        return conversation_id
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return None     
    finally:
        if conn:
            conn.close()

# Function to update the content of an existing conversation
def update_conversation(conversation_id, new_content, new_model_history):
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()
        
    # Update content of a conversaton with given id          
        cursor.execute('''
            UPDATE conversations
            SET content = ?, model_history = ?
            WHERE id = ?
            ''', (new_content, json.dumps(new_model_history), conversation_id))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        if conn:
            conn.close()
    
# Funtion to retrieve a list of all the conversation ids + titles.
def fetch_all_conversation_titles():
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        # Fetch all the titles + ids from the conversation table
        cursor.execute("Select id, title FROM conversations")
        conversations = cursor.fetchall()
        return conversations
    
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Function to retrieve the full content of a single conversation
def fetch_single_conversation(conversation_id):
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        # Fetch a single conversation based on given id
        cursor.execute("Select content, model_history FROM conversations WHERE id = ?", (conversation_id,))
        conversation = cursor.fetchone()

        if conversation:
            content = conversation[0]
            model_history = json.loads(conversation[1])
            return content, model_history
        else:
            return None, []
        
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return None, []
    finally:
        if conn:
            conn.close()
    
# Function to delete a conversation from the database
def delete_conversation(conversation_id):
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        # Delete a conversation for the given id
        cursor.execute('''
            DELETE FROM conversations
            WHERE id = ?
            ''', (conversation_id,))        
        conn.commit()

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        if conn:
            conn.close()

initialize_database()