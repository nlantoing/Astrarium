import getpass
import sys
import telnetlib
import re

HOST="horizons.jpl.nasa.gov"
PORT=6775
TIMEOUT=5

class Horizons:
    """ Interface with the telnet horizons service """
    tn = None
    host = None
    port = None
    scinote = re.compile(b"[+-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)")
    bigNumber = re.compile(b"[0-9]+\.[0-9]+")

    def __init__(self,host=HOST,port=PORT, timeout=TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
    
    def connect(self):
        """ connect to the service """
        if None == self.tn:
            try:
                self.tn = telnetlib.Telnet(self.host, self.port)
            except TimeoutError as error:
                return False

        
        return self

    def close(self):
        """ Close the current connection """
        self.tn.write("X\n".encode('ascii'))
        self.tn.close()
        self.tn = None

    def get_scivalue(self):
        """ look for the next scientific value and return it """
        result = self.tn.expect([self.scinote], self.timeout)
        final = None
        
        if(-1 == result[0]):
            raise ValueError("Can't find a proper number")

        try:
            final = float(result[1].group(0))
        except ValueError as error:
            raise ValueError("Invalid scientific number")
        
        return final

    #Removeme? should be merged with scivalue to avoid code duplicate
    def get_bigvalue(self):
        """ look for the next scientific value and return it """
        result = self.tn.expect([self.bigNumber], self.timeout)
        if(-1 == result[0]):
            raise ValueError("Can't find a proper number")
        return result[1].group(0)

    def get_barycenters(self):
        """ Return solar system barycenter list """
        self.connect()
        results = []

        self.tn.read_until(b"Horizons>", self.timeout)
        self.tn.write("barycenter\n".encode('ascii'))
        self.tn.read_until(b"---- \r\n",self.timeout)

        while True:
            newline = self.tn.read_until(b"\r\n")
            m = re.search(b'[0-9]+',newline)
            if m:
                id = int(m.group())
                m = re.search(b'[A-Za-z\-]+\ ?[A-Za-z\-]*\ ?[A-Za-z\-]*', newline)
                if m:
                    alias = m.group().decode('utf-8').strip()
                else:
                    #should raise an error instead
                    alias = "Unknown"
                results.append((id,alias))
            else:
                break
        
        self.close()
        
        return results

    def get_barycenter_members(self, barycenterId):
        """ Return the bodies list of a barycenter system """
        results = []
        query = str(barycenterId) + "*\n"
        regex = re.compile('('+str(barycenterId)+'[0-9]{2})\ *([A-Za-z0-9\-]*)')
        current = barycenterId * 100
        limit = current + 99

        #sun special case
        if(0 == current):
            results.append((10,"Sun"))
            return results

        self.connect()
        self.tn.read_until(b"Horizons>", self.timeout)
        self.tn.write(query.encode('ascii'))
        while(current != limit):
            newline = self.tn.read_until(b'\r\n', self.timeout)
            m = re.search(regex,str(newline))
            if m:
                current = int(m.group(1))
                alias = m.group(2).strip()
                results.append((current,alias))
        
        return results
    
    def get_orbit(self, body, reference):
        """ get a major body orbit details """
        self.connect()

        results = {}

        #set request
        self.tn.read_until(b"Horizons>", self.timeout)
        self.tn.write((str(body) + "\n").encode('ascii'))
        self.tn.read_until(b"<cr>:", self.timeout)
        self.tn.write("E\n".encode('ascii'))
        self.tn.read_until(b"[o,e,v,?]", self.timeout)
        self.tn.write("e\n".encode('ascii'))
        self.tn.read_some()
        self.tn.write((str(reference)+"\n").encode('ascii'))
        self.tn.read_some()
        self.tn.write("eclip\n".encode('ascii'))
        self.tn.read_some()
        self.tn.write("2000-Jan-01\n".encode('ascii'))
        self.tn.read_some()
        self.tn.write("2000-Jan-01 01:00\n".encode('ascii'))
        self.tn.read_some()
        self.tn.write("1d\n".encode('ascii'))
        self.tn.read_until(b"[ cr=(y), n, ?]")
        self.tn.write("y\n".encode('ascii'))

        #parse results
        self.tn.read_until(b"EC= ")
        results['eccentricity'] = self.get_scivalue()
        results['periapsis_distance'] = self.get_scivalue()
        results['inclination'] = self.get_scivalue()
        results['long_of_asc_node'] = self.get_scivalue()
        results['arg_of_periapsis'] = self.get_scivalue()
        results['time_of_periapsis'] = self.get_bigvalue()
        results['mean_motion'] = self.get_scivalue()
        results['mean_anomaly'] = self.get_scivalue()
        results['true_anomaly'] = self.get_scivalue()
        results['semi_major_axis'] = self.get_scivalue()
        results['apoapsis_dist'] = self.get_scivalue()
        results['orbital_period'] = self.get_scivalue()
        
        self.close()
        return results
