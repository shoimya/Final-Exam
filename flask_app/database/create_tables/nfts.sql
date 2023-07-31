CREATE TABLE IF NOT EXISTS `nfts` (
`nft_id`            int(11)  	   NOT NULL auto_increment	  COMMENT 'the id of this user',
`nft_path`          varchar(256)   NOT NULL                   COMMENT 'path_to_local_directory',
`creator_id`        int(11)        NOT NULL                   COMMENT 'the user_id of the creator',
`description`       varchar(256)   NOT NULL            		  COMMENT 'the description of the nft',
`amount`            int(11)        NOT NULL                   COMMENT 'the amount in token',
`status`            varchar(256)   NOT NULL                   COMMENT 'is it being sold right now',
`created_at`        DATETIME       NOT NULL                   COMMENT 'timestamp of NFT creation',
`owner_id`          int(11)        NOT NULL                   COMMENT 'the user_id of the current owner',
PRIMARY KEY (`nft_id`),
FOREIGN KEY (`owner_id`) REFERENCES users(user_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains site NFT information";
