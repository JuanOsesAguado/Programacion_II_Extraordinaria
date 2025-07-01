import pytest
from src.celeste.vector3d import Vector3D

def test_vector3d_init():
    v = Vector3D(1.0, 2.0, 3.0)
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.z == 3.0

def test_vector3d_add():
    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(4, 5, 6)
    v_sum = v1 + v2
    assert v_sum.x == 5
    assert v_sum.y == 7
    assert v_sum.z == 9

def test_vector3d_sub():
    v1 = Vector3D(5, 5, 5)
    v2 = Vector3D(1, 2, 3)
    v_sub = v1 - v2
    assert v_sub.x == 4
    assert v_sub.y == 3
    assert v_sub.z == 2

def test_vector3d_mul_scalar():
    v = Vector3D(1, 2, 3)
    v_mul = v * 2
    assert v_mul.x == 2
    assert v_mul.y == 4
    assert v_mul.z == 6

    v_rmul = 3 * v
    assert v_rmul.x == 3
    assert v_rmul.y == 6
    assert v_rmul.z == 9

def test_vector3d_div_scalar():
    v = Vector3D(6, 4, 2)
    v_div = v / 2
    assert v_div.x == 3
    assert v_div.y == 2
    assert v_div.z == 1

    with pytest.raises(ValueError, match="No se puede dividir por cero."):
        v / 0

def test_vector3d_magnitude():
    v = Vector3D(3, 4, 0)
    assert v.magnitude() == 5.0
    v_zero = Vector3D(0, 0, 0)
    assert v_zero.magnitude() == 0.0
    v_neg = Vector3D(-3, -4, 0)
    assert v_neg.magnitude() == 5.0

def test_vector3d_str_repr():
    v = Vector3D(1.234567, 2.345678, 3.456789)
    assert str(v) == "(1.234567, 2.345678, 3.456789)"
    assert repr(v) == "Vector3D(x=1.234567, y=2.345678, z=3.456789)"

def test_vector3d_equality():
    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(1, 2, 3)
    v3 = Vector3D(4, 5, 6)
    assert v1 == v2
    assert v1 != v3
    assert v1 != "not_a_vector"

def test_vector3d_normalized():
    v = Vector3D(3, 4, 0)
    v_norm = v.normalized()
    assert v_norm.x == 0.6
    assert v_norm.y == 0.8
    assert v_norm.z == 0.0
    assert abs(v_norm.magnitude() - 1.0) < 1e-9

    v_zero = Vector3D(0, 0, 0)
    v_zero_norm = v_zero.normalized()
    assert v_zero_norm == Vector3D(0, 0, 0)

def test_vector3d_dot_product():
    v1 = Vector3D(1, 2, 3)
    v2 = Vector3D(4, 5, 6)
    assert v1.dot(v2) == (1*4 + 2*5 + 3*6) # 4 + 10 + 18 = 32