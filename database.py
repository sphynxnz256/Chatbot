import sqlite3
import json

# Connects to or creates chatbot.db and ensures the conversations table exists
def initialize_database():
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

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

# Saves a new conversation into the database
def save_conversation(title, history, model_history):
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

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

# Updates the content and model history of an existing conversation.
def update_conversation(conversation_id, new_content, new_model_history):
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()
                  
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
    
# Retrieves a list of all conversation IDs and titles from the database.
def fetch_all_conversation_titles():
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

        cursor.execute("Select id, title FROM conversations")
        conversations = cursor.fetchall()
        return conversations
    
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Retrieves the full content and model history of a single conversation.
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
    
# Deletes a conversation from the database.
def delete_conversation(conversation_id):
    try:
        conn = sqlite3.connect("chatbot.db")
        cursor = conn.cursor()

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