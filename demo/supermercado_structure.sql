-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema supermercado
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema supermercado
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `supermercado` DEFAULT CHARACTER SET utf8mb3 ;
USE `supermercado` ;

-- -----------------------------------------------------
-- Table `supermercado`.`categorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `supermercado`.`categorias` (
  `categoria_id` INT NOT NULL AUTO_INCREMENT,
  `categoria` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`categoria_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `supermercado`.`subcategorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `supermercado`.`subcategorias` (
  `subcategoria_id` INT NOT NULL AUTO_INCREMENT,
  `subcategoria` VARCHAR(50) NOT NULL,
  `categoria_id` INT NOT NULL,
  PRIMARY KEY (`subcategoria_id`),
  INDEX `categoria_id` (`categoria_id` ASC) VISIBLE,
  CONSTRAINT `subcategorias_ibfk_1`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `supermercado`.`categorias` (`categoria_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `supermercado`.`productos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `supermercado`.`productos` (
  `producto_id` INT NOT NULL AUTO_INCREMENT,
  `producto` VARCHAR(50) NOT NULL,
  `formato` VARCHAR(50) NOT NULL,
  `precio` VARCHAR(50) NOT NULL,
  `subcategoria_id` INT NOT NULL,
  `categoria_id` INT NOT NULL,
  PRIMARY KEY (`producto_id`),
  INDEX `subcategoria_id` (`subcategoria_id` ASC) VISIBLE,
  INDEX `categoria_id` (`categoria_id` ASC) VISIBLE,
  CONSTRAINT `productos_ibfk_1`
    FOREIGN KEY (`subcategoria_id`)
    REFERENCES `supermercado`.`subcategorias` (`subcategoria_id`),
  CONSTRAINT `productos_ibfk_2`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `supermercado`.`categorias` (`categoria_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 176
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `supermercado`.`ventas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `supermercado`.`ventas` (
  `venta_id` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `dia_semana` VARCHAR(20) NOT NULL,
  `numero_semana` INT NOT NULL,
  `categoria_id` INT NOT NULL,
  PRIMARY KEY (`venta_id`),
  INDEX `categoria_id` (`categoria_id` ASC) VISIBLE,
  CONSTRAINT `ventas_ibfk_1`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `supermercado`.`categorias` (`categoria_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 152
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `supermercado`.`ventas_productos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `supermercado`.`ventas_productos` (
  `venta_id` INT NOT NULL,
  `producto_id` INT NOT NULL,
  `venta` INT NOT NULL,
  `prevision` INT NOT NULL,
  PRIMARY KEY (`venta_id`, `producto_id`),
  INDEX `producto_id` (`producto_id` ASC) VISIBLE,
  CONSTRAINT `ventas_productos_ibfk_1`
    FOREIGN KEY (`venta_id`)
    REFERENCES `supermercado`.`ventas` (`venta_id`),
  CONSTRAINT `ventas_productos_ibfk_2`
    FOREIGN KEY (`producto_id`)
    REFERENCES `supermercado`.`productos` (`producto_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
