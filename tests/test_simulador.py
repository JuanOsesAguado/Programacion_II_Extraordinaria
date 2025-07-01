import pytest
from src.celeste.simulador import Simulador
from src.celeste.vector3d import Vector3D
from src.celeste.cuerpo import CuerpoCeleste
import os

# Constante G para las pruebas
G_TEST = 6.67430e-11 

@pytest.fixture
def simulador_vacio():
    return Simulador()

@pytest.fixture
def simulador_con_cuerpos():
    sim = Simulador()
    sim.agregar_cuerpo("Tierra", 5.972e24, Vector3D(0,0,0), Vector3D(0,0,0))
    sim.agregar_cuerpo("Luna", 7.348e22, Vector3D(3.844e8,0,0), Vector3D(0,1.022e3,0))
    return sim

def test_simulador_agregar_cuerpo(simulador_vacio):
    sim = simulador_vacio
    pos = Vector3D(0,0,0)
    vel = Vector3D(0,0,0)
    sim.agregar_cuerpo("Sol", 1.989e30, pos, vel)
    assert "Sol" in sim.cuerpos
    assert sim.cuerpos["Sol"].masa == 1.989e30

def test_simulador_agregar_cuerpo_duplicado(simulador_vacio):
    sim = simulador_vacio
    pos = Vector3D(0,0,0)
    vel = Vector3D(0,0,0)
    sim.agregar_cuerpo("Duplicado", 1.0, pos, vel)
    with pytest.raises(ValueError, match="Ya existe un cuerpo con el identificador 'Duplicado'."):
        sim.agregar_cuerpo("Duplicado", 2.0, pos, vel)

def test_simulador_listar_cuerpos(capsys, simulador_con_cuerpos):
    simulador_con_cuerpos.listar_cuerpos()
    captured = capsys.readouterr()
    assert "Tierra" in captured.out
    assert "Luna" in captured.out
    assert "Listado de Cuerpos Celestes" in captured.out

def test_simulador_calcular_fuerzas_dos_cuerpos():
    sim = Simulador()
    sim.G = G_TEST # Usar la constante de prueba
    tierra = CuerpoCeleste("Tierra", 5.972e24, Vector3D(0,0,0), Vector3D(0,0,0))
    luna = CuerpoCeleste("Luna", 7.348e22, Vector3D(3.844e8,0,0), Vector3D(0,0,0))
    sim.cuerpos["Tierra"] = tierra
    sim.cuerpos["Luna"] = luna

    sim.calcular_fuerzas()

    # Distancia entre Tierra y Luna
    r = Vector3D(3.844e8,0,0)
    distancia = r.magnitude()

    # Fuerza esperada magnitud F = G * m_tierra * m_luna / r^2
    F_magnitud_esperada = sim.G * tierra.masa * luna.masa / (distancia**2)

    # Fuerza sobre la Luna (dirigida hacia la Tierra)
    # Fuerza sobre la Tierra (dirigida hacia la Luna)
    
    # La fuerza debe ser en la dirección de X para la Luna (hacia el origen)
    # y en la dirección de -X para la Tierra (hacia la Luna)
    
    # Tolerancia para comparaciones de flotantes
    tol = 1e-5
    
    # La fuerza sobre la Luna debe ser en la dirección de (-1, 0, 0)
    # r_luna - r_tierra = (3.844e8, 0, 0) - (0,0,0) = (3.844e8, 0, 0)
    # Fuerza sobre Tierra (i) de Luna (j) -> F_ij = G * mi*mj / |rij|^3 * (rj - ri)
    # F_tierra_luna = G * m_tierra * m_luna / distancia^3 * (pos_luna - pos_tierra)
    fuerza_tierra_esperada = r.normalized() * F_magnitud_esperada
    assert abs(tierra.fuerza_neta.x - fuerza_tierra_esperada.x) < tol * abs(fuerza_tierra_esperada.x)
    assert abs(tierra.fuerza_neta.y - fuerza_tierra_esperada.y) < tol * abs(fuerza_tierra_esperada.y)
    assert abs(tierra.fuerza_neta.z - fuerza_tierra_esperada.z) < tol * abs(fuerza_tierra_esperada.z)

    # Fuerza sobre Luna (j) de Tierra (i) -> F_ji = G * mj*mi / |rji|^3 * (ri - rj)
    # F_luna_tierra = G * m_luna * m_tierra / distancia^3 * (pos_tierra - pos_luna)
    fuerza_luna_esperada = -r.normalized() * F_magnitud_esperada
    assert abs(luna.fuerza_neta.x - fuerza_luna_esperada.x) < tol * abs(fuerza_luna_esperada.x)
    assert abs(luna.fuerza_neta.y - fuerza_luna_esperada.y) < tol * abs(fuerza_luna_esperada.y)
    assert abs(luna.fuerza_neta.z - fuerza_luna_esperada.z) < tol * abs(fuerza_luna_esperada.z)

