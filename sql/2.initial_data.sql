INSERT INTO country(name)
VALUES 
    ('United States'),
    ('Germany'),
    ('South Korea'),
    ('Japan'),
    ('Canada'),
    ('Sweden');

INSERT INTO company(name)
VALUES
    ('Microsoft'),
    ('Apple'),
    ('Nvidia'),
    ('IBM'),
    ('SAP'),
    ('Samsung'),
    ('Sony'),
    ('Nintendo'),
    ('Shopify'),
    ('Spotify');

INSERT INTO contact(name, country_id, company_id)
VALUES
    ('Test Runner', (SELECT id FROM country WHERE name = 'United States'), (SELECT id FROM company WHERE name = 'Nvidia')),
    ('Jane Doe', (SELECT id FROM country WHERE name = 'South Korea'), (SELECT id FROM company WHERE name = 'Samsung')),
    ('John Doe', (SELECT id FROM country WHERE name = 'Sweden'), (SELECT id FROM company WHERE name = 'Spotify'));
