CREATE TABLE IF NOT EXISTS `wallet` (
`user_key`          varchar(256)      NOT NULL                 COMMENT 'This is the key os the user',
`tokens`            int(11)           NOT NULL   DEFAULT 1000  COMMENT 'This is the tokens user has',
FOREIGN KEY (user_key) REFERENCES users(user_key)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains site wallet info";