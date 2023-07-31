CREATE TABLE IF NOT EXISTS `users` (
`user_id`         int(11)  	     NOT NULL auto_increment	  COMMENT 'This is the id of this user and primary key',
`role`            varchar(256)    NOT NULL                     COMMENT 'This is the role of the user; options include: admin and users',
`email`           varchar(256)   NOT NULL            		  COMMENT 'This is the email',
`password`        varchar(256)   NOT NULL                     COMMENT 'This is the password',
`user_key`        varchar(256)   NOT NULL           COMMENT 'This is the amount in the wallet',
`entry`           int(11)        NOT NULL                     COMMENT 'This is the amount user logged in',
PRIMARY KEY (`user_id`),
KEY `user_key_idx` (`user_key`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains site user information";
