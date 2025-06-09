<!DOCTYPE html>
<html>
<head>
    <title>MQTT Sender</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
            background-color: #f5f5f5;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 10px;
            box-sizing: border-box;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 12px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #45a049;
        }
        .log {
            margin-top: 20px;
            border: 1px solid #ddd;
            padding: 15px;
            height: 200px;
            overflow-y: auto;
            background-color: white;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        /* Estilos para los mosquitos */
        .mosquito {
            position: absolute;
            font-size: 28px;
            z-index: 100;
            pointer-events: none;
            user-select: none;
        }
        
        /* Animaciones para cada mosquito */
        .mosquito1 {
            animation: fly1 15s linear infinite;
            top: 10%;
            left: -50px;
        }
        .mosquito2 {
            animation: fly2 12s linear infinite;
            top: 30%;
            left: -50px;
        }
        .mosquito3 {
            animation: fly3 18s linear infinite;
            top: 70%;
            left: -50px;
        }
        
        @keyframes fly1 {
            0% { transform: translateX(0) translateY(0) rotate(0deg); }
            25% { transform: translateX(200px) translateY(20px) rotate(10deg); }
            50% { transform: translateX(400px) translateY(0) rotate(0deg); }
            75% { transform: translateX(600px) translateY(-20px) rotate(-10deg); }
            100% { transform: translateX(1000px) translateY(0) rotate(0deg); }
        }
        
        @keyframes fly2 {
            0% { transform: translateX(0) translateY(0) rotate(0deg); }
            25% { transform: translateX(150px) translateY(-15px) rotate(-5deg); }
            50% { transform: translateX(300px) translateY(0) rotate(0deg); }
            75% { transform: translateX(450px) translateY(15px) rotate(5deg); }
            100% { transform: translateX(1000px) translateY(0) rotate(0deg); }
        }
        
        @keyframes fly3 {
            0% { transform: translateX(0) translateY(0) rotate(0deg); }
            25% { transform: translateX(300px) translateY(10px) rotate(5deg); }
            50% { transform: translateX(600px) translateY(-10px) rotate(-5deg); }
            75% { transform: translateX(900px) translateY(5px) rotate(2deg); }
            100% { transform: translateX(1200px) translateY(0) rotate(0deg); }
        }
        
        h1 {
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
    </style>
</head>
<body>
    <!-- Mosquitos volando -->
    <div class="mosquito mosquito1">🦟</div>
    <div class="mosquito mosquito2">🦟</div>
    <div class="mosquito mosquito3">🦟</div>
    
    <h1>MQTT Sender</h1>
    
    <!-- [Resto del formulario y código PHP se mantiene igual] -->
    <form method="post">
        <div class="form-group">
            <label for="ip">Broker IP:</label>
            <input type="text" id="ip" name="ip" placeholder="ej: 192.168.1.100" required>
        </div>
        
        <div class="form-group">
            <label for="topic">Tópico:</label>
            <input type="text" id="topic" name="topic" placeholder="ej: casa/sala/luz" required>
        </div>
        
        <div class="form-group">
            <label for="message">Mensaje:</label>
            <input type="text" id="message" name="message" placeholder="ej: encender" required>
        </div>
        
        <button type="submit" name="send">Enviar Mensaje</button>
    </form>
    
    <div class="log">
        <h3>Registro de Mensajes:</h3>
        <?php
        $logFile = '/var/www/html/mqtt_log.txt';
        $maxLogEntries = 20;
        
        if (isset($_POST['send'])) {
            $ip = $_POST['ip'];
            $topic = $_POST['topic'];
            $message = $_POST['message'];
            $timestamp = date('Y-m-d H:i:s');
            
            $cmd = "mosquitto_pub -h $ip -t '$topic' -m '$message' 2>&1";
            $output = shell_exec($cmd);
            
            $logEntry = "[$timestamp] Enviado a $ip - Tópico: $topic - Mensaje: $message";
            if (!empty($output)) {
                $logEntry .= " (Error: " . trim($output) . ")";
            }
            
            file_put_contents($logFile, $logEntry . PHP_EOL, FILE_APPEND);
            header("Location: ".$_SERVER['PHP_SELF']);
            exit();
        }
        
        if (file_exists($logFile)) {
            $logContent = file($logFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
            if ($logContent === false) {
                echo "Error al leer el archivo de log.";
            } else {
                $logContent = array_reverse($logContent);
                $logContent = array_slice($logContent, 0, $maxLogEntries);
                
                foreach ($logContent as $entry) {
                    echo htmlspecialchars($entry) . "<br>";
                }
            }
        } else {
            echo "Archivo de log no accesible.";
        }
        ?>
    </div>
</body>
</html>
