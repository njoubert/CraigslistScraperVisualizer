

#table reconstructed from post link, eg: http://sfbay.craigslist.org/sfc/prk/2658742009.html
CREATE TABLE IF NOT EXISTS posts (
  id INT NOT NULL AUTO_INCREMENT,
  region VARCHAR(128) NOT NULL,   # "sfbay"
  city VARCHAR(3),                # "sfc" - NULL would indicate it's the whole region, not just a city (like sfc) in a region (sfbay)
  section VARCHAR(3) NOT NULL,    # "hhh"
  cl_id BIGINT NOT NULL,          # number id of CL post
  first_seen TIMESTAMP,           # when this entry was created
  
  PRIMARY KEY (id),
  UNIQUE INDEX compound_post_id (region, city, section, cl_id)
);

CREATE TABLE post_instance (
  id INT NOT NULL AUTO_INCREMENT,
  post_id INT NOT NULL,
  
  #primary data
  title TEXT NOT NULL,
  link VARCHAR(255) NOT NULL,
  description BLOB,
  issued DATETIME NOT NULL,
  
  #derived data
  price INT,
  sqft INT,
  neighborhood VARCHAR(255),
  bedroomcount INT,
  loc_xstreet0 VARCHAR(128),
  loc_xstreet1 VARCHAR(128),
  loc_city VARCHAR(30),
  loc_region VARCHAR(30),
  loc_link VARCHAR(255),
  
  PRIMARY KEY (id),
  INDEX (title(100))
);
