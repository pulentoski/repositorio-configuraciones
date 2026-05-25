# 🔐 Recuperación de Contraseña en Cisco IOS mediante ROMMON

## 📌 Descripción
Procedimiento para eliminar la contraseña de un router Cisco utilizando el modo ROMMON mediante acceso por consola.

---

# Paso 1: Interrumpir el Proceso de Arranque

Conectar el router mediante cable de consola y reiniciar el equipo.

Durante los primeros segundos del arranque, enviar la señal de interrupción (Break) según el emulador utilizado:

| Software | Combinación |
|---|---|
| PuTTY / Tera Term / HyperTerminal | `Ctrl + Break` |
| Laptops (sin tecla Break) | `Fn + Pause/Break` |
| SecureCRT | `Ctrl + Shift + 6` luego `b` |
| Minicom (Linux) | `Ctrl + A` luego `F` |
| macOS Terminal (screen) | `Ctrl + A` luego `Ctrl + \` |

Al realizar correctamente la interrupción, aparecerá el prompt:

```plaintext
rommon 1 >
```

---

# Paso 2: Modificar el Registro de Configuración

Configurar el registro para ignorar la configuración almacenada en la NVRAM.

```plaintext
rommon 1 > confreg 0x2142
```

📌 `0x2142` permite iniciar el router ignorando la `startup-config`.

---

# Paso 3: Reiniciar el Router

Reiniciar el equipo para aplicar el nuevo registro.

```plaintext
rommon 2 > reset
```

---

# Paso 4: Borrar la Configuración Antigua

Una vez iniciado el router, acceder al modo privilegiado y eliminar la configuración almacenada.

```plaintext
Router> enable
Router# erase startup-config
```

Confirmar el borrado:

```plaintext
Erasing the nvram filesystem will remove all configuration files! Continue? [confirm]
[OK]
Erase of nvram: complete
```

---

# Paso 5: Restaurar el Registro de Configuración

Ingresar al modo de configuración global y restaurar el registro normal de arranque.

```plaintext
Router# configure terminal
Router(config)# config-register 0x2102
```

📌 `0x2102` indica al router cargar normalmente la `startup-config` desde la NVRAM.

---

# Paso 6: Guardar y Reiniciar

Salir de configuración y reiniciar el equipo.

```plaintext
Router(config)# exit
Router# reload
```

Guardar la configuración vacía:

```plaintext
System configuration has been modified. Save? [yes/no]: yes
Building configuration...
[OK]
```

Confirmar el reinicio:

```plaintext
Proceed with reload? [confirm]
```

---

# ✅ Resultado

El router iniciará normalmente:

- Sin contraseñas configuradas.
- Con configuración vacía.
- Utilizando el registro `0x2102`.

---
