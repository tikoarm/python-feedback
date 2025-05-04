<?php
// Получаем JSON с Python API
$json_url = 'http://app:5050/review_list';
$json = file_get_contents($json_url);
$reviews = json_decode($json, true);

echo "<h1>Отзывы пользователей</h1>";

if (!$reviews || !is_array($reviews)) {
    echo "<p>Не удалось загрузить отзывы.</p>";
} else {
    foreach ($reviews as $review) {
        echo "<div style='border: 1px solid #ccc; padding: 10px; margin-bottom: 15px;'>";
        echo "<em>#" . nl2br(htmlspecialchars($review['r_id'])) . "</em> <strong>Имя пользователя:</strong> " . htmlspecialchars($review['u_name']) . "<br>";
        echo "<strong>Оценка:</strong> " . nl2br(htmlspecialchars($review['r_stars'])) . "<br>";
        echo "<strong>Отзыв:</strong> " . nl2br(htmlspecialchars($review['r_text'])) . "<br>";
        echo "<strong>Ответ AI:</strong> " . nl2br(htmlspecialchars($review['r_ai_answer'])) . "<br>";
        if ($review['a_text']) {
            echo "<br><strong>Ответ администратора:</strong> " . nl2br(htmlspecialchars($review['a_text'])) . "<br>";
            echo "<strong>От: </string><em>" . htmlspecialchars($review['a_name']) . "</em> в " . nl2br(htmlspecialchars($review['a_date'])) . "<br>";
        }
        echo "<br><strong>Дата:</strong> <em>" . htmlspecialchars($review['r_date']) . "</em>";
        echo "</div>";
    }
}
?>