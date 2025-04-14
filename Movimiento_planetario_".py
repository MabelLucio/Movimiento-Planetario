import math as mt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#variables de la tierra
xit = 1; yit = 0; vxit = 0; vyit = 2*np.pi;rt = 1
#variables inicial de Júpiter
xij = 5.20; yij = 0; vxij = 0;vyij = (4*mt.pi**2/5.20)**0.5;rj = 5.20
h = 0.004

#mas valores iniciales
mt = 6.0e24
mj = 1.9e27
ms = 1.989e30
gms = 4*(np.pi)**2
gmj = 4*(mj/ms)*np.pi**2
gmt = 4*(mt/ms)*np.pi**2

#funcion para realizar las ecuaciones, como solo cambia el valor de xi y yi en las ecuaciones llamo a la misma función pero solo cambio x y y cuando las madno llamar
def velypos(vxij,vxit,xij,xit,gms,gmt,gmj,rjt,rtj,h):
  vxj = vxij - h*(gms*xij)/rj**3- h*(gmt*(xij-xit))/rtj**3
  vxt = vxit - h*(gms*xit)/rt**3 - h*gmj*(xit-xij)/rtj**3
  xj = xij + vxj*h
  xt = xit + vxt*h
  return vxj,vxt,xj,xt

#declaracion de listas
lxj=[];lxt=[];lyj=[];lyt=[];lst=[];lsj=[];ltj=[];lytp=[];lxtp=[]

t=0
tf=11.86
#itera mientras llegue a un año de jupiter
while t<tf:
  rt = np.sqrt(xit**2+yit**2)
  rj = np.sqrt(xij**2+yij**2)
  rtj = np.sqrt((xit-xij)**2+(yit-yij)**2)
  vxj,vxt,xj,xt = velypos(vxij,vxit,xij,xit,gms,gmt,gmj,rtj,rtj,h)
  vyj,vyt,yj,yt = velypos(vyij,vyit,yij,yit,gms,gmt,gmj,rtj,rtj,h)
  vxij = vxj ; vxit = vxt ; xij = xj ; xit =xt; yij = yj ; yit =yt ; vyij = vyj ; vyit = vyt
  lyj.append(yj);lxj.append(xj)
  lyt.append(yt);lxt.append(xt)
  if t<1:  #registra solo para graficar la trayectoria de un año terrestre
    lytp.append(yt);lxtp.append(xt)
  lst.append(rt);lsj.append(rj);ltj.append(rtj) #[aqui se guardan los valores de distancia]
  t+=h


# Función para actualizar la animación en cada cuadro
def update(i):
    try:
        c.set_data([lxt[i]], [lyt[i]]) #grafica cada punto de la trayectoria de la tierra        
        posx_i=str(round(lxt[i],3)) #calcula posicion en x, y y el angulo en cada instante para mostrarlo en la gráfica
        posy_i=str(round(lyt[i],3))     
        j.set_data([lxj[i]], [lyj[i]]) #grafica cada punto de la trayectoria de jupiter      
        posx2_i=str(round(lxj[i],3)) #calcula posicion en x, y y el angulo en cada instante para mostrarlo en la gráfica
        posy2_i=str(round(lyj[i],3))  
        d1_i=str(round(lst[i],3)) 
        d2_i=str(round(lsj[i],3)) 
        d3_i=str(round(ltj[i],3))         
    except IndexError: #garantiza que el programa pueda continuar correctamente si llega al total de los datos en la lista
        c.set_data([lxt[i-1]], [lyt[i-1]])        
        posx_i=str(round(lxt[-1],3)) #guarda la ultima posicion 
        posy_i=str(round(lyt[-1],3)) #y en cada uno redondea para mostrar los valores no tan grandes en el texto de la grafica
        j.set_data([lxj[i-1]], [lyj[i-1]])        
        posx2_i=str(round(lxj[-1],3)) 
        posy2_i=str(round(lyj[-1],3))  
        d1_i=str(round(lst[-1],3)) 
        d2_i=str(round(lsj[-1],3)) 
        d3_i=str(round(ltj[-1],3))        
        pass    
    time_text.set_text(f"""Tiempo: {i * h:.2f} años
                       posición en x de la tierra = {posx_i} UA
                       posición en y de la tierra  = {posy_i} UA 
                       posición en x de jupiter = {posx2_i} UA
                       posición en y de jupiter  = {posy2_i} UA
                       distancia sol-tierra = {d1_i} UA
                       distancia sol-jupiter = {d2_i} UA
                       distancia tierra-jupiter = {d3_i} UA
                       """),
    return (j,)+(c,)+(time_text,)

# Aspectos esteticos/ configuracion de la grafica 
fig, ax = plt.subplots(figsize=(5,5)) 
ax.set_xlabel("x(m)")  # Nombre del eje x 
ax.set_ylabel("y(m)")  # Nombre del eje y
fig.suptitle(f"Movimiento planetario") # Titulo de la gráfica
time_text = plt.text(1,1, '', transform=ax.transAxes, ha='right', va='top') #cuadro de texto para el tiempo
ax.grid()  #cuadriculas
c,=ax.plot(lxt,lyt,marker='o',color='navy',markersize="4") #grafica la tierra
j,=ax.plot(lxt,lyt,marker='o',color='brown',markersize="8") #grafica jupiter
ax.plot(0,0,marker="o",color='gold',markersize="10")
plt.plot(lytp,lxtp,linestyle="--",color="blue")
plt.plot(lyj,lxj,linestyle="--",color="brown")
# Configuración de la animación
ani = FuncAnimation(fig, update,  #esta funcion anima
                    blit=True, interval=0, repeat=False)
plt.show()

