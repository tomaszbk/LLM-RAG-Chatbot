CREATE EXTENSION vector;
create database vector_db;
switch database vector_db;
CREATE TABLE business_embeddings (
	id bigserial PRIMARY KEY, 
	embedding vector(384),
	content text
);