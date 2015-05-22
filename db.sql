CREATE TABLE urls (
	nick	text,
	url	text,
	time	bigint
);

CREATE INDEX i_url ON urls(url);

CREATE TABLE whitelist (
	url	text PRIMARY KEY
);
