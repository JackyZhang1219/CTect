CREATE DATABASE IF NOT EXISTS pdfstore;

USE pdfstore;

DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs
(
    jobid             int not null AUTO_INCREMENT,
    status            varchar(256) not null,  -- uploaded, completed, error, processing...
    originaldatafile  varchar(256) not null,  -- original PDF filename from user
    datafilekey       varchar(256) not null,  -- PDF filename in S3 (bucketkey)
    resultsfilekey    varchar(256) not null,  -- results filename in S3 bucket
    PRIMARY KEY (jobid),
    FOREIGN KEY (userid) REFERENCES users(userid),
    UNIQUE      (datafilekey)
);

ALTER TABLE jobs AUTO_INCREMENT = 1001;  -- starting value


DROP USER IF EXISTS 'benfordapp-read-only';
DROP USER IF EXISTS 'benfordapp-read-write';

CREATE USER 'pdfstore-read-only' IDENTIFIED BY 'abc123!!';
CREATE USER 'pdfstore-read-write' IDENTIFIED BY 'def456!!';

GRANT SELECT, SHOW VIEW ON benfordapp.* 
      TO 'pdfstore-read-only';
GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER ON benfordapp.* 
      TO 'pdfstore-read-write';
      
FLUSH PRIVILEGES;

--
-- done
--

