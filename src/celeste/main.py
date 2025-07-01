from .simulador import Simulador
from .vector3d import Vector3D
import sys

def run_simulation(sim: Simulador, dt: float, total_time: float):
    """
    Ejecuta la simulación por un tiempo total dado.
    """
    print(f"\n--- Iniciando Simulación (dt={dt}s, tiempo total={total_time}s) ---")
    current_time = 0.0
    step = 0
    while current_time < total_time:
        print(f"\n--- Paso de Simulación {step + 1} ---")
        sim.paso_simulacion(dt, current_time)
        current_time += dt
        step += 1
        # Opcional: pausar la simulación o mostrar solo cada N pasos
        # if step % 10 == 0:
        #     sim.listar_cuerpos()
    print("\n--- Simulación Finalizada ---")
    sim.listar_cuerpos()


def main():
    simulador = Simulador()

    while True:
        print("\n--- Menú del Simulador Planetario ---")
        print("1. Listar cuerpos celestes")
        print("2. Agregar nuevo cuerpo celeste")
        print("3. Ejecutar simulación")
        print("4. Guardar estado del simulador")
        print("5. Cargar estado del simulador")
        print("6. Salir")
        print("-----------------------------------")

        choice = input("Seleccione una opción: ")

        if choice == '1':
            simulador.listar_cuerpos()
        elif choice == '2':
            try:
                cel_id = input("Ingrese el ID del cuerpo: ")
                masa = float(input("Ingrese la masa (kg): "))
                pos_x = float(input("Ingrese la posición X (m): "))
                pos_y = float(input("Ingrese la posición Y (m): "))
                pos_z = float(input("Ingrese la posición Z (m): "))
                vel_x = float(input("Ingrese la velocidad X (m/s): "))
                vel_y = float(input("Ingrese la velocidad Y (m/s): "))
                vel_z = float(input("Ingrese la velocidad Z (m/s): "))

                posicion = Vector3D(pos_x, pos_y, pos_z)
                velocidad = Vector3D(vel_x, vel_y, vel_z)
                simulador.agregar_cuerpo(cel_id, masa, posicion, velocidad)
            except ValueError as e:
                print(f"Error en la entrada: {e}. Asegúrese de ingresar números válidos.")
        elif choice == '3':
            if not simulador.cuerpos:
                print("No hay cuerpos para simular. Agregue algunos primero.")
                continue
            try:
                dt = float(input("Ingrese el paso de tiempo (dt en segundos): "))
                total_time = float(input("Ingrese el tiempo total de simulación (en segundos): "))
                if dt <= 0 or total_time <= 0:
                    print("El paso de tiempo y el tiempo total deben ser positivos.")
                    continue
                run_simulation(simulador, dt, total_time)
            except ValueError:
                print("Entrada inválida. Asegúrese de ingresar números para dt y tiempo total.")
        elif choice == '4':
            filename = input("Ingrese el nombre del archivo para guardar (ej: sistema.json o sistema.csv): ")
            try:
                simulador.guardar(filename)
            except ValueError as e:
                print(f"Error al guardar: {e}")
            except Exception as e:
                print(f"Ocurrió un error inesperado al guardar: {e}")
        elif choice == '5':
            filename = input("Ingrese el nombre del archivo para cargar (ej: sistema.json o sistema.csv): ")
            try:
                simulador.cargar(filename)
            except FileNotFoundError:
                print(f"Error: El archivo '{filename}' no se encontró.")
            except (ValueError, json.JSONDecodeError, csv.Error) as e:
                print(f"Error al cargar el archivo: {e}. Verifique el formato.")
            except Exception as e:
                print(f"Ocurrió un error inesperado al cargar: {e}")
        elif choice == '6':
            print("Saliendo del simulador. ¡Hasta luego!")
            sys.exit(0)
        else:
            print("Opción inválida. Por favor, intente de nuevo.")

if __name__ == '__main__':
    main()