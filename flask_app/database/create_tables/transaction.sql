CREATE TABLE IF NOT EXISTS `transaction` (
`tran_id`            int(11)     NOT NULL AUTO_INCREMENT COMMENT 'the id of this transaction',
`nft_id`             int(11)     NOT NULL COMMENT 'the id of the NFT involved in the transaction',
`nft_date`           DATETIME    NOT NULL COMMENT 'the timestamp when the NFT was created',
`amount`             int(11)     NOT NULL COMMENT 'the amount paid in the transaction',
`owner_id`           int(11)     NOT NULL COMMENT 'the user_id of the owner of the NFT at the time of the transaction',
`transaction_date`   DATETIME    NOT NULL COMMENT 'the timestamp of the transaction',
`type`               varchar(256)     COMMENT 'The type of the transation it is, buy or sell',
`buyer_id`              int(11)     COMMENT 'the buyer of the nft',
`seller_id`             int(11)     COMMENT 'the seller of the nft', 
PRIMARY KEY (`tran_id`),
FOREIGN KEY (`nft_id`) REFERENCES `nfts`(`nft_id`),
FOREIGN KEY (`owner_id`) REFERENCES `users`(`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Contains site NFT transaction information";