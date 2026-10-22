# A Un Punto

Aplicación móvil en Python para que una luchadora de alto rendimiento registre su día en segundos y reciba, de un vistazo, cuatro respuestas: si está cargando de más, si su control de peso va por buen camino, si está recuperada y cuándo conviene consultar a un especialista.

Basada en el perfil anónimo de una luchadora de lucha libre femenil, división de 57 kg, de la selección mexicana. Los datos fisiológicos de la muestra son simulados con valores de la literatura científica.

## Qué resuelve

1. Carga y lesión: calcula la carga diaria (minutos por esfuerzo), la compara contra las últimas 4 semanas y avisa antes de que aparezca el dolor.
2. Control de peso: acompaña el descenso hacia la división según el calendario de competencias, con límites prudentes por fase.
3. Recuperación: combina sueño, pulso, variabilidad cardiaca, fatiga, dolor, bienestar e hidratación en un índice de 0 a 100 contra la línea base personal.
4. Que el dato llegue: formulario de un minuto, valores sugeridos del día anterior, validación inmediata y mensajes que enseñan a registrar bien.

## Ejecutar en la computadora

1. Instala Python 3.11 o superior.
2. Instala las dependencias: `pip install kivy matplotlib openpyxl plyer`
3. Desde la carpeta del proyecto: `python main.py`

La ventana se abre con proporción de teléfono. La primera vez se cargan los 14 días de la muestra. En Más puedes importar el Excel completo o cargar la demostración de 182 días (simulada).

## Generar el APK para Android

Se usa Buildozer, que funciona en Linux o en macOS. En Windows usa WSL.

1. Instala Buildozer: `pip install buildozer cython`
2. Desde la carpeta del proyecto: `buildozer android debug`
3. El APK queda en la carpeta bin. Cópialo al teléfono e instálalo.

La primera compilación descarga el kit de Android y tarda entre 20 y 40 minutos. El archivo buildozer.spec ya incluye nombre, icono, permisos y dependencias.

## Estructura del proyecto

1. main.py: punto de entrada.
2. aunpunto/modelos.py: clases de datos (RegistroDiario, Competencia, Salto, Lesion, Alerta) y niveles del semáforo.
3. aunpunto/configuracion.py: paleta de color y umbrales editables (Umbrales).
4. aunpunto/repositorio.py: base de datos SQLite local (Repositorio).
5. aunpunto/importador.py: lectura de Excel y CSV (ImportadorDatos).
6. aunpunto/limpieza.py: datos faltantes (Imputador) y congruencia del registro (ValidadorRegistro).
7. aunpunto/metricas: AnalizadorCarga, AnalizadorRecuperacion, AnalizadorPeso, AnalizadorSaltos y AnalizadorDolor.
8. aunpunto/alertas.py: MotorAlertas, con mensajes de salud, de calidad del dato y de uso.
9. aunpunto/servicio.py: ServicioAtleta, la fachada que integra todo y entrega el resumen del día.
10. aunpunto/graficas.py: GeneradorGraficas.
11. aunpunto/informes.py: GeneradorInforme (PDF semanal y precompetencia).
12. aunpunto/ui: tema, componentes, pantallas y la aplicación Kivy (AUnPuntoApp).
13. datos: muestra oficial, demostración simulada e iconos.
14. herramientas: generador de la demostración y revisor de estilo.
15. pruebas: pruebas del núcleo y de la interfaz con un simulador de Kivy.

El flujo es siempre el mismo: la interfaz llama a ServicioAtleta; el servicio lee del Repositorio, limpia con Imputador, calcula con los analizadores y traduce a mensajes con MotorAlertas.

## Fórmulas

