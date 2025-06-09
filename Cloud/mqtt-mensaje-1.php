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
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
        button {
            padding: 10px 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        .log {
            margin-top: 20px;
            border: 1px solid #ddd;
            padding: 10px;
            height: 200px;
            overflow-y: auto;
            background-color: #f9f9f9;
        }
        .mosquito {
            font-size: 24px;
            position: relative;
            animation: fly 3s infinite;
        }
        @keyframes fly {
            0% { transform: translateX(0) rotate(0deg); }
            25% { transform: translateX(50px) rotate(10deg); }
            50% { transform: translateX(100px) rotate(0deg); }
            75% { transform: translateX(50px) rotate(-10deg); }
            100% { transform: translateX(0) rotate(0deg); }
        }
    </style>
</head>
<body>
    <h1>MQTT Sender <span class="mosquito">🦟</span></h1>
    
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
        // Configuración
        $logFile = __DIR__ . '/mqtt_log.txt';  // Usamos __DIR__ para ruta absoluta
        $maxLogEntries = 20;
        
        // Procesar el envío del mensaje
        if (isset($_POST['send'])) {
            $ip = $_POST['ip'];
            $topic = $_POST['topic'];
            $message = $_POST['message'];
            $timestamp = date('Y-m-d H:i:s');
            
            // Comando para publicar el mensaje MQTT
            $cmd = "mosquitto_pub -h $ip -t '$topic' -m '$message' 2>&1";
            $output = shell_exec($cmd);
            
            // Registrar el mensaje
            $logEntry = "[$timestamp] Enviado a $ip - Tópico: $topic - Mensaje: $message";
            if (!empty($output)) {
                $logEntry .= " (Error: " . trim($output) . ")";
            }
            
            // Guardar en el archivo de log
            file_put_contents($logFile, $logEntry . PHP_EOL, FILE_APPEND);
            
            // Redirigir para evitar reenvío al recargar
            header("Location: ".$_SERVER['PHP_SELF']);
            exit();
        }
        
        // Mostrar el log
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
            // Intentar crear el archivo si no existe
            if (@file_put_contents($logFile, '') === false) {
                echo "No se pudo crear el archivo de log. Verifica los permisos en el directorio: " . htmlspecialchars(__DIR__);
            } else {
                echo "Archivo de log creado. Envía tu primer mensaje.";
            }
        }
        ?>
    </div>
</body>
</html>
