import numpy as np 
import pandas as pd
import pickle

def CONCRETA(ARQ):
    AUX = ARQ + '.xlsx'
    ENTRADA = pd.read_excel(AUX, dtype = np.float64)
    ENTRADA.rename(columns = {
                              'Cement (kg)':'c', 
                              'Superplasticizer (kg)': 'sp',
                              'Water/Cement':'w-c ratio', 
                              'Addtion (kg)': 'add',
                              'Coarse Aggregate (kg)': 'cag',
                              'Fine Aggregate (kg)': 'fag',
                              'Cure time (days)': 't',
                             }, inplace = True)

    # Leitura das variavéis de escala
    AUX_1 = "scale.sav"
    ESCALAS = pickle.load(open(AUX_1, 'rb'))

    # Leitura das variáveis do modelo
    AUX_2 = "model.sav"
    MODELO = pickle.load(open(AUX_2, 'rb'))

    # Normalização das entradas
    ENTRADA_NORMAL = ENTRADA.copy()
    for COL in ENTRADA_NORMAL:
        ENTRADA_NORMAL[COL] = ENTRADA_NORMAL[COL].apply(lambda x: (x - ESCALAS[COL][0])/ ESCALAS[COL][1])

    # Predição
    for INDEX, ROW in ENTRADA_NORMAL.iterrows():
        VAL = ROW[0:7]
        DATA = np.array([VAL.tolist()])
        X = pd.DataFrame(DATA, columns = ['c', 'sp', 'cag', 'fag', 't', 'w-c ratio', 'add'])
        RESULT = MODELO[0].predict(X)
        print('fck = ', RESULT[0], 'MPa')