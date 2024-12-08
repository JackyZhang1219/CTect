CREATE DATABASE IF NOT EXISTS pdfstore;

USE pdfstore;

DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs
(
    jobid             int not null AUTO_INCREMENT,
    status            varchar(256) not null,  -- uploaded, completed, error, processing...
    classname  varchar(256) not null,  -- original PDF filename from user
    extractedtext     text, 
    PRIMARY KEY (jobid)
);

ALTER TABLE jobs AUTO_INCREMENT = 1001;  -- starting value


DROP USER IF EXISTS 'pdfstore-read-only';
DROP USER IF EXISTS 'pdfstore-read-write';

CREATE USER 'pdfstore-read-only' IDENTIFIED BY 'abc123!!';
CREATE USER 'pdfstore-read-write' IDENTIFIED BY 'def456!!';

GRANT SELECT, SHOW VIEW ON pdfstore.* 
      TO 'pdfstore-read-only';
GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER ON pdfstore.* 
      TO 'pdfstore-read-write';
      
FLUSH PRIVILEGES;

--
-- done
--