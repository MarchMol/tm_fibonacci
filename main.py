import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit
import tm_sim
import numpy as np

def empirical(max, tm, accept, start):
    df = pd.DataFrame(columns=["n", "t"])
    one = "1"
    for i in range(1,max):
        n = "_"+i*one
        tape = tm_sim.tokenize(n)
        t_n = tm_sim.sim(tm,tape, start, accept, False,"time")
        df = pd.concat([df, pd.DataFrame({"n": [i], "t": [t_n]})], ignore_index=True)
    return df

def power_regression(x, y):
    def power_func(x, a, b):
        return a * (x ** b)
    params, _ = scipy.optimize.curve_fit(power_func, x, y, p0=(1, 1))
    a, b = params

    x_fit = np.linspace(min(x), max(x), len(x))
    y_fit = power_func(x_fit, a, b)
    r2_pow = r2_score(Y, y_fit)
    

    plt.title(f"Regresión Polinomial: R2 {r2_pow:.4f}")
    plt.scatter(x, y, label="Empírico", color="red")
    plt.plot(x_fit, y_fit, label=f"Regresión: y = {a:.4f} * x^{b:.4f}", color="blue")
    plt.xlabel("Tamaño de entrada")
    plt.ylabel("Movimientos")
    plt.legend()
    plt.show()

def exp_reg(X,Y):
    def exp_function(x, a):
        return a**x
    params, _ = curve_fit(exp_function, X, Y)
    a_best = params[0]
    y_pred = exp_function(X, a_best)

    r2_exp = r2_score(Y, y_pred)

    plt.title(f"Regresión Exponencial: R2 {r2_exp:.4f}")
    plt.scatter(X,Y)
    plt.plot(X, y_pred, color="green", label=f"Regresion: y = {a_best:.2f}^x)")
    plt.xlabel("Tamaño de entrada")
    plt.ylabel("Movimientos")
    plt.legend()
    plt.show()


    
def print_seq(tape):
    rslt = ""
    for ch in tape:
        rslt+=ch
    rslt = rslt.split('|')[1]
    unary = rslt.split("#")
    fib = []
    for un in unary:
        if ("%" in un):
            fib.append(len(un)-1)
        else:
            fib.append(len(un))
            
    print(fib)
    

def test(tm, accept, start, input, showconfig, ret):
    tape = tm_sim.tokenize(input)
    rslt = tm_sim.sim(tm,tape,start,accept,showconfig,ret)
    return rslt



# Inicializar máquina de turing
accept,start,TM = tm_sim.gen_tm('./transitions.txt')

# ------ Prueba ------ #
# init_state = "_111"

# # Configuraciones
# showconfig = True
# ret = ''
# test(TM, accept, start, init_state, showconfig, ret)


# # Secuencia / cinta
# showconfig = False
# ret = 'tape'
# tape = test(TM, accept, start, init_state, showconfig, ret)
# print(tape)
# print_seq(tape)

# # Tiempo individual:
# showconfig = False
# ret = 'time'
# time = test(TM, accept, start, init_state, showconfig, ret)
# print(time)

# ------ Análisis ------ #
# time_analysis = empirical(10,TM,accept,start)
# X = time_analysis["n"].values
# Y = time_analysis['t'].values

# exp_reg(X,Y)
# power_regression(X,Y)