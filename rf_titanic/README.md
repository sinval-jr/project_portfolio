# **Previsão de Sobrevivência no Titanic com RandomForest (Scikit-learn)**
Uma implementação de um pipeline de Machine Learning com o algoritmo RandomForest para prever a sobrevivência dos passageiros do Titanic.

## 🎯 **Objetivo**
Desenvolver um modelo de Machine Learning robusto para prever a sobrevivência de passageiros do Titanic, utilizando um classificador RandomForest otimizado para alcançar máxima precisão.

## 📊 **Base de Dados – Titanic**
O dataset do Titanic, famoso em competições do Kaggle, é utilizado para treinar o modelo. Ele contém informações demográficas e de viagem dos passageiros:

**Variáveis Preditivas (Features):** Pclass (classe social), Sex, Age, Embarked (porto de embarque), SibSp (irmãos/cônjuges a bordo), Parch (pais/filhos a bordo).

**Variável Alvo (Target):** Survived (0 = Não sobreviveu, 1 = Sobreviveu).

## 🏗️ **Pipeline de Machine Learning**
O processo para construir e avaliar o modelo seguiu as seguintes etapas:

**Pré-processamento de Dados:**

- Remoção de Colunas: Exclusão de features irrelevantes ou com excesso de valores nulos (Name, Ticket, Cabin, PassengerId, Fare).

- Tratamento de Variáveis Categóricas: Conversão das colunas Sex e Embarked para formato numérico usando LabelEncoder.

- Tratamento de Valores Ausentes: Preenchimento dos valores nulos na coluna Age com a mediana das idades.

**Otimização de Hiperparâmetros:**

- Utilização do GridSearchCV para testar sistematicamente várias combinações de hiperparâmetros do RandomForest.

- Parâmetros Otimizados: n_estimators, max_depth e min_samples_split.

- Validação Cruzada (CV=5): O GridSearchCV usou 5 partições dos dados de treino para garantir que o desempenho do modelo fosse estável e evitar overfitting.

**Modelo Final:**

O modelo final é um RandomForestClassifier treinado com os melhores parâmetros encontrados na etapa de otimização.

## **Tecnologias Utilizadas**
As principais ferramentas utilizadas no projeto.

- Linguagem: Python

- Bibliotecas: Scikit-learn, Pandas, NumPy

## 📈 **Resultados**
**Precisão Alcançada:** 93% no conjunto de testes.

O modelo otimizado, após ser treinado com os melhores hiperparâmetros identificados pelo GridSearchCV, demonstrou uma ótima capacidade de generalização dos dados, sendo perceptível pela validação cruzada e validação com dados testes;