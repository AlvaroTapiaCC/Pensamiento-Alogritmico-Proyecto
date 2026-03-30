# Sistema de Planificación de Tareas
## Algoritmos y Optimización

## 1. Introducción

En este proyecto deben construir un sistema de planificación de tareas (scheduling).
Se les entregará un conjunto de tareas (cada una con duración y categoría) y un conjunto finito de recursos de procesamiento (cada recurso soporta ciertas categorías). Su trabajo consiste en asignar tareas a recursos y decidir en qué momento se ejecutan, de manera que el cronograma resultante sea válido (cumpla las restricciones) y minimice el **makespan**: el instante en que termina la última tarea del sistema.

Este tipo de problemas aparece en contextos reales como: planificación de producción, uso de máquinas en una planta, asignación de servidores a jobs, turnos de atención, y coordinación de equipos con capacidades distintas.

El desafío está en diseñar un algoritmo que produzca cronogramas válidos con el menor makespan posible.

### Ejemplo visual

Supongamos 4 tareas y 2 recursos. Un cronograma posible sería:

```
Recurso 1: [  T1 (5)  ][  T3 (4)  ]
Recurso 2: [ T2 (3) ][   T4 (6)   ]
            |----|----|----|----|----|----|
            0    2    4    6    8    9   10
                                    ^
                                    Makespan = 9
```

En este ejemplo el makespan es 9, porque es el instante en que termina la última tarea (T3 en Recurso 1). El objetivo es lograr que ese número sea lo menor posible.

Un cronograma **malo** asignaría todo a un solo recurso:

```
Recurso 1: [  T1 (5)  ][ T2 (3) ][  T3 (4)  ][   T4 (6)   ]
Recurso 2:
            |----|----|----|----|----|----|----|----|----|----|
            0         5        8        12        18
                                                   ^
                                                   Makespan = 18
```

Mismo problema, pero el doble de makespan.

### Ejemplo con categorías

Ahora agreguemos categorías. Supongamos 4 tareas y 3 recursos:

- T1 (duración 5, categoría A)
- T2 (duración 3, categoría B)
- T3 (duración 4, categoría A)
- T4 (duración 6, categoría B)

Y los recursos tienen distintas compatibilidades:

- R1 soporta: A
- R2 soporta: B
- R3 soporta: A, B

R1 solo puede ejecutar tareas de categoría A (T1, T3). R2 solo puede ejecutar tareas de categoría B (T2, T4). R3 puede ejecutar cualquiera.

Un cronograma válido:

```
R1: [  T1 (5)  ]
R2: [ T2 (3) ][   T4 (6)   ]
R3: [  T3 (4)  ]
     |----|----|----|----|----|----|
     0         5         9
                         ^
                         Makespan = 9
```

Un cronograma **inválido** sería asignar T2 (categoría B) a R1 (solo soporta A). Aunque el makespan fuera menor, la solución no es válida porque viola la restricción de compatibilidad.

## 2. Descripción

Deben implementar un planificador que, a partir de los archivos de entrada, construya un cronograma donde cada tarea:

- Quede asignada a un recurso compatible (según categoría).
- Tenga un tiempo de inicio y un tiempo de término.
- Se ejecute sin interrupciones (una vez que empieza, termina).
- No se solape con otra tarea en el mismo recurso (un recurso hace solo una tarea a la vez).

El planificador debe ser capaz de operar bajo tareas heterogéneas (duraciones distintas) y bajo recursos con capacidades diferentes (cada recurso soporta un conjunto de categorías).

El objetivo es **minimizar el makespan**: lograr que el instante en que termina la última tarea sea lo menor posible.

El resultado final de su algoritmo será un archivo `output.txt` con el cronograma encontrado.

## 3. Entradas y Ejecución

El programa debe leer los archivos de entrada y generar el archivo de salida.

Formato de ejecución:

```bash
python main.py <makespan_objetivo>
```

Ejemplo:
```bash
python main.py 12
```

- **Argumento:** `makespan_objetivo` - valor numérico que debe alcanzar o mejorar su solución
- **Tiempo máximo de ejecución:** El programa tiene un máximo de **10 segundos** por instancia de prueba. Si excede ese tiempo, se considera que no terminó.
- **Máquina de evaluación:** La evaluación se realizará en una máquina provista por el curso con las siguientes especificaciones: **1 núcleo de CPU y 4 GB de RAM** (mismo entorno que el devcontainer).

El programa debe leer automáticamente los archivos `tareas.txt` y `recursos.txt` en el directorio actual, construir el mejor cronograma posible, y escribir el resultado en `output.txt`. Se asume formato CSV (separado por comas).

> **Nota:** Pueden asumir que los datos de entrada siempre son válidos. Toda tarea tiene al menos un recurso compatible, y los archivos siempre cumplen el formato especificado. No es necesario validar los datos de entrada.

### 3.1 Archivo tareas.txt

Columnas: ID, Duración, Categoría

```
T1,5,CAT_A
T2,3,CAT_B
T3,4,CAT_A
T4,6,CAT_C
```

