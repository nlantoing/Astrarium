from horizons import Horizons

hztn = Horizons()

def test_connect():
    """ Test connection to the JPL telnet service """
    assert None == hztn.tn
    hztn.connect()
    assert None != hztn.tn

def test_bodies_list():
    """ Test the get bodies and JPL ID lists methods  """
    barycenters = hztn.get_barycenters()
    print(barycenters)
    assert barycenters[3][0] == 3
    assert barycenters[2][1] == 'Venus Barycenter'
    assert 10 == len(barycenters)
    neptune = barycenters[8]
    neptune_system = hztn.get_barycenter_members(neptune[0])
    print(neptune_system)
    assert None != neptune_system
    assert neptune_system[len(neptune_system) - 1][0] == 899
    
def test_essential_orbit():
    """ Test retrieving essential orbit data """
    mars = 499
    mars_system = 10
    neptune = 899
    neptune_system = 8
    result = hztn.get_orbit(mars,mars_system)
    assert result['orbital_period'] == 686.9707263001874
    print(result)
    result = hztn.get_orbit(neptune,neptune_system)
    print(result)
    assert result['eccentricity'] ==  0.004492338553255954
