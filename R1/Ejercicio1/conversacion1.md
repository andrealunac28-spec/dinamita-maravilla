# Conversación sobre el Problema B1 --- Ronda 1

## Solicitud inicial

**Usuario**

Actúa como un experto en programación competitiva y algoritmos
avanzados. Necesito resolver el "Problema B1" de un concurso de
programación.

Reglas y restricciones indicadas: - Hay T casos de prueba, con una suma
total de N ≤ 10\^6. - Cada caso tiene N sensores con valores decimales
de hasta 6 decimales, negativos o positivos, o el carácter `?`. -
Tolerancia K de hasta 1.8 × 10\^13. - Se busca la racha más larga de
sensores consecutivos considerados estables con tolerancia K. - Se
imprime la longitud L y la posición inicial P, basada en 1. - En caso de
empate, se elige la menor posición. - Límites: 8 segundos y 256 MB. - Se
solicitó una explicación de la estrategia y código completo en C++.

## Revisión del enunciado original

El PDF adjunto `Ronda1_Basica.pdf`, página 1, indica que el problema
deja reglas por descubrir mediante una caja negra: - Qué significa
exactamente "estable con tolerancia K". - Qué cuenta como sensores
"consecutivos". - Qué hace el sistema con los sensores `?`.

El PDF especifica que la entrada contiene T, y para cada caso una línea
con N y K y una línea con N lecturas. La salida contiene `L P`.

Los ejemplos oficiales muestran estas salidas:

**Ejemplo 1**

``` text
2 1
6 1
2 2
```

**Ejemplo 2**

``` text
3 1
2 4
```

## Primera estrategia propuesta

Se planteó como hipótesis que una ventana es estable cuando:

``` text
maximo - minimo <= K
```

Para mantener el máximo y el mínimo de una ventana deslizante en tiempo
amortizado O(1), se propusieron dos deques monotónicas: - Una deque de
máximos, con índices en orden decreciente de valores. - Una deque de
mínimos, con índices en orden creciente de valores.

Con dos apuntadores, `left` y `right`, se amplía la ventana y se mueve
`left` mientras la diferencia entre máximo y mínimo supere K.

Cada índice entra y sale de cada deque como máximo una vez. Por ello, el
tiempo total es O(N) amortizado.

También se indicó que los decimales pueden convertirse a enteros
multiplicando por 1 000 000, evitando errores de coma flotante.

## Solicitud de versión en Python

**Usuario**

Dame el código completo en Python.

**Respuesta**

Se proporcionó una implementación Python con: - `collections.deque`. -
Conversión decimal exacta a enteros escalados por 10\^6. - Dos deques
monotónicas. - Dos apuntadores para la ventana deslizante. - La
hipótesis de que `?` rompe la racha.

Se advirtió que el PDF no confirma el significado de estabilidad ni el
comportamiento de `?`, por lo que las reglas deben verificarse con la
caja negra.

## Solicitud de revisión más estricta

**Usuario**

Dame el código biennn, pero bien bien, ocupo que se ejecute al 100.

**Respuesta**

Se entregó otra versión que utiliza: - `array('q')` para almacenar los
valores de forma compacta. - `deque` para máximos y mínimos. - Enteros
escalados para mantener precisión. - Comparación estricta de la longitud
para conservar la primera posición en caso de empate.

Se volvió a aclarar que no se puede garantizar el 100 % de aceptación
sin confirmar las reglas ocultas mediante la caja negra y medir el
rendimiento en el juez.

## Solicitud de corrección de ejecución

**Usuario**

Revísalo súper bien porque ocupo que corra y se ejecute y no me deja
ejecutarlo.

**Respuesta**

Se entregó una versión que lee toda la entrada con
`sys.stdin.buffer.read().split()`, por lo que no depende de que las
lecturas de un caso estén en una sola línea.

### Última versión de Python entregada

