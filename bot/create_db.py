import psycopg2


def db_create():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin", host="localhost")
    cursor = conn.cursor()

    conn.autocommit = True
    sql = '''DROP DATABASE IF EXISTS rieltor_bot;'''
    cursor.execute(sql)
    sql = '''CREATE DATABASE rieltor_bot
            WITH 
            OWNER = postgres
            ENCODING = 'UTF8'
            TABLESPACE = pg_default
            CONNECTION LIMIT = -1;'''
    try:
        cursor.execute(sql)
    except psycopg2.Error as e:
        print("Error creating database:", e)
    conn.commit()
    cursor.close()
    conn.close()
    conn = psycopg2.connect(dbname="rieltor_bot", user="postgres", password="admin",
                            host="localhost")
    cursor = conn.cursor()
    conn.autocommit = True
    sql1 = '''
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS admins CASCADE;
DROP TABLE IF EXISTS selection CASCADE;
DROP TABLE IF EXISTS buy_request CASCADE;
DROP TABLE IF EXISTS sell_request CASCADE;
DROP TABLE IF EXISTS users_mortgage CASCADE;
DROP TABLE IF EXISTS users_questions CASCADE;
DROP TABLE IF EXISTS users_conlultation CASCADE;

CREATE TABLE admins (
  id                 BIGSERIAL,
  name               VARCHAR   NOT NULL,
  tg_id               INT       NOT NULL,
  link               VARCHAR   NOT NULL,
  username           VARCHAR   NOT NULL,
  date_of_add        TIMESTAMP NOT NULL,
  date_of_update     TIMESTAMP,
  PRIMARY KEY (id)
);

CREATE TABLE selection (
  id                 BIGSERIAL,
  type_of            VARCHAR   NOT NULL,
  link               VARCHAR   NOT NULL,
  date_of_add        TIMESTAMP NOT NULL,
  date_of_update     TIMESTAMP,
  admin_id           BIGINT    NOT NULL REFERENCES admins ON DELETE CASCADE,
  PRIMARY KEY (id)
);

CREATE TABLE users (
  id                 BIGSERIAL,
  name               VARCHAR   NOT NULL,
  tg_id              INT        NOT NULL,
  link               VARCHAR   NOT NULL,
  username           VARCHAR   NOT NULL,
  years              VARCHAR,
  date_of_birth      DATE,
  phone_number       VARCHAR,
  work_phone_number  VARCHAR,
  salary             INT,
  place_of_work      VARCHAR,
  children           VARCHAR,
  date_of_add        TIMESTAMP NOT NULL,
  date_of_update     TIMESTAMP,
  admin_id           BIGINT     NOT NULL REFERENCES admins ON DELETE CASCADE,
  PRIMARY KEY (id)
);

CREATE TABLE buy_request (
  id                     	BIGSERIAL,
  type_of_object_buy     	VARCHAR   NOT NULL,
  cost_range             	VARCHAR   NOT NULL,
  type_of_object_buy_detail VARCHAR,
  land_square            	VARCHAR,
  number_of_rooms        	INT,
  square                 	VARCHAR,
  location_              	VARCHAR,
  calculation_format     	VARCHAR,
  is_approved            	BOOL,
  date_of_add            	TIMESTAMP NOT NULL,
  user_id                	BIGINT    NOT NULL REFERENCES users ON DELETE CASCADE,
  PRIMARY KEY (id)
);

CREATE TABLE sell_request (
  id                  BIGSERIAL,
  type_of_object      VARCHAR   NOT NULL,
  address             VARCHAR,
  number_of_rooms     INT,
  square              VARCHAR,
  date_of_add         TIMESTAMP NOT NULL,
  user_id             BIGINT    NOT NULL REFERENCES users ON DELETE CASCADE,
  PRIMARY KEY (id)
);

CREATE TABLE users_mortgage (
  id                  BIGSERIAL,
  family_mortgage     BOOL      NOT NULL,
  rural_mortgage      BOOL      NOT NULL,
  base_rate           BOOL      NOT NULL,
  IT_mortgage         BOOL      NOT NULL,
  state_support_2020  BOOL      NOT NULL,
  date_of_add         TIMESTAMP NOT NULL,
  user_id             BIGINT    NOT NULL REFERENCES users ON DELETE CASCADE,
  PRIMARY KEY (id)
);

CREATE TABLE users_questions (
  id                  BIGSERIAL,
  question            BOOL      NOT NULL,
  date_of_add         TIMESTAMP NOT NULL,
  user_id             BIGINT    NOT NULL REFERENCES users ON DELETE CASCADE,
  PRIMARY KEY (id)
);

CREATE TABLE users_conlultation (
  id                  BIGSERIAL,
  date_of_add         TIMESTAMP NOT NULL,
  user_id             BIGINT    NOT NULL REFERENCES users ON DELETE CASCADE,
  PRIMARY KEY (id)
);
    '''
    cursor.execute(sql1)
    conn.commit()
    print("Database created successfully........")

    # Closing the connection

    cursor.close()
    conn.close()


db_create()
