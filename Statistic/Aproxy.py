from scipy.optimize import curve_fit
import math 
import numpy as np
import pandas as pd


def mapping_time_live(values_x, a, b):     
    #return (2.71**values_x)*b + a                  # не работает на времени жизни
    #return a/values_x + b                          # 7.484% на времени жизни
    return a/(values_x**2) + b                      # не работает на времени жизни
    #return (np.log(values_x)*b + a)                # 11.134% на времени жизни
    #return ((2.71**values_x)*b + a*(values_x**2))  # не работает на времени жизни
    #return ((values_x)*b + a*(values_x**2))        # 24.737% на времени жизни
    #return ((values_x)*b + a)                      # 14.649% на времени жизни
    #return (a/(values_x**(1/2)) + b)               # 9.327% на времени жизни
    #return (a/(values_x**(b)))                     # не работает на времени жизни

def mapping_alive(values_x, a, b):
    #return (2.71**values_x)*a + b                  # не работает на активных
    #return a/values_x + b                          # 33.171% на активных
    return a/(values_x**2) + b                      # 12.015% на активных
    #return (np.log(values_x)*a + b)                # 66.715% на активных
    #return ((2.71**values_x)*b + a*(values_x**2))  # не работает на активных
    #return ((values_x)*b + a*(values_x**2))        # 146.078% на активных
    #return ((values_x)*b + a)                      # 93.767% на активных
    #return (a/(values_x**(1/2)) + b)               # 50.455% на активных
    #return (a/(values_x**(b)))                     # 43.018% на активных

id_point : int = 0

df_orders = pd.read_excel(f'Statistic\\result\\depend_live_time_on_traps\\Function_{id_point}.xlsx', index_col=0)
#print(df_orders)

x_time_live = np.array([])
y_time_live = np.array([])

for i in range(len(df_orders['trapsCount'])):
    if(df_orders['CountData'][i] != 0):
        x_time_live = np.append(x_time_live,df_orders['trapsCount'][i])
        y_time_live = np.append(y_time_live,df_orders['mean_time_live'][i])

# print(ydata)

args, covar = curve_fit(mapping_time_live,x_time_live,y_time_live)
a =  args[0]
b =  args[1]
print(a,b)

yint=[]
for x in x_time_live:
    yint.append(mapping_time_live(x,a,b))


so = 0
for i in range(len(y_time_live)):
    if(y_time_live[i] !=0):
        so += abs(yint[i]-y_time_live[i])/y_time_live[i]
so = so / (len(y_time_live)) * 100
so = round(so,3)
print(so)

x_alive = df_orders['trapsCount']
y_alive = df_orders['mean_count_alive']

args, covar = curve_fit(mapping_alive,x_alive,y_alive)
a =  args[0]
b =  args[1]
print(a,b)

yint=[]
for x in x_alive:
    yint.append(mapping_alive(x,a,b))

so = 0
for i in range(len(y_alive)):
    if(y_alive[i] !=0):
        so += abs(yint[i]-y_alive[i])/y_alive[i]

so = so / (len(y_time_live)) * 100
so = round(so,3)
print(so)