drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null
);

-- Single table called entries.
-- Each row has an id, title, and a text.
-- The id is an automatically incrementing integer and a primary key.
-- Title and text fields are strings that must not be null.
