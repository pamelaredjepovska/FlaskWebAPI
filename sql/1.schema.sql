CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);

CREATE TABLE contact (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    country_id INTEGER REFERENCES country(id),
    company_id INTEGER REFERENCES company(id)
);