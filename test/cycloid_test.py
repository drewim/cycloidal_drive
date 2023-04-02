from scripts.cycloid_design import CycloidGeometry
import pytest
  
def test_num_rollers_and_dependency_changes():
    cycloid = CycloidGeometry()
    cycloid.set_num_rollers = 8
    assert cycloid.get_num_rollers == 8
    assert cycloid.get_num_rotors == 7
    assert cycloid.get_gear_ratio == 7
    
def test_num_rollers_invalid_input():
    cycloid = CycloidGeometry()
    with pytest.raises(ValueError):
        cycloid.set_num_rollers = 1
        
def test_num_rotors_and_dependency_changes():
    cycloid = CycloidGeometry()
    cycloid.set_num_rotors = 6
    assert cycloid.get_num_rotors == 6
    assert cycloid.get_num_rollers == 7
    assert cycloid.get_gear_ratio == 6

def test_num_rotors_invalid_input():
    cycloid = CycloidGeometry()
    with pytest.raises(ValueError):
        cycloid.set_num_rotors = 1
        
def test_eccentricity_invalid_input():
    # eccentricity must be greater than 0 and less than 
    # radius_pin_circle / num_rollers
    cycloid = CycloidGeometry()
    cycloid.set_radius_pin_circle = 9
    cycloid.set_num_rollers = 3
    with pytest.raises(ValueError):
        cycloid.set_eccentricity = 5

def test_radius_output_shaft_pins_invalid_input():
    cycloid = CycloidGeometry()
    with pytest.raises(ValueError):
        cycloid.set_radius_output_shaft_pins = 0.5

def test_radius_output_shaft_pins_validity():
    cycloid = CycloidGeometry()
    cycloid.set_radius_output_shaft_pins = 2
    assert cycloid.get_radius_output_shaft_pins == 2
    # assert cycloid.get_base_hole_diam == 

def test_radius_output_shaft_circle_invalid_input():
    cycloid = CycloidGeometry()
    with pytest.raises(ValueError):
        cycloid.set_radius_output_shaft_circle = 4

def test_radius_output_shaft_circle_validity():
    cycloid = CycloidGeometry
    cycloid.set_radius_output_shaft_circle = 6
    assert cycloid.get_radius_output_shaft_circle == 6

def test_num_output_shaft_invalid_input():
    cycloid = CycloidGeometry()
    with pytest.raises(ValueError):
        cycloid.set_num_output_shafts = 1

def test_num_output_shaft_validity():
    cycloid = CycloidGeometry
    cycloid.set_num_output_shafts = 6
    assert cycloid.get_num_output_shafts == 6

        
# TODO: ADD more tests to fully test class

 