1. Carga del día = minutos por esfuerzo percibido (escala de 0 a 10).
2. Carga aguda y crónica: promedio móvil exponencial con lambda = 2 / (N + 1), N = 7 y N = 28.
3. Relación de carga = aguda / crónica. Zona recomendada de 0.8 a 1.3; precaución arriba de 1.3; riesgo alto arriba de 1.5.
4. Monotonía = promedio de 7 días / desviación estándar de 7 días. Alerta arriba de 2.
5. Strain = suma semanal por monotonía.
6. Índice de disponibilidad = 50 + 10 por la suma ponderada de los puntajes z de cada variable contra sus 28 días previos. Ámbar debajo de 45 y rojo debajo de 35.
7. Altura promedio de saltos = promedio de SJ, CMJ y ABK de cada toma.
8. Índice de elasticidad = (CMJ menos SJ) / SJ por 100. Índice de brazos = (ABK menos CMJ) / CMJ por 100.
9. Porcentaje sobre la división = peso / división por 100, menos 100.
10. Pérdida semanal = (peso de hace 7 días menos peso de hoy) / peso de hace 7 días por 100.

## Control de peso por fase

1. Mantenimiento, más de 42 días al pesaje: hasta 8 % sobre la división.
2. Descenso crónico, de 42 a 8 días: de 0.5 a 1 % por semana; alerta arriba de 1.5 %.
3. Descenso agudo, de 7 a 0 días: no más de 3 % en 72 horas ni 5 % en 7 días.
4. Recuperación: el rebote no debe superar la tolerancia de 2 kg si hay segundo pesaje.

Las fechas de competencia se deducen de la columna dias_a_competencia y se pueden capturar a mano en Más, Calendario de competencias.

## Alertas

Salud y rendimiento: carga muy alta o en aumento, semana que sube de golpe, monotonía, recuperación baja, dolor intenso, molestia repetida en la misma zona, variabilidad baja dos días, pulso elevado, deshidratación, deshidratación con carga alta, pérdida de peso rápida o insegura, rebote excesivo, asimetría entre piernas y caída del salto.

Calidad del dato: campos obligatorios, valores fuera de rango, fecha futura, descanso con minutos, sesión sin minutos, esfuerzo sin minutos, dolor sin zona, zona sin dolor, cambio de peso inusual, horas de sueño extremas y registro tardío.

Uso del sistema: registrar el día, días sin registro, relación de carga en calibración, datos estimados, competencia pendiente en el calendario y evaluación de saltos pendiente.

Una alerta roja de calidad impide guardar; una ámbar pide confirmación. Toda alerta de salud dice qué hacer y, cuando corresponde, indica consultar a un especialista.

## Datos faltantes

1. Variables continuas (sueño, pulso, variabilidad): si falta un solo día se promedia con sus vecinos.
2. Escalas de 1 a 5 y orina: mediana de los 7 días previos si hay al menos 3 valores reales.
3. Carga: nunca se estima.
4. Peso: nunca se estima en los 10 días previos a competir.
5. Descanso y viaje cuentan como carga 0 porque son datos reales.
6. La relación de carga se muestra solo con 21 de 28 días registrados.

Todo valor estimado queda marcado y se dibuja como punto hueco.

## Paleta

Negro 141414, grafito 2A2A2C, beige F3EEE4 y E5DCCB, blanco FFFFFF, grises 55565A, 8A8B8F y D7D3CB, azules 1C2E4A, 2F5D8A, 6E93B8 y C9D8E8. Verde 2E7D4F, ámbar C8891C y rojo B03A3A se reservan para semáforos, alertas y gráficas. Los umbrales se pueden ajustar con un archivo umbrales.json en la carpeta de datos de la app.

## Pruebas y estilo

1. Pruebas: `python ejecutar_pruebas.py`
2. Reglas de estilo: `python herramientas/revisar_estilo.py`

El revisor confirma que no haya emojis, rayas, signos de desplazamiento ni flechas, y que en el código el guion aparezca solo como operador de resta.

## Aviso de salud

El sistema orienta y no diagnostica. Sus umbrales son puntos de partida de la literatura y deben validarse con el cuerpo médico. Los datos se guardan solo en el teléfono.