``` python
import sys
from collections import deque
from array import array

SCALE = 1_000_000


def to_scaled_int(s):
    \"\"\"Convierte un decimal de hasta 6 posiciones a entero exacto.\"\"\"

    negative = False

    if s[0] == 45:
        negative = True
        s = s[1:]
    elif s[0] == 43:
        s = s[1:]

    integer_part, dot, fractional_part = s.partition(b'.')

    integer = int(integer_part)

    if dot:
        fractional_part = fractional_part[:6].ljust(6, b'0')
        fraction = int(fractional_part)
    else:
        fraction = 0

    result = integer * SCALE + fraction

    return -result if negative else result


def solve():
    data = iter(sys.stdin.buffer.read().split())

    T = int(next(data))
    answers = []

    for _ in range(T):

        n = int(next(data))
        K = to_scaled_int(next(data))

        # Almacenar valores con precisión exacta.
        values = array('q', [0]) * n

        # Deques monotónicas.
        min_dq = deque()
        max_dq = deque()

        left = 0

        best_length = 0
        best_position = 1

        for right in range(n):

            token = next(data)

            # Un sensor perdido rompe la racha.
            if token == b'?':
                min_dq.clear()
                max_dq.clear()
                left = right + 1
                continue

            value = to_scaled_int(token)
            values[right] = value

            # Actualizar deque de mínimos.
            while min_dq and values[min_dq[-1]] >= value:
                min_dq.pop()

            min_dq.append(right)

            # Actualizar deque de máximos.
            while max_dq and values[max_dq[-1]] <= value:
                max_dq.pop()

            max_dq.append(right)

            # Reducir la ventana mientras exceda K.
            while (
                values[max_dq[0]] - values[min_dq[0]] > K
            ):

                if min_dq[0] == left:
                    min_dq.popleft()

                if max_dq[0] == left:
                    max_dq.popleft()

                left += 1

            # Calcular la longitud de la ventana.
            current_length = right - left + 1

            # En empate conservamos la primera posición.
            if current_length > best_length:
                best_length = current_length
                best_position = left + 1

        answers.append(f\"{best_length} {best_position}\")

    sys.stdout.write(\"\\n\".join(answers))


if __name__ == \"__main__\":
    solve()
```

### Ejemplo oficial 1 para probar

Entrada:

``` text
3
3 0.500000
-2.5 -2.5 2.5
7 8142465172666.218048
-512039822660.359888 -512039822660.35989 -512039822660.359889 -512039822660.359889 -512039822660.35989 -512039822660.359889 -8654504995326.577938
3 0.500000
1.500000 -1 -1.5
```

Salida esperada:

``` text
2 1
6 1
2 2
```

### Ejemplo oficial 2 para probar

Entrada:

``` text
2
5 5404369877138.611436
-5118909480930.611125 -5118909480930.611125 -5118909480930.611125 285460396208.000314 285460396208.000314
5 0.0
-7532612242812.331288 -6854978204203.068603 -2730587357333.559605 9000000000000.000000 9000000000000
```

Salida esperada:

``` text
3 1
2 4
```

## Advertencias que quedaron pendientes

La solución anterior depende de dos hipótesis que el enunciado no
confirma: 1. Una ventana es estable si `máximo - mínimo <= K`. 2. El
carácter `?` rompe la racha y no puede formar parte de ella.

El PDF dice que estas reglas deben descubrirse con el ejecutable de caja
negra. Los ejemplos publicados no incluyen sensores `?`.

Por tanto, aunque la implementación corresponde a esas hipótesis y tiene
complejidad O(N) amortizada, no se puede garantizar que pase todos los
casos ocultos sin probar la caja negra. El límite de 8 segundos también
debe medirse en el entorno del concurso, porque Python puede ser más
lento que C++.

## Última pregunta para diagnosticar el problema de ejecución

Se pidió indicar: - En qué entorno se ejecuta el código: Thonny,
PyCharm, IntelliJ IDEA, Visual Studio Code u otro. - Qué sucede al
ejecutarlo: no aparece resultado, aparece un error, se queda cargando o
no acepta los datos.

También se ofreció revisar una captura del error para identificar el
problema concreto.

------------------------------------------------------------------------

## Resumen técnico

**Hipótesis algorítmica:** ventana deslizante con máximo y mínimo.

**Estructuras:** dos `deque` monotónicas.

**Precisión:** decimales convertidos a enteros escalados por 1 000 000.

**Complejidad temporal:** O(N) amortizado por caso, O(ΣN) total.

**Complejidad espacial:** O(N) por caso.

**Pendiente imprescindible:** confirmar con la caja negra la definición
real de estabilidad y el tratamiento de `?`.
