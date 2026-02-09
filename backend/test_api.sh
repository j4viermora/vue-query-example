#!/bin/bash

# Script para probar la API de Reservas
# Asegúrate de que el servidor esté corriendo en http://localhost:8000

BASE_URL="http://localhost:8000"

echo "======================================"
echo "Test 1: Health Check"
echo "======================================"
curl -s $BASE_URL/health | python3 -m json.tool
echo -e "\n"

echo "======================================"
echo "Test 2: Crear Primera Reserva"
echo "======================================"
RESPONSE1=$(curl -s -X POST $BASE_URL/reservas \
  -H "Content-Type: application/json" \
  -d '{"fecha": "2026-02-15", "nombre_amenity": "Piscina"}')
echo "$RESPONSE1" | python3 -m json.tool
ID1=$(echo "$RESPONSE1" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['id'])")
echo "ID guardado: $ID1"
echo -e "\n"

echo "======================================"
echo "Test 3: Crear Segunda Reserva"
echo "======================================"
RESPONSE2=$(curl -s -X POST $BASE_URL/reservas \
  -H "Content-Type: application/json" \
  -d '{"fecha": "2026-02-20", "nombre_amenity": "Cancha de Tenis"}')
echo "$RESPONSE2" | python3 -m json.tool
ID2=$(echo "$RESPONSE2" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['id'])")
echo "ID guardado: $ID2"
echo -e "\n"

echo "======================================"
echo "Test 4: Listar Todas las Reservas"
echo "======================================"
curl -s $BASE_URL/reservas | python3 -m json.tool
echo -e "\n"

echo "======================================"
echo "Test 5: Obtener Reserva Específica"
echo "======================================"
curl -s $BASE_URL/reservas/$ID1 | python3 -m json.tool
echo -e "\n"

echo "======================================"
echo "Test 6: Actualizar Reserva"
echo "======================================"
curl -s -X PATCH $BASE_URL/reservas/$ID2 \
  -H "Content-Type: application/json" \
  -d '{"nombre_amenity": "Cancha de Tenis Olímpica"}' | python3 -m json.tool
echo -e "\n"

echo "======================================"
echo "Test 7: Verificar Actualización"
echo "======================================"
curl -s $BASE_URL/reservas/$ID2 | python3 -m json.tool
echo -e "\n"

echo "======================================"
echo "Test 8: Error 404 - Reserva No Existe"
echo "======================================"
curl -s $BASE_URL/reservas/invalid-uuid-12345 | python3 -m json.tool
echo -e "\n"

echo "======================================"
echo "Test 9: Eliminar Reserva"
echo "======================================"
echo "Código de respuesta:"
curl -s -o /dev/null -w "%{http_code}" -X DELETE $BASE_URL/reservas/$ID2
echo -e "\n"

echo "======================================"
echo "Test 10: Verificar Eliminación (404)"
echo "======================================"
curl -s $BASE_URL/reservas/$ID2 | python3 -m json.tool
echo -e "\n"

echo "======================================"
echo "Test 11: Lista Final (Una Reserva)"
echo "======================================"
curl -s $BASE_URL/reservas | python3 -m json.tool
echo -e "\n"

echo "======================================"
echo "Test 12: Error de Validación"
echo "======================================"
curl -s -X POST $BASE_URL/reservas \
  -H "Content-Type: application/json" \
  -d '{"fecha": "fecha-invalida", "nombre_amenity": ""}' | python3 -m json.tool
echo -e "\n"

echo "======================================"
echo "Todos los tests completados!"
echo "======================================"
