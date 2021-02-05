CREATE TABLE `img` (
  `id` int NOT NULL AUTO_INCREMENT,
  `md5` varchar(255) NOT NULL,
  `url` varchar(255) DEFAULT NULL,
  `save_name` varchar(255) NOT NULL,
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;