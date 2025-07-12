import numpy as np
np.set_printoptions(precision=3, suppress=True, linewidth=200)
# Função para calcular a matriz de rigidez de uma barra
def calcular_matriz_rigidez(E, I, A, L):
    return np.array([
        [E*A/L, 0, 0, -E*A/L, 0, 0],
        [0, 12*E*I/L**3, 6*E*I/L**2, 0, -12*E*I/L**3, 6*E*I/L**2],
        [0, 6*E*I/L**2, 4*E*I/L, 0, -6*E*I/L**2, 2*E*I/L],
        [-E*A/L, 0, 0, E*A/L, 0, 0],
        [0, -12*E*I/L**3, -6*E*I/L**2, 0, 12*E*I/L**3, -6*E*I/L**2],
        [0, 6*E*I/L**2, 2*E*I/L, 0, -6*E*I/L**2, 4*E*I/L]
    ])

# Função para calcular a matriz de rotação em graus
def calcular_matriz_rotacao(theta):
    return np.array([
        [np.cos(np.deg2rad(theta)), np.sin(np.deg2rad(theta)), 0, 0, 0, 0],
        [-np.sin(np.deg2rad(theta)), np.cos(np.deg2rad(theta)), 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, np.cos(np.deg2rad(theta)), np.sin(np.deg2rad(theta)), 0],
        [0, 0, 0, -np.sin(np.deg2rad(theta)), np.cos(np.deg2rad(theta)), 0],
        [0, 0, 0, 0, 0, 1]
    ])

# Definindo os parâmetros das barras
Eab = 25e6
Ebd = 25e6
Edc = 25e6
Ede = 200e6

Lab = 4
Lbd = 4
Ldc = 4
Lde = 5

Aab = 0.16
Abd = 0.18
Adc = 0.16
Ade = 0.00126

Iab = 2.133e-3
Ibd = 5.4e-3
Idc = 2.133e-3
Ide = 0.7854e-8

# Ângulos em graus
anguloab = 90
angulobc = 0
angulocd = -90
angulode = -53
# Gerando as matrizes de rigidez para cada barra
Kab = calcular_matriz_rigidez(Eab, Iab, Aab, Lab)
Kbd = calcular_matriz_rigidez(Ebd, Ibd, Abd, Lbd)
Kdc = calcular_matriz_rigidez(Edc, Idc, Adc, Ldc)
Kde = calcular_matriz_rigidez(Ede, Ide, Ade, Lde)

# Gerando as matrizes de rotação para cada barra
Rab = calcular_matriz_rotacao(anguloab)
Rbc = calcular_matriz_rotacao(angulobc)
Rcd = calcular_matriz_rotacao(angulocd)
Rde = calcular_matriz_rotacao(angulode)

# Função para calcular a matriz de rigidez no sistema global
def calcular_matriz_global(K_local, R):
    R_T = np.transpose(R)
    return np.dot(np.dot(R_T, K_local), R)

# Calculando as matrizes de rigidez no sistema global
K_global_ab = calcular_matriz_global(Kab, Rab)
K_global_bc = calcular_matriz_global(Kbd, Rbc)
K_global_cd = calcular_matriz_global(Kdc, Rcd)
K_global_de = calcular_matriz_global(Kde, Rde)

# Função para formatar a matriz com notação científica
def formatar_matriz(matriz):
    return np.array2string(matriz, formatter={'float_kind': lambda x: f"{x:.2e}"})

# Imprimindo as matrizes de rigidez global
print("\nMatriz de rigidez global para a barra AB:")
print(formatar_matriz(K_global_ab))
print("\nMatriz de rigidez global para a barra BD:")
print(formatar_matriz(K_global_bc))
print("\nMatriz de rigidez global para a barra DC:")
print(formatar_matriz(K_global_cd))
print("\nMatriz de rigidez global para a barra DE:")
print(formatar_matriz(K_global_de))

# Função para calcular os vetores de força
def calcular_vetor_forca(q, L):
    F_v = q * L / 2  # Força vertical
    M = q * L**2 / 12  # Momento
    return np.array([
        [0], [F_v], [M],
        [0], [F_v], [-M]
    ])

