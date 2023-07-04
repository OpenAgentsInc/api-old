-- Users table
create table users (
  npub text primary key,
  name text
);

-- Conversations table
create table conversations (
  id uuid primary key,
  initial_message text,
  user_npub text references users(npub)
);

-- Messages table
create table messages (
  id uuid primary key,
  conversation_id uuid references conversations(id),
  sender text,
  message text,
  user_npub text references users(npub),
  timestamp timestamp
);
