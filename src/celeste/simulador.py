import json
import csv
from typing import List, Dict
from .vector3d import Vector3D
from .cuerpo import CuerpoCeleste

class Simulador:
    # Constante gravitatoria universal G
    # Valor aproximado para G en m^3 kg^-1 s^-2
    G = 6.67430e-11 

    def __init__(self):
        """
        Inicializa el simulador con una colección vacía de cuerpos celestes.
        """
        self.cuerpos: Dict[str, CuerpoCeleste] = {}

    def listar_cuerpos(self):
        """
        Muestra de forma enumerada todos los cuerpos registrados en el simulador.
        """
        if not self.cuerpos:
            print("No hay cuerpos celestes registrados en el simulador.")
            return

        print("\n--- Listado de Cuerpos Celestes ---")
        for i, cuerpo_id in enumerate(self.cuerpos):
            cuerpo = self.cuerpos[cuerpo_id]
            print(f"{i+1}. {cuerpo}")
        print("----------------------------------")

    def agregar_cuerpo(self, id: str, masa: float, posicion: Vector3D, velocidad: Vector3D):
        """
        Permite agregar un cuerpo celeste al simulador.
        Valida que el identificador sea único y que la masa sea positiva.
        """
        if id in self.cuerpos:
            raise ValueError(f"Ya existe un cuerpo con el identificador '{id}'.")
        
        try:
            nuevo_cuerpo = CuerpoCeleste(id, masa, posicion, velocidad)
            self.cuerpos[id] = nuevo_cuerpo
            print(f"Cuerpo '{id}' agregado exitosamente.")
        except ValueError as e:
            print(f"Error al agregar cuerpo: {e}")

    def obtener_cuerpo(self, id: str) -> CuerpoCeleste | None:
        """
        Devuelve un cuerpo celeste por su identificador, o None si no existe.
        """
        return self.cuerpos.get(id)

    def calcular_fuerzas(self):
        """
        Para cada cuerpo, calcula la fuerza neta resultante de la atracción gravitatoria
        de todos los demás cuerpos (ley de gravitación universal de Newton).
        La fuerza neta se almacena temporalmente en el atributo fuerza_neta de cada cuerpo.
        """
        for cuerpo_i in self.cuerpos.values():
            cuerpo_i.fuerza_neta = Vector3D(0.0, 0.0, 0.0) # Resetear la fuerza neta

        cuerpos_list = list(self.cuerpos.values())
        num_cuerpos = len(cuerpos_list)

        for i in range(num_cuerpos):
            for j in range(i + 1, num_cuerpos):
                cuerpo_i = cuerpos_list[i]
                cuerpo_j = cuerpos_list[j]

                # Vector distancia de i a j
                r_ij = cuerpo_j.posicion - cuerpo_i.posicion
                distancia = r_ij.magnitude()

                if distancia == 0:
                    # En un escenario real, esto podría indicar una colisión.
                    # Aquí, simplemente evitamos la división por cero.
                    continue

                # Ley de gravitación universal: F = G * (m1 * m2) / r^2 * r_hat
                # r_hat es el vector unitario en la dirección de r_ij
                # La fórmula de la ley de gravitación en el enunciado es Fᵢⱼ = G·(mᵢ·mⱼ)/rᵢⱼ³ · (rⱼ – rᵢ)
                # Esta fórmula ya incluye el vector dirección, donde (rⱼ – rᵢ) es r_ij
                # Y r_ij^3 en el denominador es para que la magnitud sea 1/r^2 y se multiplique por el vector r_ij
                
                magnitud_fuerza = (self.G * cuerpo_i.masa * cuerpo_j.masa) / (distancia**3)
                
                fuerza_ij = r_ij * magnitud_fuerza # Fuerza de i sobre j
                
                # Por la tercera ley de Newton, F_ji = -F_ij
                cuerpo_i.fuerza_neta = cuerpo_i.fuerza_neta + fuerza_ij
                cuerpo_j.fuerza_neta = cuerpo_j.fuerza_neta - fuerza_ij # Fuerza de j sobre i

    def paso_simulacion(self, dt: float, current_time: float):
        """
        Ejecuta un paso de tiempo de la simulación usando el método de Euler explícito.
        """
        self.calcular_fuerzas()

        # Actualizar velocidades y posiciones
        for cuerpo in self.cuerpos.values():
            cuerpo.aplicar_fuerza(cuerpo.fuerza_neta, dt)
            cuerpo.mover(dt)

        # Calcular y mostrar energías y momento
        energia_cinetica_total = self._calcular_energia_cinetica_total()
        energia_potencial_total = self._calcular_energia_potencial_total()
        momento_lineal_total = self._calcular_momento_lineal_total()

        print(f"\nPaso t = {current_time:.2f} s:")
        print(f"  Energía Cinética Total: {energia_cinetica_total:.6e} J")
        print(f"  Energía Potencial Total: {energia_potencial_total:.6e} J")
        print(f"  Momento Lineal Total: {momento_lineal_total} kg·m/s")

    def _calcular_energia_cinetica_total(self) -> float:
        """Calcula la energía cinética total del sistema."""
        total_energia_cinetica = 0.0
        for cuerpo in self.cuerpos.values():
            total_energia_cinetica += cuerpo.energia_cinetica()
        return total_energia_cinetica

    def _calcular_energia_potencial_total(self) -> float:
        """Calcula la energía potencial gravitatoria total del sistema."""
        total_energia_potencial = 0.0
        cuerpos_list = list(self.cuerpos.values())
        num_cuerpos = len(cuerpos_list)

        for i in range(num_cuerpos):
            for j in range(i + 1, num_cuerpos):
                cuerpo_i = cuerpos_list[i]
                cuerpo_j = cuerpos_list[j]
                total_energia_potencial += cuerpo_i.energia_potencial_con(cuerpo_j, self.G)
        return total_energia_potencial

    def _calcular_momento_lineal_total(self) -> Vector3D:
        """Calcula el momento lineal total del sistema."""
        total_momento_lineal = Vector3D(0.0, 0.0, 0.0)
        for cuerpo in self.cuerpos.values():
            momento_cuerpo = cuerpo.velocidad * cuerpo.masa
            total_momento_lineal = total_momento_lineal + momento_cuerpo
        return total_momento_lineal

    def guardar(self, archivo: str):
        """
        Guarda el estado completo del sistema en formato JSON o CSV.
        """
        if archivo.endswith('.json'):
            self._guardar_json(archivo)
        elif archivo.endswith('.csv'):
            self._guardar_csv(archivo)
        else:
            raise ValueError("Formato de archivo no soportado. Use .json o .csv")

    def _guardar_json(self, archivo: str):
        """Guarda el estado del simulador en un archivo JSON."""
        data = [cuerpo.to_dict() for cuerpo in self.cuerpos.values()]
        with open(archivo, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Estado del simulador guardado en '{archivo}' (JSON).")

    def _guardar_csv(self, archivo: str):
        """Guarda el estado del simulador en un archivo CSV."""
        with open(archivo, 'w', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            # Encabezado CSV: id;masa;pos_x;pos_y;pos_z;vel_x;vel_y;vel_z
            writer.writerow(['id', 'masa', 'pos_x', 'pos_y', 'pos_z', 'vel_x', 'vel_y', 'vel_z'])
            for cuerpo in self.cuerpos.values():
                row = [
                    cuerpo.id, cuerpo.masa,
                    cuerpo.posicion.x, cuerpo.posicion.y, cuerpo.posicion.z,
                    cuerpo.velocidad.x, cuerpo.velocidad.y, cuerpo.velocidad.z
                ]
                writer.writerow(row)
        print(f"Estado del simulador guardado en '{archivo}' (CSV).")

    def cargar(self, archivo: str):
        """
        Carga el estado completo del sistema desde un archivo JSON o CSV.
        Vacía la colección actual de cuerpos antes de cargar.
        """
        self.cuerpos.clear() # Vaciar colección antes de cargar

        if archivo.endswith('.json'):
            self._cargar_json(archivo)
        elif archivo.endswith('.csv'):
            self._cargar_csv(archivo)
        else:
            raise ValueError("Formato de archivo no soportado. Use .json o .csv")
        print(f"Estado del simulador cargado desde '{archivo}'.")

    def _cargar_json(self, archivo: str):
        """Carga el estado del simulador desde un archivo JSON."""
        with open(archivo, 'r') as f:
            data = json.load(f)
        
        for item in data:
            cuerpo = CuerpoCeleste.from_dict(item)
            self.cuerpos[cuerpo.id] = cuerpo

    def _cargar_csv(self, archivo: str):
        """Carga el estado del simulador desde un archivo CSV."""
        with open(archivo, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            header = next(reader) # Saltar el encabezado

            for row in reader:
                id_val = row[0]
                masa_val = float(row[1])
                posicion_val = Vector3D(float(row[2]), float(row[3]), float(row[4]))
                velocidad_val = Vector3D(float(row[5]), float(row[6]), float(row[7]))
                
                cuerpo = CuerpoCeleste(id_val, masa_val, posicion_val, velocidad_val)
                self.cuerpos[cuerpo.id] = cuerpo