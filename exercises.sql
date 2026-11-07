CREATE TABLE IF NOT EXISTS todos(
    id INTEGER primary key,
    title TEXT NOT NULL,
    done INTEGER DEFAULT 0
);
 select title FROM todos;
 update todos set done = 1 where id = 1;
 update todos set done = 0 where id = 2;
 update todos set done = 1 where id = 3;
SELECT * FROM todos;
