CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    country_id INT,
    company_id INT
);

CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);