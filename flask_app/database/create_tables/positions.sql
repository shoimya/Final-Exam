CREATE TABLE IF NOT EXISTS `positions` (
`position_id`        int(11)       NOT NULL AUTO_INCREMENT	COMMENT 'The position id',
`inst_id`            int(11)       NOT NULL 				COMMENT 'FK:The instiution id',
`title`              varchar(100)  NOT NULL					COMMENT 'My title in this position',
`responsibilities`   varchar(500)  NOT NULL                 COMMENT 'My responsibilities in this position',
`start_date`         date          NOT NULL                 COMMENT 'My start date for this position',
`end_date`           date          DEFAULT NULL             COMMENT 'The end date for this position',
PRIMARY KEY (`position_id`),
FOREIGN KEY (inst_id) REFERENCES institutions(inst_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT="Positions I have held";