
CREATE DATABASE assistant



CREATE TABLE `memories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uuid` CHAR(36) NOT NULL,
  `name` VARCHAR(255),
  `content` TEXT,
  `reflection` TEXT,
  `tags` JSON,
  `active` BOOLEAN NOT NULL DEFAULT TRUE,
  `source` VARCHAR(255),
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;


CREATE TABLE conversation (
    id INTEGER NOT NULL AUTO_INCREMENT,
    uuid CHAR(36) NOT NULL,
    user_message VARCHAR(255),
    chat_response VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
