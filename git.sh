#!/bin/bash

# Definir el nombre del archivo que contendrá el contador
COUNTER_FILE="contador.txt"

# Verificar si el archivo existe. Si no existe, crearlo e inicializar el contador en 1
if [ ! -f "$COUNTER_FILE" ]; then
    echo "1" > "$COUNTER_FILE"
fi

# Leer el valor actual del contador desde el archivo
COUNTER=$(cat "$COUNTER_FILE")

# Incrementar el contador en 1
COUNTER=$((COUNTER+1))

# Actualizar el archivo con el nuevo valor del contador
echo "$COUNTER" > "$COUNTER_FILE"

# Añadir todos los cambios al área de staging
git add .

# Realizar un commit con el mensaje que incluye el valor actual del contador
git commit -m "contador = $COUNTER"

# Subir los cambios al repositorio remoto (cambiar 'main' por 'master' si es necesario)
git pull origin main

# chmod +x git.sh y para ejecutarlo ./git.sh
