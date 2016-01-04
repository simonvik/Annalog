CREATE TABLE urls (
	nick	text,
	url	text PRIMARY KEY,
	time	bigint,
	count	int DEFAULT 0
);

CREATE TABLE whitelist (
	url	text PRIMARY KEY
);

CREATE TABLE lastseen (
	nick	text,
	time	bigint,
	count	int DEFAULT 0
);
