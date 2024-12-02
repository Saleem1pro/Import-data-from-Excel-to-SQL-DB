-- Si la base de données existe déjà, on la supprime
DROP DATABASE IF EXISTS indemniter;

-- Création de la base de données
CREATE DATABASE indemniter;

-- Utilisation de la base de données
USE indemniter;

-- Table : EMPLOYE --
drop table employe;
CREATE TABLE EMPLOYE
(
   NUMEMP               BIGINT NOT NULL,
   NUMSERVICE           BIGINT NOT NULL,
   EMP_NUMEMP           BIGINT,
   NOMEMP               VARCHAR(50),
   FONCTION             CHAR(20),
   DATEEMB              DATE,
   SALAIRE              DECIMAL(12,4),
   COMM                 DECIMAL(12,4),
   PRIMARY KEY (NUMEMP)
);

--==============================================================
-- Table : ENFANT
--==============================================================
CREATE TABLE ENFANT
(
   NUMENF               BIGINT NOT NULL,
   PRENOM               VARCHAR(30) NOT NULL,
   AGE                  TINYINT NOT NULL,
   CODEIND              CHAR(1) NOT NULL,
   NUMEMP               BIGINT NOT NULL,
   PRIMARY KEY (NUMENF)
);

--==============================================================
-- Table : INDEMNITE
--==============================================================
CREATE TABLE INDEMNITE
(
   CODEIND              CHAR(1) NOT NULL,
   NIVEAU               VARCHAR(30) NOT NULL,
   MONTANT              DECIMAL(8,4) NOT NULL,
   PRIMARY KEY (CODEIND)
);

--==============================================================
-- Table : SERVICE
--==============================================================
CREATE TABLE SERVICE
(
   NUMSERVICE           BIGINT NOT NULL,
   NOMSERVICE           VARCHAR(50),
   LOCALITE             VARCHAR(50),
   PRIMARY KEY (NUMSERVICE)
);

--==============================================================
-- Ajout des contraintes de clé étrangère
--==============================================================

-- Contrainte FK_AFFECTATION
ALTER TABLE EMPLOYE 
   ADD CONSTRAINT FK_AFFECTATION 
   FOREIGN KEY (NUMSERVICE)
   REFERENCES SERVICE (NUMSERVICE) 
   ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Contrainte FK_SUBORDONNE
ALTER TABLE EMPLOYE 
   ADD CONSTRAINT FK_SUBORDONNE 
   FOREIGN KEY (EMP_NUMEMP)
   REFERENCES EMPLOYE (NUMEMP) 
   ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Contrainte FK_PARENTE
ALTER TABLE ENFANT 
   ADD CONSTRAINT FK_PARENTE 
   FOREIGN KEY (NUMEMP)
   REFERENCES EMPLOYE (NUMEMP) 
   ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Contrainte FK_PERCEPTION
ALTER TABLE ENFANT 
   ADD CONSTRAINT FK_PERCEPTION 
   FOREIGN KEY (CODEIND)
   REFERENCES INDEMNITE (CODEIND) 
   ON DELETE RESTRICT ON UPDATE RESTRICT;

SELECT * FROM service;
SELECT * FROM employe;
SELECT * FROM enfant;
SELECT * FROM indemnite;

SHOW GRANTS FOR 'root'@'localhost';

SELECT user, host, plugin FROM mysql.user WHERE user = 'root';
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '7Xu101Be!20?';
FLUSH PRIVILEGES;
