CREATE TABLE "files" (
	"id"	INTEGER UNIQUE,
	"path"	TEXT NOT NULL,
	"title"	TEXT NOT NULL,
	"extension"	TEXT NOT NULL,
	"content"	TEXT NOT NULL,
	"created_at"	TEXT NOT NULL,
	"modified_at"	TEXT NOT NULL,
	"size"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

create virtual table files_fts using fts5(
	id, path, title, extension, content
);

CREATE TRIGGER update_files_fts
after update on files
BEGIN
	update files_fts
	set 
		id = NEW.id,
		path = NEW.path,
		title = NEW.title,
		extension = NEW.extension,
		content = NEW.content
	where id = OLD.id;
end

CREATE TRIGGER insert_files_fts
after insert on files
BEGIN
	insert into files_fts (id, path, title, extension,content)
	values (NEW.id, NEW.path, NEW.title, NEW.extension,NEW.content);
end

CREATE TRIGGER delete_files_fts AFTER DELETE ON files
BEGIN
    DELETE FROM files_fts WHERE id = OLD.id;
END;