-- Users table
create table users (
  id uuid primary key,
  name text,
  npub text
);

-- Conversations table
create table conversations (
  id uuid primary key,
  initial_message text,
  user_id uuid references users(id)
);

-- Messages table
create table messages (
  id uuid primary key,
  conversation_id uuid references conversations(id),
  sender text,
  message text,
  user_id uuid references users(id),
  timestamp timestamp
);