# Carga distribuída na barra BC
q_bc = 40  # kN/m
L_bc = 4  # m

# Calculando os vetores de força locais
f_ab = np.zeros((6, 1))
f_bc = calcular_vetor_forca(q_bc, L_bc)
f_cd = np.zeros((6, 1))
f_de = np.zeros((6, 1))

# Função para calcular o vetor de força global
def calcular_vetor_forca_global(f_local, R):
    R_T = np.transpose(R)
    return np.dot(R_T, f_local)

# Calculando os vetores de força globais
f_global_ab = calcular_vetor_forca_global(f_ab, Rab)
f_global_bc = calcular_vetor_forca_global(f_bc, Rbc)
f_global_cd = calcular_vetor_forca_global(f_cd, Rcd)
f_global_de = calcular_vetor_forca_global(f_de, Rde)

# Imprimindo os vetores de força globais
print("\nVetor de força global para a barra AB:")
print(formatar_matriz(f_global_ab))
print("\nVetor de força global para a barra BD:")
print(formatar_matriz(f_global_bc))
print("\nVetor de força global para a barra CD:")
print(formatar_matriz(f_global_cd))
print("\nVetor de força global para a barra DE:")
print(formatar_matriz(f_global_de))

# Construção da Matriz Global 15x15
K_global = np.zeros((15, 15))
K_global[0:6, 0:6] += K_global_ab
K_global[3:9, 3:9] += K_global_bc
K_global[6:12, 6:12] += K_global_cd
K_global[6:9, 6:9] += K_global_de[0:3, 0:3]
K_global[6:9, 12:15] += K_global_de[0:3, 3:6]
K_global[12:15, 6:9] += K_global_de[3:6, 0:3]
K_global[12:15, 12:15] += K_global_de[3:6, 3:6]

# Imprimindo a matriz global
print("\nMatriz Global 15x15:")
print(formatar_matriz(K_global))

# Construção do vetor de força global 15x1
f_global = np.zeros((15, 1))
f_global[0:6, 0] += f_global_ab[:, 0]
f_global[3:9, 0] += f_global_bc[:, 0]
f_global[6:12, 0] += f_global_cd[:, 0]
f_global[9:15, 0] += f_global_de[:, 0]

# Imprimindo o vetor de força global 15x1
print("\nVetor de força global 15x1:")
print(formatar_matriz(f_global))

# Construção da matriz global reduzida
def calcular_matriz_global_reduzida(K_global_ab, K_global_bc, K_global_cd, K_global_de):
    Srd = np.zeros((8, 8))
    Srd[0:3, 0:3] = K_global_ab[3:6, 3:6] + K_global_bc[0:3, 0:3]
    Srd[0:3, 3:6] = K_global_bc[0:3, 3:6]
    Srd[3:6, 0:3] = K_global_bc[3:6, 0:3]
    Srd[3:6, 3:6] = K_global_bc[3:6, 3:6] + K_global_cd[0:3, 0:3] + K_global_de[0:3, 0:3]
    Srd[6, 3:6] = K_global_cd[5, 0:3]
    Srd[7, 3:6] = K_global_de[5, 0:3]
    Srd[3:6, 6] = K_global_cd[0:3, 5]
    Srd[3:6, 7] = K_global_de[0:3, 5]
    Srd[6, 6] = K_global_cd[5, 5]
    Srd[7, 7] = K_global_de[5, 5]
    return Srd

# Calculando a matriz global reduzida
K_reduzida = calcular_matriz_global_reduzida(K_global_ab, K_global_bc, K_global_cd, K_global_de)

# Imprimindo a matriz global reduzida
print("\nMatriz Global Reduzida:")
print(formatar_matriz(K_reduzida))

# Calculando o vetor de força global reduzido
f_global_reduzido = np.zeros((1, 8))
f_global_reduzido[0, 0:3] += f_global_ab[2:5, 0] + f_global_bc[0:3, 0]
f_global_reduzido[0, 3:6] += f_global_bc[3:6, 0] + f_global_cd[0:3, 0]
f_global_reduzido[0, 6] += f_global_cd[5, 0] + f_global_de[2, 0]
f_global_reduzido[0, 7] += f_global_de[5, 0]

