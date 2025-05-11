-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Хост: db
-- Время создания: Май 11 2025 г., 18:45
-- Версия сервера: 8.0.42
-- Версия PHP: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `feedback_db`
--

-- --------------------------------------------------------

--
-- Структура таблицы `answer`
--

CREATE TABLE `answer` (
  `id` int NOT NULL,
  `admin_id` int NOT NULL,
  `review_id` int NOT NULL,
  `text` varchar(128) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `answer`
--

INSERT INTO `answer` (`id`, `admin_id`, `review_id`, `text`, `date`) VALUES
(1, 2, 8, 'spasibo Artur', '2025-05-04 13:06:31');

-- --------------------------------------------------------

--
-- Структура таблицы `api_keys`
--

CREATE TABLE `api_keys` (
  `id` int NOT NULL,
  `api_key` varchar(128) NOT NULL,
  `created_by` int NOT NULL,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `api_keys`
--

INSERT INTO `api_keys` (`id`, `api_key`, `created_by`, `create_date`) VALUES
(1, '55bc56cf3c4eb12ea6e149674a0b298f', 1, '2025-05-09 17:03:07'),
(2, '3865ba2a8ee8eb7fab569bbf021dc1d7', 1, '2025-05-09 17:12:19'),
(3, '5fa87fd44fe2e9dd3492ce4ff94fe750', 1, '2025-05-09 17:16:01'),
(4, 'eabac29cb05a86606d4e6e8745e5874d', 1, '2025-05-09 17:25:45'),
(5, '252adf03cc475f26f97f97048a794d87', 1, '2025-05-09 18:00:25'),
(6, 'c5b5bfb5d4dcaa4f8d04831a6d719b4b', 1, '2025-05-11 13:41:51');

-- --------------------------------------------------------

--
-- Структура таблицы `reviews`
--

CREATE TABLE `reviews` (
  `id` int NOT NULL,
  `userid` int NOT NULL,
  `stars` int NOT NULL DEFAULT '1',
  `text` varchar(128) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ai_answer` varchar(256) NOT NULL DEFAULT '-'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `reviews`
--

INSERT INTO `reviews` (`id`, `userid`, `stars`, `text`, `date`, `ai_answer`) VALUES
(7, 1, 3, 'review 1 from Tigran', '2025-05-09 13:05:52', 'ai answer on 1'),
(8, 4, 5, 'review 2 from Artur', '2025-05-09 13:06:17', 'answer from ai to second review'),
(9, 1, 5, 'Большое спасибо, нам все понравилось', '2025-05-11 13:41:23', 'Большое спасибо за ваш отзыв! Мы очень рады, что вам все понравилось.\n');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `telegram_id` bigint NOT NULL,
  `name` varchar(32) NOT NULL,
  `admin` int NOT NULL DEFAULT '0',
  `source` varchar(64) NOT NULL DEFAULT 'Unknown',
  `reg_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `telegram_id`, `name`, `admin`, `source`, `reg_date`) VALUES
(1, 251464707, 'Tigran', 1, 'Unknown', '2025-05-02 19:29:26'),
(2, 1, 'root', 1, 'Unknown', '2025-05-03 09:40:51'),
(4, 592048273, 'Artur', 0, 'Unknown', '2025-05-03 16:39:25'),
(5, 464651097, 'Max', 0, 'Unknown', '2025-05-03 17:58:14');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `answer`
--
ALTER TABLE `answer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`),
  ADD KEY `review_id` (`review_id`);

--
-- Индексы таблицы `api_keys`
--
ALTER TABLE `api_keys`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`);

--
-- Индексы таблицы `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userid` (`userid`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `telegram_id` (`telegram_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `answer`
--
ALTER TABLE `answer`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `api_keys`
--
ALTER TABLE `api_keys`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `answer`
--
ALTER TABLE `answer`
  ADD CONSTRAINT `answer_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `answer_ibfk_2` FOREIGN KEY (`review_id`) REFERENCES `reviews` (`id`);

--
-- Ограничения внешнего ключа таблицы `api_keys`
--
ALTER TABLE `api_keys`
  ADD CONSTRAINT `api_keys_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Ограничения внешнего ключа таблицы `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
