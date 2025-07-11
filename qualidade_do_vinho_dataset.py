# -*- coding: utf-8 -*-
"""Qualidade do Vinho - Dataset

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JoyzImg5CJqrVmmuUBsQKHF91wvpS77y
"""

import pandas as pd
import numpy as np

# Visualização
import matplotlib.pyplot as plt
import seaborn as sns

# Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
df = pd.read_csv(url, sep=';')
df.head()

df.info()

df.isnull().sum()

df.describe()

sns.countplot(x='quality', data=df)
plt.title('Distribuição das notas de qualidade do vinho')
plt.show()

df.hist(bins=15, figsize=(15, 10), layout=(4,3))
plt.tight_layout()
plt.show()

plt.figure(figsize=(15,8))
sns.boxplot(data=df)
plt.xticks(rotation=45)
plt.title('Boxplot de variáveis para detecção de outliers')
plt.show()

correlation_matrix = df.corr()
correlation_matrix

plt.figure(figsize=(12,8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Mapa de calor das correlações')
plt.show()

plt.figure(figsize=(10,6))
sns.boxplot(x='quality', y='alcohol', data=df, palette="Blues")
plt.title('Distribuição do teor alcoólico por qualidade do vinho', fontsize=14)
plt.xlabel('Qualidade', fontsize=12)
plt.ylabel('Teor Alcoólico', fontsize=12)
plt.tight_layout()
plt.show()

sns.boxplot(x='quality', y='volatile acidity', data=df)
plt.title('Distribuição da acidez volátil por qualidade do vinho')
plt.show()

X = df.drop('quality', axis=1)
y = df['quality']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
lr_preds = lr.predict(X_test_scaled)

rf = RandomForestRegressor(random_state=42)
rf.fit(X_train_scaled, y_train)
rf_preds = rf.predict(X_test_scaled)

lr_mse = mean_squared_error(y_test, lr_preds)
lr_r2 = r2_score(y_test, lr_preds)

rf_mse = mean_squared_error(y_test, rf_preds)
rf_r2 = r2_score(y_test, rf_preds)

print(f"Linear Regression - MSE: {lr_mse:.3f}, R2: {lr_r2:.3f}")
print(f"Random Forest - MSE: {rf_mse:.3f}, R2: {rf_r2:.3f}")

plt.scatter(y_test, rf_preds)
plt.xlabel('Qualidade Real')
plt.ylabel('Qualidade Prevista')
plt.title('Random Forest: Valores Reais vs Previsto')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.show()

importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]
feature_names = X.columns

plt.figure(figsize=(12,6))
sns.barplot(x=importances[indices], y=feature_names[indices], palette='viridis')
plt.title('Importância das Variáveis no Random Forest')
plt.xlabel('Importância')
plt.ylabel('Variáveis')
plt.tight_layout()
plt.show()

correlations = df.corr()['quality'].abs().sort_values(ascending=False)
correlations

# Selecionar as variáveis mais correlacionadas
top_features = correlations.index[1:5]  # ignorando 'quality' que fica em primeiro
print("Variáveis mais correlacionadas:", top_features.tolist())

# Criar pairplot
sns.pairplot(df[top_features.to_list() + ['quality']], hue='quality', palette='coolwarm', height=2.5)
plt.suptitle('Pairplot das variáveis mais correlacionadas com a qualidade', y=1.02)
plt.show()

from sklearn.model_selection import cross_val_score, KFold

# Configurar K-Fold com 5 divisões
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Calcular R² médio com validação cruzada
cv_scores = cross_val_score(rf, X_train_scaled, y_train, cv=kf, scoring='r2')

print(f"R² médio na validação cruzada: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

from sklearn.model_selection import GridSearchCV

# Definir grade de hiperparâmetros para Random Forest
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10]
}

# Configurar busca em grade
grid_search = GridSearchCV(RandomForestRegressor(random_state=42), param_grid,
                           cv=3, scoring='r2', n_jobs=-1, verbose=2)

# Executar busca de hiperparâmetros
grid_search.fit(X_train_scaled, y_train)

print("Melhores hiperparâmetros encontrados:")
print(grid_search.best_params_)

best_rf = grid_search.best_estimator_
best_rf_preds = best_rf.predict(X_test_scaled)

best_mse = mean_squared_error(y_test, best_rf_preds)
best_r2 = r2_score(y_test, best_rf_preds)

print(f"Random Forest Otimizado - MSE: {best_mse:.3f}, R²: {best_r2:.3f}")