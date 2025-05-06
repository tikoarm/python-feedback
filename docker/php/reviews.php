<?php
$user_param = isset($_GET['user']) ? $_GET['user'] : null;

// If the parameter is not provided, show an error
if ($user_param === null) {
    echo json_encode(["error" => "Missing 'user' parameter"]);
    exit;
}

// Получаем JSON с Python API
$api_url = "http://app:5050/review_list/?user=" . urlencode($user_param);
$json = file_get_contents($api_url);
$reviews = json_decode($json, true);

echo "<h1>User Reviews</h1>";
echo "<h2>User filter: " . $user_param . "</h2>";

if (!$reviews || !is_array($reviews)) {
    echo "<p>Failed to load reviews.</p>";
} else {
    foreach ($reviews as $review) {
        echo "<div style='border: 1px solid #ccc; padding: 10px; margin-bottom: 15px;'>";
        echo "<em>#" . nl2br(htmlspecialchars($review['r_id'])) . "</em> <strong>Username:</strong> " . htmlspecialchars($review['u_name']) . "<br>";
        echo "<strong>Rating:</strong> " . nl2br(htmlspecialchars($review['r_stars'])) . "<br>";
        echo "<strong>Review:</strong> " . nl2br(htmlspecialchars($review['r_text'])) . "<br>";
        echo "<strong>AI Response:</strong> " . nl2br(htmlspecialchars($review['r_ai_answer'])) . "<br>";
        if ($review['a_text']) {
            echo "<br><strong>Admin Response:</strong> " . nl2br(htmlspecialchars($review['a_text'])) . "<br>";
            echo "<strong>From: </strong><em>" . htmlspecialchars($review['a_name']) . "</em> on " . nl2br(htmlspecialchars($review['a_date'])) . "<br>";
        }
        echo "<br><strong>Date:</strong> <em>" . htmlspecialchars($review['r_date']) . "</em>";
        echo "</div>";
    }
}
?>