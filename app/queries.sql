INSERT INTO companies(
    id,
    name,
    category,
    balance_paisa
)
VALUES (
    1,
    "Danesh Publications",
    "publishers",
    100000
);

INSERT INTO publishers (
    id,
    companies_id
)
VALUES (
    1,
    1
);


INSERT INTO books (
    id,
    publisher_id,
    title,
    edition,
    year_of_publishing,
    pages,
    colours,
    binding,
    times_printed
)
VALUES (
    1,
    1,
    "Secondary English 3",
    1,
    "2022",
    100,
    4,
    "UV",
    1
);

INSERT INTO companies (
    id,
    name,
    category,
    balance_paisa
)
VALUES (
    2,
    "Shafiq Paper",
    "paper supplier",
    100000
);

INSERT INTO paper_suppliers(
    id,
    companies_id
)
VALUES (
    1,
    2
);

INSERT INTO paper (
    batch_no,
    paper_suppliers_id,
    size,
    type,
    bought_rate,
    market_rate,
    country,
    stock_reams
)
VALUES (
    1,
    1,
    "A4",
    "Matt",
    20,
    22,
    "Pakistan",
    100
);


INSERT INTO orders 
            (date,
            book_id, 
            quantity, 
            plates_unit_cost, 
            binding_unit_cost, 
            paper_unit_cost,
            batch_no,
            status)
VALUES (
    "30 Oct 2023",
    1,
    1000,
    10,
    1,
    1,
    1,
    "Pending"
    );