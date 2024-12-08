CREATE DATABASE IF NOT EXISTS pdfstore;

USE pdfstore;

DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs
(
    jobid             int not null AUTO_INCREMENT,
    status            varchar(256) not null,  -- uploaded, completed, error, processing...
    originaldatafile  varchar(256) not null,  -- original PDF filename from user
    extractedtext     text, 
    averagerating     float default -1,
    PRIMARY KEY (jobid)
);

ALTER TABLE jobs AUTO_INCREMENT = 1001;  -- starting value


DROP USER IF EXISTS 'pdfstore-read-only';
DROP USER IF EXISTS 'pdfstore-read-write';

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

INSERT INTO jobs(jobid, status, originaldatafile, extractedtext)
      values(1001, 'completed', 'cs310', "this class is really bad, it's genuinely horrible")