CREATE DATABASE IF NOT EXISTS rag_chatbot;
USE rag_chatbot;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE uploaded_files (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    original_filename VARCHAR(255) NOT NULL,

    stored_filename VARCHAR(255) NOT NULL,

    file_size BIGINT NOT NULL,

    file_type VARCHAR(20) NOT NULL,


    status VARCHAR(20) NOT NULL DEFAULT 'Ready',

    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_uploaded_files_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE

);


/*
|--------------------------------------------------------------------------
| Conversations
|--------------------------------------------------------------------------
*/

CREATE TABLE conversations (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    title VARCHAR(255) DEFAULT 'New Chat',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_conversations_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE

);

/*
|--------------------------------------------------------------------------
| Chat Messages
|--------------------------------------------------------------------------
*/

CREATE TABLE chat_messages (

    id INT AUTO_INCREMENT PRIMARY KEY,

    conversation_id INT NOT NULL,

    role ENUM('user', 'assistant') NOT NULL,

    message TEXT NOT NULL,

    sources JSON DEFAULT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_chat_messages_conversation
        FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE

);
