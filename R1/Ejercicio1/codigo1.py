
import sys
from collections import deque
from array import array

SCALE = 1_000_000


def to_scaled_int(s):
    """Convierte un decimal de hasta 6 posiciones a entero exacto."""

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

        answers.append(f"{best_length} {best_position}")

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()
