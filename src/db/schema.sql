SET NAMES 'utf8';

DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS post_instance;

#table reconstructed from post link, eg: http://sfbay.craigslist.org/sfc/prk/2658742009.html
CREATE TABLE posts (
  id             INT           NOT NULL AUTO_INCREMENT,
  region         VARCHAR(128)  NOT NULL,    # "sfbay"
  city           VARCHAR(3),                # "sfc" - NULL would indicate it's the whole region, not just a city (like sfc) in a region (sfbay)
  section        VARCHAR(3)    NOT NULL,    # "hhh"
  cl_id          BIGINT        NOT NULL,    # number id of CL post
  created        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  posted_on      TIMESTAMP     NOT NULL,    # when this entry was created
  last_seen      TIMESTAMP     NOT NULL,    # last time this entry was in database

  PRIMARY KEY (id),
  INDEX citysection (city, section)
);

CREATE TABLE post_instance (
  id             INT NOT NULL AUTO_INCREMENT,
  post_id        INT NOT NULL,
  
  #primary data
  title          TEXT  CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  link           VARCHAR(255) NOT NULL,
  description    TEXT CHARACTER SET utf8 COLLATE utf8_general_ci,
  issued         DATETIME NOT NULL,
  
  #derived data
  price          INT,
  sqft           INT,
  neighborhood   VARCHAR(255),
  bedroomcount   INT,

  loc_xstreet0   VARCHAR(128),
  loc_xstreet1   VARCHAR(128),
  loc_city       VARCHAR(30),
  loc_region     VARCHAR(30),
  loc_link       VARCHAR(255),
  
  
  
  PRIMARY KEY (id),
  INDEX (title(100)).
  INDEX (post_id)
  INDEX (price, bedroomcount, sqft)
);