### 3.2 Archivo recursos.txt

Columnas: ID, Categoría_1, Categoría_2, ...

```
R1,CAT_A
R2,CAT_B,CAT_C
R3,CAT_A,CAT_B,CAT_C
```

### 3.3 Salida esperada: output.txt

El algoritmo debe generar este archivo con la solución. El archivo **no lleva header** (sin línea de encabezado).

Columnas: ID_Tarea, ID_Recurso, Tiempo_Inicio, Tiempo_Fin

```
T1,R1,0,5
T2,R2,0,3
T3,R3,0,4
T4,R2,3,9
```

El formato es CSV sin espacios (aunque el sistema acepta espacios opcionales).

## 4. Restricciones del Modelo

El cronograma generado debe cumplir **estrictamente** las siguientes restricciones. Una solución que viole cualquiera de ellas se considera **inválida**.

1. **Atomicidad:** Las tareas no pueden ser interrumpidas una vez iniciadas.
2. **Compatibilidad:** Un recurso solo puede ejecutar tareas cuya categoría esté incluida en sus categorías soportadas.
3. **Exclusividad:** Un recurso ejecuta una sola tarea a la vez (no puede haber solapamiento temporal).
4. **Tiempo:** El tiempo de inicio de cualquier tarea debe ser ≥ 0.
5. **Completitud:** Todas las tareas del archivo de entrada deben aparecer en el cronograma de salida.

## 5. Equipos de Trabajo

- Los grupos son de **3 estudiantes**.
- Los grupos se forman libremente entre los alumnos.
- Todos los integrantes deben contribuir al código. Ver sección de reglas Git.

## 6. Lenguaje y Herramientas

- **Lenguaje:** Python 3 con tipado estático. Se debe usar `mypy` para verificar tipos.
- **Librerías:** Se permite y fomenta el uso de librerías externas (numpy, etc.). No reinventen la rueda.
- **IA:** Se permite el uso de herramientas de IA como asistente de programación.
- **Git/GitHub:** El código debe estar en un repositorio de GitHub. El repositorio es parte de la entrega.

### Estructura mínima del repositorio

```
/
├── main.py              # Punto de entrada del programa (obligatorio en la raíz)
├── docs/
│   └── diagrama.pdf     # Diagrama de estrategia (o .png, .md, etc.)
└── ...                  # Otros archivos y módulos de su solución
```

El archivo `main.py` **debe estar en la raíz** del repositorio. Es el archivo que se ejecutará para evaluar su solución.

### Reglas de Git

- **Únicamente se evalúa lo que este en `main`.** El código debe estar en `main` al momento de la entrega. Commits en otras ramas no serán considerados para la evaluación.
- Cada integrante debe tener commits en `main`. Un integrante sin commits no cumple el requisito mínimo de participación (ver sección de evaluación).
- Se espera un mínimo de 10 commits por grupo. Una frecuencia menor puede resultar en descuentos.
- Los commits deben ser frecuentes y contar con mensajes descriptivos del cambio realizado.

## 7. Evaluación y Nota Final

### Causas de Calificación Mínima

Las siguientes situaciones resultan en una nota final de **1.0**, sin posibilidad de compensación mediante otros componentes:

- **Ausencia de participación:** Un integrante sin commits en `main`.
- **Solución no funcional:** Programa que no genera `output.txt`, produce errores de ejecución o viola restricciones del modelo.

### Ponderación Final

| Condición | EP | EF | Control |
|---|---|---|---|
| Control ≥ 3.95 | 20% | 50% | 30% |
| Control < 3.95 | 20% | 30% | 50% |

### Entrega Parcial (EP)

Evaluación presencial (23/03) con instancias simplificadas (≤20 tareas, una categoría).

| Aspecto | Peso | Criterio |
|---|---|---|
| Diagrama de estrategia | 30% | Presentación del diagrama |
| Código funcional | 70% | Generación de `output.txt` válido |

### Entrega Final (EF)

Evaluación de instancias complejas (cientos/miles de tareas, múltiples categorías).

| Aspecto | Peso | Criterio |
|---|---|---|
| Diagrama actualizado | 15% | Actualización respecto a la EP |
| Código funcional | 35% | Cumplir umbrales (CPU < 10s, makespan ≤ objetivo) |
| Competencia CPU | 25% | Menor tiempo de CPU (promedio de 3 ejecuciones) |
| Competencia makespan | 25% | Menor makespan obtenido (promedio de 3 ejecuciones) |

**Importante:** Si no se cumplen los umbrales (CPU < 10s y makespan ≤ objetivo), la nota de la EF será **1.0**.

## 8. Datos de Prueba

- **Datos EP:** Instancias pequeñas, una categoría.
- **Datos EF:** Instancias grandes, múltiples categorías.
- **Verificador:** Script `verificador.py` para validar soluciones.

## 9. Consideraciones de Honestidad

El estudiante debe ser dueño absoluto de su código. El cuerpo docente se reserva el derecho a separar grupos o interrogar a estudiantes sobre su implementación.
