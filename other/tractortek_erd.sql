-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema tractortek
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema tractortek
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tractortek` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `tractortek` ;

-- -----------------------------------------------------
-- Table `tractortek`.`warranty_prices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tractortek`.`warranty_prices` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `esp_id` VARCHAR(8) NOT NULL,
  `price_2020` BIGINT NOT NULL,
  `price_2021` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `esp_id` (`esp_id` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `tractortek`.`warranty_sales`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tractortek`.`warranty_sales` (
  `sales_id` INT NOT NULL AUTO_INCREMENT,
  `esp_id` VARCHAR(8) NOT NULL,
  `emp_id` VARCHAR(10) NOT NULL,
  `year` YEAR NOT NULL,
  `week` VARCHAR(5) NOT NULL,
  `quantity` INT NOT NULL,
  PRIMARY KEY (`sales_id`),
  INDEX `esp_id` (`esp_id` ASC) INVISIBLE,
  INDEX `emp_id` (`emp_id` ASC) VISIBLE,
  CONSTRAINT `fk_warranty_sales_warranty_prices1`
    FOREIGN KEY (`esp_id`)
    REFERENCES `tractortek`.`warranty_prices` (`esp_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 4161
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `tractortek`.`employees`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tractortek`.`employees` (
  `emp_id` VARCHAR(10) NOT NULL,
  `name` VARCHAR(30) NOT NULL,
  `paygrade` VARCHAR(5) NOT NULL,
  `region` VARCHAR(2) NOT NULL,
  PRIMARY KEY (`emp_id`),
  INDEX `emp_id` (`emp_id` ASC) VISIBLE,
  CONSTRAINT `fk_employees_warranty_sales1`
    FOREIGN KEY (`emp_id`)
    REFERENCES `tractortek`.`warranty_sales` (`emp_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `tractortek`.`prod_prices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tractortek`.`prod_prices` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `prod_id` VARCHAR(8) NOT NULL,
  `quarter` VARCHAR(3) NOT NULL,
  `year` YEAR NOT NULL,
  `price` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `year` (`year` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `tractortek`.`prod_sales`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tractortek`.`prod_sales` (
  `sales_id` INT NOT NULL AUTO_INCREMENT,
  `prod_id` VARCHAR(8) NOT NULL,
  `emp_id` VARCHAR(8) NOT NULL,
  `year` YEAR NOT NULL,
  `week` VARCHAR(5) NOT NULL,
  `quantity` INT NOT NULL,
  PRIMARY KEY (`sales_id`),
  INDEX `prod_id_idx` (`prod_id` ASC, `emp_id` ASC) VISIBLE,
  INDEX `fk_prod_sales_employees1_idx` (`emp_id` ASC) VISIBLE,
  INDEX `fk_prod_sales_prod_prices1_idx` (`year` ASC) VISIBLE,
  CONSTRAINT `fk_prod_sales_employees1`
    FOREIGN KEY (`emp_id`)
    REFERENCES `tractortek`.`employees` (`emp_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_prod_sales_prod_prices1`
    FOREIGN KEY (`year`)
    REFERENCES `tractortek`.`prod_prices` (`year`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_prod_sales_employees2`
    FOREIGN KEY (`emp_id`)
    REFERENCES `tractortek`.`employees` (`emp_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 4164
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `tractortek`.`prod_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tractortek`.`prod_info` (
  `prod_id` VARCHAR(8) NOT NULL,
  `prod_name` VARCHAR(30) NOT NULL,
  `prod_manufc` VARCHAR(30) NOT NULL,
  `esp_id` VARCHAR(8) NOT NULL,
  `prod_sales_sales_id` INT NOT NULL,
  PRIMARY KEY (`prod_id`),
  INDEX `prod_id` (`prod_sales_sales_id` ASC) VISIBLE,
  INDEX `fk_prod_info_warranty_sales1_idx` (`esp_id` ASC) VISIBLE,
  CONSTRAINT `fk_prod_info_prod_sales`
    FOREIGN KEY (`prod_sales_sales_id`)
    REFERENCES `tractortek`.`prod_sales` (`sales_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_prod_info_warranty_sales1`
    FOREIGN KEY (`esp_id`)
    REFERENCES `tractortek`.`warranty_sales` (`esp_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
