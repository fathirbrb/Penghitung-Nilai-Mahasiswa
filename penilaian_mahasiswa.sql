-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 02, 2025 at 02:12 PM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `penilaian_mahasiswa`
--

-- --------------------------------------------------------

--
-- Table structure for table `absensi`
--

CREATE TABLE `absensi` (
  `id_absensi` int NOT NULL,
  `id_matkul` int NOT NULL,
  `npm` varchar(20) NOT NULL,
  `jumlah_pertemuan` int NOT NULL,
  `jumlah_hadir` int NOT NULL,
  `nilai_absensi` float GENERATED ALWAYS AS ((case when (`jumlah_pertemuan` > 0) then round(((`jumlah_hadir` * 100.0) / `jumlah_pertemuan`),2) else 0 end)) STORED,
  `nilai_akhir_absensi` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `absensi`
--

INSERT INTO `absensi` (`id_absensi`, `id_matkul`, `npm`, `jumlah_pertemuan`, `jumlah_hadir`, `nilai_akhir_absensi`) VALUES
(1, 1, '24121201', 14, 12, NULL),
(2, 2, '24121201', 14, 10, NULL),
(3, 3, '24121201', 14, 13, NULL),
(4, 4, '24121201', 14, 13, NULL),
(5, 5, '24121201', 14, 14, NULL),
(6, 6, '24121201', 14, 13, NULL),
(7, 7, '24121201', 14, 12, NULL),
(8, 8, '24121201', 14, 14, NULL),
(9, 9, '24121201', 14, 13, NULL),
(10, 10, '24121201', 14, 10, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `mahasiswa`
--

CREATE TABLE `mahasiswa` (
  `npm` varchar(20) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `jurusan` varchar(100) NOT NULL,
  `angkatan` int NOT NULL,
  `program_studi` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mahasiswa`
--

INSERT INTO `mahasiswa` (`npm`, `nama`, `jurusan`, `angkatan`, `program_studi`) VALUES
('24121201', 'Sandi', 'Teknik Informatika', 2023, 'S1 Teknik Informatika'),
('24121202', 'Budi', 'Teknik Informatika', 2023, 'S1 Teknik Informatika'),
('24121203', 'Dewi', 'Ilmu Komputer', 2024, 'S1 Sistem Informasi'),
('24121204', 'Rina', 'Ilmu Komputer', 2024, 'S1 Sistem Informasi'),
('24121205', 'Eka', 'Teknik Informatika', 2024, 'S1 Teknik Informatika'),
('24121206', 'Fahmi', 'Teknik Informatika', 2024, 'S1 Teknik Informatika'),
('24121207', 'Putra', 'Ilmu Komputer', 2024, 'S1 Sistem Informasi'),
('24121208', 'Indah', 'Ilmu Komputer', 2024, 'S1 Sistem Informasi'),
('24121209', 'Aldi', 'Ilmu Komputer', 2024, 'S1 Ilmu Komputer'),
('24121210', 'Siti', 'Ilmu Komputer', 2024, 'S1 Ilmu Komputer');

-- --------------------------------------------------------

--
-- Table structure for table `mata_kuliah`
--

CREATE TABLE `mata_kuliah` (
  `id_matkul` int NOT NULL,
  `nama_matkul` varchar(100) NOT NULL,
  `sks` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `mata_kuliah`
--

INSERT INTO `mata_kuliah` (`id_matkul`, `nama_matkul`, `sks`) VALUES
(1, 'Basis Data', 2),
(2, 'Algoritma', 3),
(3, 'Pemrograman Java', 3),
(4, 'Matematika', 2),
(5, 'Jaringan Komputer', 3),
(6, 'Sistem Operasi', 3),
(7, 'Kecerdasan Buatan', 3),
(8, 'Jaringan Komputer Lanjut', 3),
(9, 'Desain Web', 2),
(10, 'Teori Automata', 3);

-- --------------------------------------------------------

--
-- Table structure for table `nilai_akhir_mahasiswa`
--

CREATE TABLE `nilai_akhir_mahasiswa` (
  `id_nilai` int NOT NULL,
  `id_matkul` int NOT NULL,
  `npm` varchar(20) NOT NULL,
  `nilai_akhir_total` float DEFAULT NULL,
  `huruf_matkul` varchar(2) DEFAULT NULL,
  `bobot_matkul` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `nilai_quiz`
--

CREATE TABLE `nilai_quiz` (
  `id_quiz` int NOT NULL,
  `id_matkul` int NOT NULL,
  `npm` varchar(20) NOT NULL,
  `rata_rata_quiz` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `nilai_quiz`
--

INSERT INTO `nilai_quiz` (`id_quiz`, `id_matkul`, `npm`, `rata_rata_quiz`) VALUES
(1, 1, '24121201', 87.5),
(2, 2, '24121201', 82.5),
(3, 3, '24121201', 92.5),
(4, 4, '24121201', 72.5),
(5, 5, '24121201', 82.5),
(6, 6, '24121201', 77.5),
(7, 7, '24121201', 87.5),
(8, 8, '24121201', 82.5),
(9, 9, '24121201', 72.5),
(10, 10, '24121201', 92.5);

-- --------------------------------------------------------

--
-- Table structure for table `nilai_quiz_detail`
--

CREATE TABLE `nilai_quiz_detail` (
  `id_quiz_detail` INT NOT NULL AUTO_INCREMENT,
  `id_matkul` INT NOT NULL,
  `npm` VARCHAR(20) NOT NULL,  -- NPM mahasiswa
  `quiz_number` INT NOT NULL,  -- Nomor quiz (Quiz 1, Quiz 2, dsb.)
  `nilai_quiz` FLOAT DEFAULT 0 NOT NULL,  -- Nilai quiz (nilai default 0)
  PRIMARY KEY (`id_quiz_detail`),
  FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah`(`id_matkul`) ON DELETE CASCADE,
  FOREIGN KEY (`npm`) REFERENCES `mahasiswa`(`npm`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `nilai_quiz_detail`
--
DELIMITER $$
CREATE TRIGGER `update_rata_rata_quiz` AFTER INSERT ON `nilai_quiz_detail` FOR EACH ROW BEGIN
    DECLARE rata FLOAT;

    SELECT AVG(nilai_quiz)
    INTO rata
    FROM nilai_quiz_detail
    WHERE npm = NEW.npm AND id_matkul = NEW.id_matkul;

    INSERT INTO nilai_quiz (id_matkul, npm, rata_rata_quiz)
    VALUES (NEW.id_matkul, NEW.npm, IFNULL(rata,0))
    ON DUPLICATE KEY UPDATE rata_rata_quiz = VALUES(rata_rata_quiz);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `nilai_responsi`
--

CREATE TABLE `nilai_responsi` (
  `id_responsi` int NOT NULL,
  `id_matkul` int NOT NULL,
  `npm` varchar(20) NOT NULL,
  `nilai_responsi` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `nilai_responsi`
--

INSERT INTO `nilai_responsi` (`id_responsi`, `id_matkul`, `npm`, `nilai_responsi`) VALUES
(1, 2, '24121201', 85),
(2, 3, '24121201', 88),
(3, 5, '24121201', 90),
(4, 6, '24121201', 80),
(5, 7, '24121201', 92),
(6, 8, '24121201', 88),
(7, 10, '24121201', 90);

-- --------------------------------------------------------

--
-- Table structure for table `nilai_tugas`
--

CREATE TABLE `nilai_tugas` (
  `id_tugas` int NOT NULL,
  `id_matkul` int NOT NULL,
  `npm` varchar(20) NOT NULL,
  `rata_rata_tugas` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `nilai_tugas`
--

INSERT INTO `nilai_tugas` (`id_tugas`, `id_matkul`, `npm`, `rata_rata_tugas`) VALUES
(1, 1, '24121201', 82.5),
(2, 2, '24121201', 82.5),
(3, 3, '24121201', 87.5),
(4, 4, '24121201', 77.5),
(5, 5, '24121201', 87.5),
(6, 6, '24121201', 82.5),
(7, 7, '24121201', 92.5),
(8, 8, '24121201', 82.5),
(9, 9, '24121201', 77.5),
(10, 10, '24121201', 92.5);

-- --------------------------------------------------------

--
-- Table structure for table `nilai_tugas_detail`
--

CREATE TABLE `nilai_tugas_detail` (
  `id_tugas_detail` INT NOT NULL AUTO_INCREMENT,
  `id_matkul` INT NOT NULL,
  `npm` VARCHAR(20) NOT NULL,  -- NPM mahasiswa
  `tugas_number` INT NOT NULL,  -- Nomor tugas (Tugas 1, Tugas 2, dsb.)
  `nilai_tugas` FLOAT DEFAULT 0 NOT NULL,  -- Nilai tugas (nilai default 0)
  PRIMARY KEY (`id_tugas_detail`),
  FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah`(`id_matkul`) ON DELETE CASCADE,
  FOREIGN KEY (`npm`) REFERENCES `mahasiswa`(`npm`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Triggers `nilai_tugas_detail`
--
DELIMITER $$
CREATE TRIGGER `calculate_final_grade` AFTER INSERT ON `nilai_tugas_detail` FOR EACH ROW BEGIN
    DECLARE nilai FLOAT DEFAULT 0;
    DECLARE huruf VARCHAR(2);
    DECLARE bobot FLOAT;

    DECLARE p_tugas FLOAT;
    DECLARE p_quiz FLOAT;
    DECLARE p_abs FLOAT;
    DECLARE p_uts FLOAT;
    DECLARE p_uas FLOAT;
    DECLARE p_res FLOAT;

    SELECT persentase_tugas, persentase_quiz, persentase_absensi,
           persentase_uts, persentase_uas, IFNULL(persentase_responsi,0)
    INTO p_tugas, p_quiz, p_abs, p_uts, p_uas, p_res
    FROM persentase_matkul
    WHERE id_matkul = NEW.id_matkul;

    SET nilai =
          (IFNULL((SELECT rata_rata_tugas FROM nilai_tugas WHERE id_matkul=NEW.id_matkul AND npm=NEW.npm),0) * p_tugas / 100)
        + (IFNULL((SELECT rata_rata_quiz FROM nilai_quiz WHERE id_matkul=NEW.id_matkul AND npm=NEW.npm),0) * p_quiz / 100)
        + (IFNULL((SELECT nilai_absensi FROM absensi WHERE id_matkul=NEW.id_matkul AND npm=NEW.npm),0) * p_abs / 100)
        + (IFNULL((SELECT nilai_uts FROM nilai_uts WHERE id_matkul=NEW.id_matkul AND npm=NEW.npm),0) * p_uts / 100)
        + (IFNULL((SELECT nilai_uas FROM nilai_uas WHERE id_matkul=NEW.id_matkul AND npm=NEW.npm),0) * p_uas / 100)
        + (IFNULL((SELECT nilai_responsi FROM nilai_responsi WHERE id_matkul=NEW.id_matkul AND npm=NEW.npm),0) * p_res / 100);

    SET huruf = CASE
        WHEN nilai >= 99 THEN 'A+'
        WHEN nilai >= 90 THEN 'A'
        WHEN nilai >= 80 THEN 'B'
        WHEN nilai >= 70 THEN 'C'
        WHEN nilai >= 60 THEN 'D'
        ELSE 'E'
    END;

    SET bobot = CASE
        WHEN huruf IN ('A+', 'A') THEN 4.0
        WHEN huruf = 'B' THEN 3.0
        WHEN huruf = 'C' THEN 2.0
        WHEN huruf = 'D' THEN 1.0
        ELSE 0.0
    END;

    INSERT INTO nilai_akhir_mahasiswa (id_matkul, npm, nilai_akhir_total, huruf_matkul, bobot_matkul)
    VALUES (NEW.id_matkul, NEW.npm, nilai, huruf, bobot)
    ON DUPLICATE KEY UPDATE
        nilai_akhir_total = VALUES(nilai_akhir_total),
        huruf_matkul = VALUES(huruf_matkul),
        bobot_matkul = VALUES(bobot_matkul);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `update_rata_rata_tugas` AFTER INSERT ON `nilai_tugas_detail` FOR EACH ROW BEGIN
    DECLARE rata FLOAT;

    SELECT AVG(nilai_tugas)
    INTO rata
    FROM nilai_tugas_detail
    WHERE npm = NEW.npm AND id_matkul = NEW.id_matkul;

    INSERT INTO nilai_tugas (id_matkul, npm, rata_rata_tugas)
    VALUES (NEW.id_matkul, NEW.npm, IFNULL(rata,0))
    ON DUPLICATE KEY UPDATE rata_rata_tugas = VALUES(rata_rata_tugas);

END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `nilai_uas`
--

CREATE TABLE `nilai_uas` (
  `id_uas` int NOT NULL,
  `id_matkul` int NOT NULL,
  `npm` varchar(20) NOT NULL,
  `nilai_uas` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `nilai_uas`
--

INSERT INTO `nilai_uas` (`id_uas`, `id_matkul`, `npm`, `nilai_uas`) VALUES
(1, 1, '24121201', 85),
(2, 2, '24121201', 80),
(3, 3, '24121201', 92),
(4, 4, '24121201', 88),
(5, 5, '24121201', 90),
(6, 6, '24121201', 84),
(7, 7, '24121201', 93),
(8, 8, '24121201', 90),
(9, 9, '24121201', 88),
(10, 10, '24121201', 90);

-- --------------------------------------------------------

--
-- Table structure for table `nilai_uts`
--

CREATE TABLE `nilai_uts` (
  `id_uts` int NOT NULL,
  `id_matkul` int NOT NULL,
  `npm` varchar(20) NOT NULL,
  `nilai_uts` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `nilai_uts`
--

INSERT INTO `nilai_uts` (`id_uts`, `id_matkul`, `npm`, `nilai_uts`) VALUES
(1, 1, '24121201', 80),
(2, 2, '24121201', 75),
(3, 3, '24121201', 85),
(4, 4, '24121201', 90),
(5, 5, '24121201', 85),
(6, 6, '24121201', 80),
(7, 7, '24121201', 95),
(8, 8, '24121201', 85),
(9, 9, '24121201', 90),
(10, 10, '24121201', 88);

-- --------------------------------------------------------

--
-- Table structure for table `persentase_matkul`
--

CREATE TABLE `persentase_matkul` (
  `id_persentase` int NOT NULL,
  `id_matkul` int NOT NULL,
  `persentase_absensi` float NOT NULL,
  `persentase_tugas` float NOT NULL,
  `persentase_quiz` float NOT NULL,
  `persentase_uts` float NOT NULL,
  `persentase_uas` float NOT NULL,
  `persentase_responsi` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `persentase_matkul`
--

INSERT INTO `persentase_matkul` (`id_persentase`, `id_matkul`, `persentase_absensi`, `persentase_tugas`, `persentase_quiz`, `persentase_uts`, `persentase_uas`, `persentase_responsi`) VALUES
(1, 1, 5, 20, 10, 25, 25, NULL),
(2, 2, 5, 20, 10, 25, 25, 15),
(3, 3, 5, 20, 10, 25, 25, 15),
(4, 4, 5, 25, 15, 25, 20, NULL),
(5, 5, 5, 20, 10, 25, 25, 15),
(6, 6, 5, 20, 10, 25, 25, 15),
(7, 7, 5, 20, 10, 25, 25, 15),
(8, 8, 5, 20, 10, 25, 25, 15),
(9, 9, 5, 20, 10, 25, 25, NULL),
(10, 10, 5, 20, 10, 25, 25, 15);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `absensi`
--
ALTER TABLE `absensi`
  ADD PRIMARY KEY (`id_absensi`),
  ADD KEY `id_matkul` (`id_matkul`),
  ADD KEY `npm` (`npm`);

--
-- Indexes for table `mahasiswa`
--
ALTER TABLE `mahasiswa`
  ADD PRIMARY KEY (`npm`);

--
-- Indexes for table `mata_kuliah`
--
ALTER TABLE `mata_kuliah`
  ADD PRIMARY KEY (`id_matkul`);

--
-- Indexes for table `nilai_akhir_mahasiswa`
--
ALTER TABLE `nilai_akhir_mahasiswa`
  ADD PRIMARY KEY (`id_nilai`),
  ADD UNIQUE KEY `uniq_nilai_matkul_npm` (`id_matkul`,`npm`),
  ADD KEY `npm` (`npm`);

--
-- Indexes for table `nilai_quiz`
--
ALTER TABLE `nilai_quiz`
  ADD PRIMARY KEY (`id_quiz`),
  ADD UNIQUE KEY `uniq_matkul_npm_quiz` (`id_matkul`,`npm`),
  ADD KEY `npm` (`npm`);

--
-- Indexes for table `nilai_quiz_detail`
--
ALTER TABLE `nilai_quiz_detail`
  ADD PRIMARY KEY (`id_quiz_detail`),
  ADD KEY `id_matkul` (`id_matkul`),
  ADD KEY `npm` (`npm`);

--
-- Indexes for table `nilai_responsi`
--
ALTER TABLE `nilai_responsi`
  ADD PRIMARY KEY (`id_responsi`),
  ADD KEY `id_matkul` (`id_matkul`),
  ADD KEY `npm` (`npm`);

--
-- Indexes for table `nilai_tugas`
--
ALTER TABLE `nilai_tugas`
  ADD PRIMARY KEY (`id_tugas`),
  ADD UNIQUE KEY `uniq_matkul_npm_tugas` (`id_matkul`,`npm`),
  ADD KEY `npm` (`npm`);

--
-- Indexes for table `nilai_tugas_detail`
--
ALTER TABLE `nilai_tugas_detail`
  ADD PRIMARY KEY (`id_tugas_detail`),
  ADD KEY `id_matkul` (`id_matkul`),
  ADD KEY `npm` (`npm`);

--
-- Indexes for table `nilai_uas`
--
ALTER TABLE `nilai_uas`
  ADD PRIMARY KEY (`id_uas`),
  ADD KEY `id_matkul` (`id_matkul`),
  ADD KEY `npm` (`npm`);

--
-- Indexes for table `nilai_uts`
--
ALTER TABLE `nilai_uts`
  ADD PRIMARY KEY (`id_uts`),
  ADD KEY `id_matkul` (`id_matkul`),
  ADD KEY `npm` (`npm`);

--
-- Indexes for table `persentase_matkul`
--
ALTER TABLE `persentase_matkul`
  ADD PRIMARY KEY (`id_persentase`),
  ADD KEY `id_matkul` (`id_matkul`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `absensi`
--
ALTER TABLE `absensi`
  MODIFY `id_absensi` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `mata_kuliah`
--
ALTER TABLE `mata_kuliah`
  MODIFY `id_matkul` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `nilai_akhir_mahasiswa`
--
ALTER TABLE `nilai_akhir_mahasiswa`
  MODIFY `id_nilai` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `nilai_quiz`
--
ALTER TABLE `nilai_quiz`
  MODIFY `id_quiz` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `nilai_quiz_detail`
--
ALTER TABLE `nilai_quiz_detail`
  MODIFY `id_quiz_detail` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `nilai_responsi`
--
ALTER TABLE `nilai_responsi`
  MODIFY `id_responsi` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `nilai_tugas`
--
ALTER TABLE `nilai_tugas`
  MODIFY `id_tugas` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `nilai_tugas_detail`
--
ALTER TABLE `nilai_tugas_detail`
  MODIFY `id_tugas_detail` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `nilai_uas`
--
ALTER TABLE `nilai_uas`
  MODIFY `id_uas` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `nilai_uts`
--
ALTER TABLE `nilai_uts`
  MODIFY `id_uts` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `persentase_matkul`
--
ALTER TABLE `persentase_matkul`
  MODIFY `id_persentase` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `absensi`
--
ALTER TABLE `absensi`
  ADD CONSTRAINT `absensi_ibfk_1` FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah` (`id_matkul`) ON DELETE CASCADE,
  ADD CONSTRAINT `absensi_ibfk_2` FOREIGN KEY (`npm`) REFERENCES `mahasiswa` (`npm`) ON DELETE CASCADE;

--
-- Constraints for table `nilai_akhir_mahasiswa`
--
ALTER TABLE `nilai_akhir_mahasiswa`
  ADD CONSTRAINT `nilai_akhir_mahasiswa_ibfk_1` FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah` (`id_matkul`) ON DELETE CASCADE,
  ADD CONSTRAINT `nilai_akhir_mahasiswa_ibfk_2` FOREIGN KEY (`npm`) REFERENCES `mahasiswa` (`npm`) ON DELETE CASCADE;

--
-- Constraints for table `nilai_quiz`
--
ALTER TABLE `nilai_quiz`
  ADD CONSTRAINT `nilai_quiz_ibfk_1` FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah` (`id_matkul`) ON DELETE CASCADE,
  ADD CONSTRAINT `nilai_quiz_ibfk_2` FOREIGN KEY (`npm`) REFERENCES `mahasiswa` (`npm`) ON DELETE CASCADE;

--
-- Constraints for table `nilai_quiz_detail`
--
ALTER TABLE `nilai_quiz_detail`
  ADD CONSTRAINT `nilai_quiz_detail_ibfk_1` FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah` (`id_matkul`) ON DELETE CASCADE,
  ADD CONSTRAINT `nilai_quiz_detail_ibfk_2` FOREIGN KEY (`npm`) REFERENCES `mahasiswa` (`npm`) ON DELETE CASCADE;

--
-- Constraints for table `nilai_responsi`
--
ALTER TABLE `nilai_responsi`
  ADD CONSTRAINT `nilai_responsi_ibfk_1` FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah` (`id_matkul`) ON DELETE CASCADE,
  ADD CONSTRAINT `nilai_responsi_ibfk_2` FOREIGN KEY (`npm`) REFERENCES `mahasiswa` (`npm`) ON DELETE CASCADE;

--
-- Constraints for table `nilai_tugas`
--
ALTER TABLE `nilai_tugas`
  ADD CONSTRAINT `nilai_tugas_ibfk_1` FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah` (`id_matkul`) ON DELETE CASCADE,
  ADD CONSTRAINT `nilai_tugas_ibfk_2` FOREIGN KEY (`npm`) REFERENCES `mahasiswa` (`npm`) ON DELETE CASCADE;

--
-- Constraints for table `nilai_tugas_detail`
--
ALTER TABLE `nilai_tugas_detail`
  ADD CONSTRAINT `nilai_tugas_detail_ibfk_1` FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah` (`id_matkul`) ON DELETE CASCADE,
  ADD CONSTRAINT `nilai_tugas_detail_ibfk_2` FOREIGN KEY (`npm`) REFERENCES `mahasiswa` (`npm`) ON DELETE CASCADE;

--
-- Constraints for table `nilai_uas`
--
ALTER TABLE `nilai_uas`
  ADD CONSTRAINT `nilai_uas_ibfk_1` FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah` (`id_matkul`) ON DELETE CASCADE,
  ADD CONSTRAINT `nilai_uas_ibfk_2` FOREIGN KEY (`npm`) REFERENCES `mahasiswa` (`npm`) ON DELETE CASCADE;

--
-- Constraints for table `nilai_uts`
--
ALTER TABLE `nilai_uts`
  ADD CONSTRAINT `nilai_uts_ibfk_1` FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah` (`id_matkul`) ON DELETE CASCADE,
  ADD CONSTRAINT `nilai_uts_ibfk_2` FOREIGN KEY (`npm`) REFERENCES `mahasiswa` (`npm`) ON DELETE CASCADE;

--
-- Constraints for table `persentase_matkul`
--
ALTER TABLE `persentase_matkul`
  ADD CONSTRAINT `persentase_matkul_ibfk_1` FOREIGN KEY (`id_matkul`) REFERENCES `mata_kuliah` (`id_matkul`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

