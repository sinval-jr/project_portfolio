# Classificação da Base de Dados Iris com Rede Neural (TensorFlow/Keras)
Uma implementação de uma Rede Neural Densa (MLP) para classificar as espécies de flores da base de dados Iris.

## 🎯 **Objetivo**
Construir e treinar uma Rede Neural para atingir alta precisão na classificação das três espécies de flores do conjunto de dados Iris (Setosa, Versicolor e Virginica).

## 📊 **Base de Dados – Iris**
O Iris é um conjunto de dados clássico para problemas de classificação em aprendizado de máquina, composto por:

- **150 amostras no total**.

- 4 características (features) por amostra:

- Comprimento da sépala (cm)

- Largura da sépala (cm)

- Comprimento da pétala (cm)

- Largura da pétala (cm)

- **3 classes (espécies):** Iris Setosa, Iris Versicolor e Iris Virginica.

## 🏗️ **Arquitetura da Rede Neural**
A rede neural desenvolvida segue a seguinte estrutura de um Perceptron de Múltiplas Camadas (MLP):

1) Camada de Entrada (com 4 neurônios, correspondentes às 4 características do dataset)

2) Camada Densa Oculta (4 neurônios, função de ativação ReLU)

3) Camada Densa Oculta (4 neurônios, função de ativação ReLU)

4) Camada de Saída (3 neurônios, função de ativação Softmax para classificação multiclasse)

## **Tecnologias Utilizadas** 
As principais ferramentas utilizadas para o treinamento da rede.

- Linguagem: Python (3.12.1)

- Frameworks: TensorFlow, Keras

- Bibliotecas: Scikit-learn, NumPy, Pandas

## 📈 **Resultados**
**Precisão Alcançada:** 92% no conjunto de testes.

O desempenho do modelo foi avaliado utilizando uma matriz de confusão, que detalha os acertos e erros para cada uma das três classes.