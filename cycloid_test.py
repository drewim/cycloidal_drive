from cycloid_design import Cycloid, Plotter
import pytest

        
def test_num_rollers_and_dependency_changes():
    cycloid = Cycloid()
    cycloid.set_num_rollers = 8
    assert cycloid.get_num_rollers == 8
    assert cycloid.get_num_rotors == 7
    assert cycloid.get_gear_ratio == 7
    
def test_num_rollers_invalid_input():
    cycloid = Cycloid()
    with pytest.raises(ValueError):
        cycloid.set_num_rollers = 1
        
def test_num_rotors_and_dependency_changes():
    cycloid = Cycloid()
    cycloid.set_num_rotors = 6
    assert cycloid.get_num_rotors == 6
    assert cycloid.get_num_rollers == 7
    assert cycloid.get_gear_ratio == 6

def test_num_rotors_invalid_input():
    cycloid = Cycloid()
    with pytest.raises(ValueError):
        cycloid.set_num_rotors = 1
        
def test_eccentricity_invalid_input():
    # eccentricity must be greater than 0 and less than 
    # radius_pin_circle / num_rollers
    cycloid = Cycloid()
    cycloid.set_radius_pin_circle = 9
    cycloid.set_num_rollers = 3
    with pytest.raises(ValueError):
        cycloid.set_eccentricity = 5
        
# TODO: ADD more tests to fully test class

 