# Imprimindo o vetor de força global reduzido
print("\nVetor de força global reduzido 8x1:")
print(formatar_matriz(f_global_reduzido))

# Inicializando o vetor de graus de liberdade
graus_liberdade = np.ones(15)
graus_liberdade[0:3] = [1, 1, 1]  # Nó A
graus_liberdade[3:6] = [-20, 0, 0]  # Nó B
graus_liberdade[6:9] = [0, 0, 0]  # Nó C
graus_liberdade[9:12] = [1, 1, 0]  # Nó D
graus_liberdade[12:15] = [1, 1, 0]  # Nó E

# Imprimindo o vetor de graus de liberdade
print("\nVetor de Graus de Liberdade A:")
print(graus_liberdade)

# Vetor de graus de liberdade reduzido
graus_liberdade_reduzido = np.ones(8)
graus_liberdade_reduzido[0:6] = graus_liberdade[3:9]
graus_liberdade_reduzido[6] = graus_liberdade[11]
graus_liberdade_reduzido[7] = graus_liberdade[14]

# Imprimindo o vetor de graus de liberdade reduzido
print("\nMatriz reduzida de graus de liberdade:")
print(graus_liberdade_reduzido)

# Calculando os deslocamentos
K_reduzida_inv = np.linalg.inv(K_reduzida)
f_global_reduzido_t = f_global_reduzido.reshape(8, 1)
graus_liberdade_reduzido_t = graus_liberdade_reduzido.reshape(8, 1)
diferenca = graus_liberdade_reduzido_t - f_global_reduzido_t

deslocamentos = np.dot(K_reduzida_inv, diferenca)
print("\nDeslocamentos:")
print(deslocamentos)

# Função para construir a matriz global reduzida 1
Sg = np.zeros((7, 8))
Sg[0:3, 0:3] = K_global_ab[0:3, 3:6]
Sg[3:5, 3:6] = K_global_cd[3:5, 0:3]
Sg[5:8, 3:6] = K_global_de[3:5, 0:3]
Sg[3:5, 6] = K_global_cd[3:5, 5]
Sg[5:7, 7] = K_global_de[3:5 ,5]

print("\nMatriz global reduzida:")
print(Sg)

# Calculando as reações
reacoes = np.dot(Sg, deslocamentos)
print("\nReações:")
print(reacoes)

# Calculando os esforços internos
# Definindo o vetor de deslocamentos 15 x 1
VetorDesloc = np.zeros((15, 1))

VetorDesloc[3:9, 0] = deslocamentos[0:6, 0]
VetorDesloc[11, 0] = deslocamentos[6, 0]
VetorDesloc[14, 0] = deslocamentos[7, 0]

print("\nVetor de deslocamentos 15 x 1")
print(VetorDesloc)

# Deslocamentos para cada elemento
DeslElem1 = np.zeros((6, 1))
DeslElem1[0:6, 0] = VetorDesloc[0:6, 0]

DeslElem2 = np.zeros((6, 1))
DeslElem2[0:6, 0] = VetorDesloc[3:9, 0]

DeslElem3 = np.zeros((6, 1))
DeslElem3[0:6, 0] = VetorDesloc[6:12, 0]

DeslElem4 = np.zeros((6, 1))
DeslElem4[0:6, 0] = VetorDesloc[9:15, 0]

# Esforços internos nos elementos
EsfIntElem1 = (K_global_ab @ DeslElem1) + f_global_ab
print("\nEsforços no elemento AB:")
print(EsfIntElem1)

EsfIntElem2 = f_global_bc + (K_global_bc @ DeslElem2)
print("\nEsforços no elemento BD:")
print(EsfIntElem2)

EsfIntElem3 = f_global_cd + (K_global_cd @ DeslElem3)
print("\nEsforços no elemento CD:")
print(EsfIntElem3)

EsfIntElem4 = f_global_de + (K_global_de @ DeslElem4)
print("\nEsforços no elemento DE:")
print(EsfIntElem4)
