import pytest
from src.celeste.vector3d import Vector3D
from src.celeste.cuerpo import CuerpoCeleste

def test_cuerpo_celeste_init():
    pos = Vector3D(0, 0, 0)
    vel = Vector3D(0, 0, 0)
    cuerpo = CuerpoCeleste("Tierra", 5.972e24, pos, vel)
    assert cuerpo.id == "Tierra"
    assert cuerpo.masa == 5.972e24
    assert cuerpo.posicion == pos
    assert cuerpo.velocidad == vel
    assert cuerpo.fuerza_neta == Vector3D(0.0, 0.0, 0.0)

def test_cuerpo_celeste_init_invalid_masa():
    pos = Vector3D(0, 0, 0)
    vel = Vector3D(0, 0, 0)
    with pytest.raises(ValueError, match="La masa debe ser un valor positivo."):
        CuerpoCeleste("Invalido", 0, pos, vel)
    with pytest.raises(ValueError, match="La masa debe ser un valor positivo."):
        CuerpoCeleste("Invalido", -10, pos, vel)

def test_cuerpo_celeste_aplicar_fuerza():
    cuerpo = CuerpoCeleste("Test", 1.0, Vector3D(0,0,0), Vector3D(0,0,0))
    fuerza = Vector3D(10.0, 0.0, 0.0)
    dt = 1.0
    cuerpo.aplicar_fuerza(fuerza, dt)
    # a = F/m = 10/1 = 10
    # v_nueva = v_actual + a * dt = 0 + 10 * 1 = 10
    assert cuerpo.velocidad == Vector3D(10.0, 0.0, 0.0)

    fuerza_y = Vector3D(0.0, 5.0, 0.0)
    cuerpo.aplicar_fuerza(fuerza_y, dt)
    assert cuerpo.velocidad == Vector3D(10.0, 5.0, 0.0) # Acumula

def test_cuerpo_celeste_mover():
    cuerpo = CuerpoCeleste("Test", 1.0, Vector3D(0,0,0), Vector3D(1.0, 2.0, 3.0))
    dt = 1.0
    cuerpo.mover(dt)
    # r_nueva = r_actual + v * dt = (0,0,0) + (1,2,3) * 1 = (1,2,3)
    assert cuerpo.posicion == Vector3D(1.0, 2.0, 3.0)

    dt_half = 0.5
    cuerpo.mover(dt_half)
    # r_nueva = (1,2,3) + (1,2,3) * 0.5 = (1,2,3) + (0.5, 1, 1.5) = (1.5, 3, 4.5)
    assert cuerpo.posicion == Vector3D(1.5, 3.0, 4.5)

def test_cuerpo_celeste_energia_cinetica():
    cuerpo = CuerpoCeleste("Test", 2.0, Vector3D(0,0,0), Vector3D(3.0, 4.0, 0.0))
    # v.magnitude() = sqrt(3^2 + 4^2) = 5
    # K = 0.5 * m * ||v||^2 = 0.5 * 2.0 * 5.0^2 = 1.0 * 25.0 = 25.0
    assert cuerpo.energia_cinetica() == 25.0

    cuerpo_estatico = CuerpoCeleste("Estático", 10.0, Vector3D(0,0,0), Vector3D(0,0,0))
    assert cuerpo_estatico.energia_cinetica() == 0.0

def test_cuerpo_celeste_energia_potencial_con():
    G = 6.67430e-11 # Constante G para pruebas

    cuerpo1 = CuerpoCeleste("C1", 1.0, Vector3D(0,0,0), Vector3D(0,0,0))
    cuerpo2 = CuerpoCeleste("C2", 1.0, Vector3D(1,0,0), Vector3D(0,0,0))
    # Distancia = 1
    # U = -G * (m1 * m2) / r = -G * (1 * 1) / 1 = -G
    assert cuerpo1.energia_potencial_con(cuerpo2, G) == -G
    assert cuerpo2.energia_potencial_con(cuerpo1, G) == -G # Simétrico

    cuerpo3 = CuerpoCeleste("C3", 2.0, Vector3D(3,0,0), Vector3D(0,0,0))
    # Distancia entre cuerpo1 y cuerpo3 = 3
    # U = -G * (1 * 2) / 3 = -2G/3
    assert cuerpo1.energia_potencial_con(cuerpo3, G) == -G * (1.0 * 2.0) / 3.0

    # Misma posición (debería ser infinito negativo o manejarlo como colisión)
    cuerpo_colision = CuerpoCeleste("C4", 1.0, Vector3D(0,0,0), Vector3D(0,0,0))
    assert cuerpo1.energia_potencial_con(cuerpo_colision, G) == float('-inf')

    # Consigo mismo
    assert cuerpo1.energia_potencial_con(cuerpo1, G) == 0.0

def test_cuerpo_celeste_str_repr():
    pos = Vector3D(1.0, 2.0, 3.0)
    vel = Vector3D(4.0, 5.0, 6.0)
    cuerpo = CuerpoCeleste("Marte", 6.39e23, pos, vel)
    assert "ID: Marte" in str(cuerpo)
    assert "Masa: 6.39e+23 kg" in str(cuerpo)
    assert "Posición: (1.000000, 2.000000, 3.000000)" in str(cuerpo)
    assert "Velocidad: (4.000000, 5.000000, 6.000000) m/s" in str(cuerpo)
    
    # Repr debería ser más detallado para reconstrucción
    assert repr(cuerpo) == "CuerpoCeleste(id='Marte', masa=6.39e+23, posicion=Vector3D(x=1.0, y=2.0, z=3.0), velocidad=Vector3D(x=4.0, y=5.0, z=6.0))"
