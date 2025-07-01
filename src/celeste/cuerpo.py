from .vector3d import Vector3D

class CuerpoCeleste:
    def __init__(self, id: str, masa: float, posicion: Vector3D, velocidad: Vector3D):
        """
        Inicializa un nuevo CuerpoCeleste.
        """
        if masa <= 0:
            raise ValueError("La masa debe ser un valor positivo.")
        self.id = id
        self.masa = masa
        self.posicion = posicion
        self.velocidad = velocidad
        self.fuerza_neta = Vector3D(0.0, 0.0, 0.0) # Para acumular fuerzas en cada paso

    def aplicar_fuerza(self, fuerza: Vector3D, dt: float):
        """
        Actualiza la velocidad del cuerpo basándose en una fuerza aplicada y un paso de tiempo.
        v_nueva = v_actual + (F/m) * dt
        """
        aceleracion = fuerza / self.masa
        self.velocidad = self.velocidad + aceleracion * dt

    def mover(self, dt: float):
        """
        Actualiza la posición del cuerpo basándose en su velocidad y un paso de tiempo.
        r_nueva = r_actual + v * dt
        """
        self.posicion = self.posicion + self.velocidad * dt

    def energia_cinetica(self) -> float:
        """
        Calcula la energía cinética del cuerpo. K = 0.5 * m * ||v||^2
        """
        return 0.5 * self.masa * (self.velocidad.magnitude()**2)

    def energia_potencial_con(self, otro: 'CuerpoCeleste', G: float) -> float:
        """
        Calcula la energía potencial gravitatoria entre este cuerpo y otro.
        U = -G * (m1 * m2) / ||r1 - r2||
        """
        if self.id == otro.id:
            return 0.0 # No hay energía potencial consigo mismo

        distancia_vector = self.posicion - otro.posicion
        distancia = distancia_vector.magnitude()

        if distancia == 0:
            # Evitar división por cero si los cuerpos están en la misma posición.
            # En un simulador real, esto indicaría una colisión o un estado no físico.
            return float('-inf')
        
        return -G * (self.masa * otro.masa) / distancia

    def __str__(self) -> str:
        """
        Representación legible del cuerpo celeste.
        """
        return (f"ID: {self.id}, Masa: {self.masa:.2e} kg, "
                f"Posición: {self.posicion}, Velocidad: {self.velocidad} m/s")

    def __repr__(self) -> str:
        """
        Representación oficial del cuerpo celeste.
        """
        return (f"CuerpoCeleste(id='{self.id}', masa={self.masa}, "
                f"posicion={repr(self.posicion)}, velocidad={repr(self.velocidad)})")

    def to_dict(self) -> dict:
        """Convierte el cuerpo celeste a un diccionario para persistencia."""
        return {
            "id": self.id,
            "masa": self.masa,
            "posicion": self.posicion.to_list(),
            "velocidad": self.velocidad.to_list()
        }

    @staticmethod
    def from_dict(data: dict) -> 'CuerpoCeleste':
        """Crea un CuerpoCeleste desde un diccionario."""
        return CuerpoCeleste(
            id=data["id"],
            masa=data["masa"],
            posicion=Vector3D.from_list(data["posicion"]),
            velocidad=Vector3D.from_list(data["velocidad"])
        )