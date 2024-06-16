CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE contact (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    country_id INTEGER REFERENCES country(id),
    company_id INTEGER REFERENCES company(id)
);