SET foreign_key_checks = 0;
DROP TABLE IF EXISTS tag;
CREATE TABLE tag (
    id int(11) AUTO_INCREMENT NOT NULL,
    tag text NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET foreign_key_checks = 1;

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS review;
SET foreign_key_checks = 1;
CREATE TABLE review (
    id int(11) NOT NULL,
    product_id int(11) NOT NULL,
    review_title varchar(60) NOT NULL,
    review_text text NOT NULL,
    language_id int(2) NOT NULL DEFAULT '1',
    average_rating float(3,1) DEFAULT NULL,
    PRIMARY KEY (id),
    KEY web_review_idx_language_id (language_id),
    KEY web_review_idx_product_id (product_id),
    KEY average_rating (average_rating),
    KEY web_review_idx_product_id_language_id (product_id, language_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET foreign_key_checks = 0;
DROP TABLE IF EXISTS review_tag_map;
SET foreign_key_checks = 1;
CREATE TABLE review_tag_map (
    tag_id int(11) NOT NULL,
    review_id int(11) NOT NULL,
    PRIMARY KEY  (tag_id, review_id),
    KEY tag_fk (tag_id),
    CONSTRAINT image_fk FOREIGN KEY (review_id) REFERENCES review (id),
    CONSTRAINT tag_fk FOREIGN KEY (tag_id) REFERENCES tag (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
