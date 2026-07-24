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

    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    
    status VARCHAR(20) NOT NULL DEFAULT 'Ready',

    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_uploaded_files_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE

);

CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    question TEXT NOT NULL,

    answer TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_chat_history_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
