import pygeoip


def dados_ip(ip):
    city = pygeoip.GeoIP('projeto/geo_location/GeoIPCity.dat')
    emp = pygeoip.GeoIP('projeto/geo_location/GeoIPOrg.dat') 
    

    ip_sem_porta = ip.split(':')[0]
    empresa = emp.org_by_addr(ip_sem_porta)
    endereco = city.record_by_addr(ip_sem_porta)
    #print(endereco['country_name'])
    #print(endereco['region_code'])
    #print(endereco['city'])
    #print(endereco['latitude'])
    #print(endereco['longitude'])
    return endereco, empresa


    