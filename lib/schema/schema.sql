CREATE TABLE IF NOT EXISTS member (
    mem_id INTEGER PRIMARY KEY,    -- Member ID
    mem_name TEXT NOT NULL,        -- Member username 
    mem_roles TEXT NOT NULL,       -- Roles 
    mem_date_join TEXT NOT NULL,   -- Day joined server
    mem_isbot TEXT NOT NULL        -- Is a bot?
);

CREATE TABLE IF NOT EXISTS attachment(
    att_id INTERGER PRIMARY KEY,    -- Attachment ID
    att_filename TEXT NOT NULL,     -- File name
    att_created_date TEXT NOT NULL, -- Date created
    att_type TEXT NOT NULL,         -- Media type
    att_scr TEXT NOT NULL           -- Source    
);

CREATE TABLE IF NOT EXISTS task(
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,     -- Task ID
    task_memid INTEGER NOT NULL,             -- Member ID
    task_content TEXT NOT NULL,              -- Task content
    task_date TEXT NOT NULL            -- Schedule date
);

