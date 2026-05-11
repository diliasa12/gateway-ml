-- Buat database
CREATE DATABASE IF NOT EXISTS 2410511078_ml_service;
USE ml_service;

-- Buat tabel hasil prediksi
CREATE TABLE IF NOT EXISTS hasil_prediksi (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    ph                FLOAT        NOT NULL,
    lembap_udara      FLOAT        NOT NULL,
    prediksi          VARCHAR(50)  NOT NULL,
    nilai_confidence  FLOAT        NOT NULL,
    created_at        DATETIME     NOT NULL
);
