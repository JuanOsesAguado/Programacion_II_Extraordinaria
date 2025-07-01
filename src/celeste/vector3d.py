import math

class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        """
        Inicializa un nuevo Vector3D.
        """
        self.x = x
        self.y = y
        self.z = z

    def add(self, other: 'Vector3D') -> 'Vector3D':
        """
        Suma este vector con otro vector.
        """
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        """
        Sobrecarga del operador + para la suma de vectores.
        """
        return self.add(other)

    def sub(self, other: 'Vector3D') -> 'Vector3D':
        """
        Resta otro vector de este vector.
        """
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        """
        Sobrecarga del operador - para la resta de vectores.
        """
        return self.sub(other)

    def mul(self, scalar: float) -> 'Vector3D':
        """
        Multiplica este vector por un escalar.
        """
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __mul__(self, scalar: float) -> 'Vector3D':
        """
        Sobrecarga del operador * para la multiplicación por un escalar.
        """
        return self.mul(scalar)

    def __rmul__(self, scalar: float) -> 'Vector3D':
        """
        Sobrecarga del operador * para la multiplicación por un escalar (cuando el escalar está a la izquierda).
        """
        return self.mul(scalar)

    def div(self, scalar: float) -> 'Vector3D':
        """
        Divide este vector por un escalar.
        """
        if scalar == 0:
            raise ValueError("No se puede dividir por cero.")
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)

    def __truediv__(self, scalar: float) -> 'Vector3D':
        """
        Sobrecarga del operador / para la división por un escalar.
        """
        return self.div(scalar)

    def magnitude(self) -> float:
        """
        Calcula la magnitud (longitud) del vector.
        """
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalized(self) -> 'Vector3D':
        """
        Devuelve un vector normalizado (magnitud 1).
        """
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0.0, 0.0, 0.0) # O levantar un error, según la política deseada
        return self / mag

    def dot(self, other: 'Vector3D') -> float:
        """
        Calcula el producto punto con otro vector.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __str__(self) -> str:
        """
        Representación legible del vector para el usuario.
        """
        return f"({self.x:.6f}, {self.y:.6f}, {self.z:.6f})"

    def __repr__(self) -> str:
        """
        Representación oficial del vector para desarrolladores.
        """
        return f"Vector3D(x={self.x}, y={self.y}, z={self.z})"

    def __eq__(self, other: object) -> bool:
        """
        Define la igualdad entre dos objetos Vector3D.
        """
        if not isinstance(other, Vector3D):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def to_list(self) -> list:
        """Convierte el vector a una lista [x, y, z]."""
        return [self.x, self.y, self.z]

    @staticmethod
    def from_list(data: list) -> 'Vector3D':
        """Crea un Vector3D desde una lista [x, y, z]."""
        if len(data) != 3:
            raise ValueError("La lista debe contener 3 elementos para un Vector3D.")
        return Vector3D(data[0], data[1], data[2])