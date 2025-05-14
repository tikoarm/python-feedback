<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Feedback Demo – Tikoarm</title>
  <style>
    body {
      font-family: sans-serif;
      max-width: 800px;
      margin: 50px auto;
      padding: 0 20px;
      color: #333;
    }
    h1 {
      text-align: center;
    }
    .section {
      margin-bottom: 30px;
    }
    a {
      color: #007acc;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    code {
      background: #f3f3f3;
      padding: 2px 5px;
      border-radius: 3px;
    }
  </style>
</head>
<body>
  <h1>📬 Feedback Bot Demo</h1>

  <div class="section">
    <strong>Telegram bot:</strong><br>
    <a href="https://t.me/feedback_demobot?start=source_feedback_tikoarm_com" target="_blank">
      @feedback_demobot
    </a>
  </div>

  <div class="section">
    <strong>Access Info:</strong>
    <ul>
      <li>
        <strong>🔑 phpMyAdmin login:</strong> available on request (contact developer)
        <br>
        <a href="http://db.feedback.tikoarm.com/" target="_blank">db.feedback.tikoarm.com</a>
      </li>
      <li>
        <strong>🌐 Web Interface:</strong>
        <ul>
          <li><a href="http://feedback.tikoarm.com/reviews.php" target="_blank">reviews.php</a><br>Required params: <code>user ['all' / id]</code></li>
          <li><a href="http://feedback.tikoarm.com/logs.php" target="_blank">logs.php</a></li>
          <li><a href="http://feedback.tikoarm.com/index.php" target="_blank">index.php</a></li>
        </ul>
      </li>
      <li>
        <strong>📡 API Endpoints:</strong>
        <ul>
          <li>
            <code>GET /review_list/</code> – full review list for PHP frontend<br>
            Required params: <code>api_key</code>, <code>user [all/id]</code><br>
          </li>
          <li>
            <code>POST /apikey/add</code> – create API key<br>
            Required params: <code>admin_key</code>, <code>user_id</code>
          </li>
          <li>
            <code>GET /logs/view</code> – retrieve log contents<br>
            Required params: <code>admin_key</code>, <code>log_type</code> (<code>warning</code> | <code>error</code> | <code>info</code>)
          </li>
          <li>
            <code>GET /health</code> – retrieves service health status (uptime, version, database)<br>
            <a href="http://api.feedback.tikoarm.com/health" target="_blank">Open /health</a>
          </li>
          <li><em>Note: <code>api_key</code> is public (see example above). <code>admin_key</code> is available on request (contact developer).</em></li>
        </ul>
        Base API URL: <a href="http://api.feedback.tikoarm.com/" target="_blank">api.feedback.tikoarm.com</a>
        <br>
        Example public API key: <code>143160c030063f7f7d8b1572da68e91a</code>
      </li>
    </ul>
  </div>

  <hr>
  <small>
    Powered by Docker, Flask, PHP, MySQL and Nginx on Ubuntu 20.04 VPS.
  </small>
</body>
</html>