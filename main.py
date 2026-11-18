import argparse,json
from orbits import EARTH_RADIUS,MU_EARTH,hohmann,sample_orbit,period

def main():
    p=argparse.ArgumentParser(description='Hohmann orbit-transfer mission planner')
    p.add_argument('--from-km',type=float,default=400,help='Initial altitude above Earth (km)')
    p.add_argument('--to-km',type=float,default=35786,help='Final altitude above Earth (km)')
    p.add_argument('--json',action='store_true')
    p.add_argument('--plot',action='store_true',help='Save standalone interactive orbit diagram as HTML')
    args=p.parse_args()
    if min(args.from_km,args.to_km)<0:p.error('Altitudes cannot be negative')
    r1=EARTH_RADIUS+args.from_km*1000;r2=EARTH_RADIUS+args.to_km*1000
    transfer=hohmann(MU_EARTH,r1,r2)
    summary={'initial_altitude_km':args.from_km,'target_altitude_km':args.to_km,'first_burn_m_s':round(transfer.first_burn_m_s,2),'second_burn_m_s':round(transfer.second_burn_m_s,2),'total_delta_v_m_s':round(transfer.total_delta_v_m_s,2),'transfer_time_hours':round(transfer.duration_s/3600,2),'target_orbital_period_hours':round(period(MU_EARTH,r2)/3600,2)}
    print(json.dumps(summary,indent=2) if args.json else '\n'.join(f'{k}: {v}' for k,v in summary.items()))
    if args.plot:
        import pathlib
        points=sample_orbit(MU_EARTH,(r1+r2)/2,abs(r2-r1)/(r1+r2))
        coords=[(round(x/1000,1),round(y/1000,1)) for x,y in points]
        html='''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Orbit transfer</title><style>body{font:16px system-ui;background:#080f20;color:white;text-align:center}canvas{width:min(90vw,900px);background:#121e36;border-radius:12px}</style></head><body><h1>Hohmann transfer orbit</h1><p>Two-body illustrative transfer path, kilometers</p><canvas id="c" width="900" height="700"></canvas><script>const points=__POINTS__;const c=document.getElementById('c').getContext('2d');const max=Math.max(...points.map(p=>Math.hypot(...p)));const scale=310/max;c.translate(450,350);c.strokeStyle='#53b5f8';c.lineWidth=3;c.beginPath();points.forEach((p,i)=>i?c.lineTo(p[0]*scale,-p[1]*scale):c.moveTo(p[0]*scale,-p[1]*scale));c.stroke();c.fillStyle='#4f9eea';c.beginPath();c.arc(0,0,__ER__*scale,0,2*Math.PI);c.fill();</script></body></html>'''.replace('__POINTS__',json.dumps(coords)).replace('__ER__',str(EARTH_RADIUS/1000))
        pathlib.Path('transfer.html').write_text(html,encoding='utf-8');print('Wrote transfer.html')
if __name__=='__main__':main()
