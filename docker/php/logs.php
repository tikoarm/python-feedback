

<?php
$admin_key = 'admin_sk-1NfzR3wTbv8Kqz7YLopFD4MJuxn2EG59'; // замените на настоящий ключ
$log_type = $_GET['type'] ?? 'info'; // можно менять на 'error', 'warning' и т.д.

$url = "http://app:5050/logs/view?admin_key=$admin_key&log_type=$log_type";

// Инициализация cURL
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HEADER, false);

// Выполнение запроса
$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$error_msg = curl_error($ch);
curl_close($ch);

// Обработка ошибки соединения
if ($response === false) {
    echo "<p>cURL error: " . htmlspecialchars($error_msg) . "</p>";
    exit;
}

// Проверка кода ответа
if ($http_code >= 400) {
    echo "<p>API returned HTTP status $http_code</p>";
}

// Декодирование JSON
$data = json_decode($response, true);
if (!$data) {
    echo "<p>Failed to decode response.</p>";
    exit;
}

if (isset($data['error'])) {
    echo "<p>Error: " . htmlspecialchars($data['error']) . "</p>";
    exit;
}

if (!isset($data['lines'])) {
    echo "<p>Failed to load logs.</p>";
    exit;
}

// Кнопки для выбора типа логов
echo "<div style='margin-bottom: 10px;'>
        <a href='?type=info'><button>Info</button></a>
        <a href='?type=warning'><button>Warning</button></a>
        <a href='?type=error'><button>Error</button></a>
      </div>";
// Вывод логов
echo "<h2>Logs ($log_type)</h2><pre>";
foreach ($data['lines'] as $line) {
    echo htmlspecialchars($line);
}
echo "</pre>";
?>