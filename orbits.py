"""Two-body circular-orbit transfer estimates and Kepler propagation in SI units."""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt,pi,sin,cos

MU_EARTH=3.986004418e14
EARTH_RADIUS=6378137.0

@dataclass(frozen=True)
class Transfer:
    r1_m:float
    r2_m:float
    first_burn_m_s:float
    second_burn_m_s:float
    total_delta_v_m_s:float
    duration_s:float

def circular_speed(mu:float,radius:float)->float:
    if mu<=0 or radius<=0:raise ValueError('mu and radius must be positive')
    return sqrt(mu/radius)

def period(mu:float,semimajor_axis:float)->float:
    if mu<=0 or semimajor_axis<=0:raise ValueError('mu and axis must be positive')
    return 2*pi*sqrt(semimajor_axis**3/mu)

def hohmann(mu:float,r1:float,r2:float)->Transfer:
    if min(mu,r1,r2)<=0:raise ValueError('mu and radii must be positive')
    a=(r1+r2)/2
    v1,v2=circular_speed(mu,r1),circular_speed(mu,r2)
    t1=sqrt(mu*(2/r1-1/a));t2=sqrt(mu*(2/r2-1/a))
    d1=t1-v1;d2=v2-t2
    return Transfer(r1,r2,d1,d2,abs(d1)+abs(d2),pi*sqrt(a**3/mu))

def solve_kepler(mean_anomaly:float,eccentricity:float,tolerance:float=1e-12)->float:
    if not 0<=eccentricity<1:raise ValueError('Only elliptic orbits supported')
    e_anomaly=mean_anomaly if eccentricity<.8 else pi
    for _ in range(80):
        step=(e_anomaly-eccentricity*sin(e_anomaly)-mean_anomaly)/(1-eccentricity*cos(e_anomaly))
        e_anomaly-=step
        if abs(step)<tolerance:return e_anomaly
    raise ArithmeticError('Kepler solver failed to converge')

def position_2d(mu:float,a:float,e:float,time_s:float,true_anomaly_at_epoch:float=0)->tuple[float,float]:
    """Periapsis-aligned orbit, elapsed seconds since periapsis (epoch argument is mean anomaly in rad)."""
    if mu<=0 or a<=0:raise ValueError('Invalid gravitational parameter or semimajor axis')
    m=sqrt(mu/a**3)*time_s+true_anomaly_at_epoch
    E=solve_kepler(m,e)
    return a*(cos(E)-e),a*sqrt(1-e*e)*sin(E)

def sample_orbit(mu:float,a:float,e:float,n:int=180)->list[tuple[float,float]]:
    if n<3:raise ValueError('At least 3 points required')
    T=period(mu,a)
    return [position_2d(mu,a,e,T*k/n) for k in range(n+1)]
