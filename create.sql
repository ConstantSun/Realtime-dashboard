CREATE TABLE tps_src.client (
    client_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100),
    branch_id VARCHAR(10),
    id_number VARCHAR(20),
    issue_date DATE,
    city_of_issue VARCHAR(100),
    registration_type VARCHAR(100),
    client_remarks VARCHAR(100),
    sex CHAR(1),
    birthday DATE,
    ac_open_date DATE,
    last_modified TIMESTAMP,
    expiry DATE
);

