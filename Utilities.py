import math

def Distance_Vincenty( coord1, coord2, maxIter=200, tol=10**-12 ):

        #--- CONSTANTS ------------------------------------+
        a=6378137.0                             # radius at equator in meters (WGS-84)
        f=1/298.257223563                       # flattening of the ellipsoid (WGS-84)
        b=(1-f)*a

        phi_1,L_1,=coord1                       # (lat=L_?,lon=phi_?)
        phi_2,L_2,=coord2                  
        
        #  MS:  Check for "zero" distance
        if ( abs( phi_1 - phi_2) + abs( L_1 - L_2 ) ) < 0.00001:
            return 0

        u_1=math.atan((1-f)*math.tan(math.radians(phi_1)))
        u_2=math.atan((1-f)*math.tan(math.radians(phi_2)))

        L=math.radians(L_2-L_1)

        Lambda=L                                # set initial value of lambda to L

        sin_u1=math.sin(u_1)
        cos_u1=math.cos(u_1)
        sin_u2=math.sin(u_2)
        cos_u2=math.cos(u_2)

        #--- BEGIN ITERATIONS -----------------------------+
        iters=0
        for i in range(0,maxIter):
            iters+=1
            
            cos_lambda=math.cos(Lambda)
            sin_lambda=math.sin(Lambda)
            sin_sigma=math.sqrt((cos_u2*math.sin(Lambda))**2+(cos_u1*sin_u2-sin_u1*cos_u2*cos_lambda)**2)
            cos_sigma=sin_u1*sin_u2+cos_u1*cos_u2*cos_lambda
            sigma=math.atan2(sin_sigma,cos_sigma)
            sin_alpha=(cos_u1*cos_u2*sin_lambda)/sin_sigma
            cos_sq_alpha=1-sin_alpha**2
            cos2_sigma_m=cos_sigma-((2*sin_u1*sin_u2)/cos_sq_alpha)
            C=(f/16)*cos_sq_alpha*(4+f*(4-3*cos_sq_alpha))
            Lambda_prev=Lambda
            Lambda=L+(1-C)*f*sin_alpha*(sigma+C*sin_sigma*(cos2_sigma_m+C*cos_sigma*(-1+2*cos2_sigma_m**2)))

            # successful convergence
            diff=abs(Lambda_prev-Lambda)
            if diff<=tol:
                break
            
        u_sq=cos_sq_alpha*((a**2-b**2)/b**2)
        A=1+(u_sq/16384)*(4096+u_sq*(-768+u_sq*(320-175*u_sq)))
        B=(u_sq/1024)*(256+u_sq*(-128+u_sq*(74-47*u_sq)))
        delta_sig=B*sin_sigma*(cos2_sigma_m+0.25*B*(cos_sigma*(-1+2*cos2_sigma_m**2)-(1/6)*B*cos2_sigma_m*(-3+4*sin_sigma**2)*(-3+4*cos2_sigma_m**2)))

        m=b*A*(sigma-delta_sig)                 # output distance in meters     
        #self.km=self.meters/1000                    # output distance in kilometers
        #self.mm=self.meters*1000                    # output distance in millimeters
        #self.miles=self.meters*0.000621371          # output distance in miles
        #self.n_miles=self.miles*(6080.20/5280)      # output distance in nautical miles
        #self.ft=self.miles*5280                     # output distance in feet
        #self.inches=self.feet*12                    # output distance in inches
        #self.yards=self.feet/3                      # output distance in yards
        return m
    
def Distance_GreatCircle( coord1, coord2 ):
    lon1, lat1, lon2, lat2 = map(math.radians, [coord1[1], coord1[0], coord2[1], coord2[0]])
    
    return 6371009.0 * ( math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)))

def Distance_Haversine( coord1, coord2 ):
    lon1, lat1, lon2, lat2 = map(math.radians, [coord1[1], coord1[0], coord2[1], coord2[0]])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * 6371009.0 * math.asin(math.sqrt(a))