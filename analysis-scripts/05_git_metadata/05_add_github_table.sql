CREATE TABLE github_owner (
    owner_id INTEGER PRIMARY KEY, -- TODO: check if this is the same already?! yes!! how to verify?
    owner_login TEXT NOT NULL,
    node_id TEXT NOT NULL,
    gravatar_id TEXT NOT NULL,
    type TEXT NOT NULL, -- "User", "Organization"
    site_admin BOOLEAN NOT NULL,
    name TEXT,
    company TEXT,
    blog TEXT,
    location TEXT,
    email TEXT,
    hireable BOOLEAN NOT NULL,
    bio TEXT,
    twitter_username TEXT,
    public_repos INTEGER NOT NULL,
    public_gists INTEGER NOT NULL,
    followers INTEGER NOT NULL,
    following INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE (owner_login),
    UNIQUE (node_id)
);

-- we can add this later, let's verify the import first
-- ALTER TABLE repo add FOREIGN KEY (owner_id, owner_login) REFERENCES github_owner(owner_id, owner_login)