def test_simulador_paso_simulacion(capsys, simulador_con_cuerpos):
    sim = simulador_con_cuerpos
    initial_time = 0.0
    dt = 100.0 # Un dt pequeño para no cambiar demasiado las posiciones
    
    tierra_inicial_pos = sim.cuerpos["Tierra"].posicion
    luna_inicial_pos = sim.cuerpos["Luna"].posicion

    sim.paso_simulacion(dt, initial_time)
    captured = capsys.readouterr()

    assert "Paso t = 0.00 s:" in captured.out
    assert "Energía Cinética Total:" in captured.out
    assert "Energía Potencial Total:" in captured.out
    assert "Momento Lineal Total:" in captured.out

    # Las posiciones y velocidades deberían haber cambiado (excepto si son 0 y no hay fuerzas)
    # La Tierra y la Luna sí tienen fuerzas, así que sus posiciones y velocidades deberían actualizarse.
    assert sim.cuerpos["Tierra"].posicion != tierra_inicial_pos
    assert sim.cuerpos["Luna"].posicion != luna_inicial_pos
    assert sim.cuerpos["Tierra"].velocidad != Vector3D(0,0,0) # La Tierra inicialmente no se mueve, pero la Luna la atrae

def test_simulador_guardar_cargar_json(simulador_con_cuerpos, tmp_path):
    sim = simulador_con_cuerpos
    file_path = tmp_path / "test_sim.json"
    sim.guardar(str(file_path))
    assert os.path.exists(file_path)

    new_sim = Simulador()
    new_sim.cargar(str(file_path))

    assert len(new_sim.cuerpos) == len(sim.cuerpos)
    assert "Tierra" in new_sim.cuerpos
    assert new_sim.cuerpos["Tierra"].masa == sim.cuerpos["Tierra"].masa
    assert new_sim.cuerpos["Tierra"].posicion == sim.cuerpos["Tierra"].posicion
    assert new_sim.cuerpos["Tierra"].velocidad == sim.cuerpos["Tierra"].velocidad

    # Asegurarse de que el simulador se vacíe antes de cargar
    sim.agregar_cuerpo("NuevoCuerpo", 1.0, Vector3D(1,1,1), Vector3D(1,1,1))
    assert len(sim.cuerpos) == 3
    sim.cargar(str(file_path))
    assert len(sim.cuerpos) == 2 # Debe volver a ser 2 después de cargar el archivo original

def test_simulador_guardar_cargar_csv(simulador_con_cuerpos, tmp_path):
    sim = simulador_con_cuerpos
    file_path = tmp_path / "test_sim.csv"
    sim.guardar(str(file_path))
    assert os.path.exists(file_path)

    new_sim = Simulador()
    new_sim.cargar(str(file_path))

    assert len(new_sim.cuerpos) == len(sim.cuerpos)
    assert "Tierra" in new_sim.cuerpos
    assert new_sim.cuerpos["Tierra"].masa == sim.cuerpos["Tierra"].masa
    assert new_sim.cuerpos["Tierra"].posicion == sim.cuerpos["Tierra"].posicion
    assert new_sim.cuerpos["Tierra"].velocidad == sim.cuerpos["Tierra"].velocidad

def test_simulador_guardar_cargar_unsupported_format(simulador_vacio, tmp_path):
    sim = simulador_vacio
    file_path = tmp_path / "test_sim.txt"
    with pytest.raises(ValueError, match="Formato de archivo no soportado. Use .json o .csv"):
        sim.guardar(str(file_path))
    with pytest.raises(ValueError, match="Formato de archivo no soportado. Use .json o .csv"):
        sim.cargar(str(file_path))