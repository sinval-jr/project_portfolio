import pandas as pd
import dash
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import math
from scipy import stats
import numpy as np


def calcular_estatisticas(df):

    dados = df

    if dados.empty:
        return None
    
    media = dados.mean()
    moda = dados.mode().iloc[0] if not dados.mode().empty else None
    mediana = dados.median()
    desvio_padrao = dados.std()
    q1 = dados.quantile(0.25)
    q3 = dados.quantile(0.75)
    coef_variacao = (desvio_padrao / media) * 100 if media != 0 else None
    n = len(dados.dropna())
    z = 1.96
    if n > 1:
        erro_padrao = desvio_padrao / math.sqrt(n)
        margem_erro = z * erro_padrao
        ic_min = media - margem_erro
        ic_max = media + margem_erro
    else:
        ic_min, ic_max = media, media

    return {
        "média": round(media, 2),
        "moda": moda,
        "mediana": round(mediana, 2),
        "desvio_padrão": round(desvio_padrao, 2),
        "Q1 (25%)": round(q1, 2),
        "Q3 (75%)": round(q3, 2),
        "coef_variação (%)": round(coef_variacao, 2) if coef_variacao is not None else None,
        "Intervalo_min": round(ic_min, 2),
        "Intervalo_max": round(ic_max, 2)
    }

def teste_hipotese_duas_medias(grupo1, grupo2, nome_grupo1="Grupo A", nome_grupo2="Grupo B", alpha=0.05):
    """
    Executa o teste t de Welch para comparar as médias de dois grupos independentes.

    Parâmetros:
        grupo1, grupo2: Series ou arrays numéricos
        nome_grupo1, nome_grupo2: nomes opcionais para exibição
        alpha: nível de significância (default = 0.05)

    Retorna:
        html.Div com hipóteses, estatística t, p-valor e conclusão
    """
    # Limpando valores ausentes
    grupo1 = np.array(grupo1.dropna())
    grupo2 = np.array(grupo2.dropna())

    # Estatísticas básicas
    media1 = grupo1.mean()
    media2 = grupo2.mean()
    n1 = len(grupo1)
    n2 = len(grupo2)

    # Teste t de Welch
    t_stat, p_valor = stats.ttest_ind(grupo1, grupo2, equal_var=False)

    # Hipóteses
    h0 = f"H₀: μ({nome_grupo1}) = μ({nome_grupo2})"
    h1 = f"H₁: μ({nome_grupo1}) ≠ μ({nome_grupo2})"

    # Decisão
    decisao = "✅ Rejeitamos H₀: diferença significativa." if p_valor < alpha else "❌ Não rejeitamos H₀: sem evidência significativa."

    return html.Div([
        html.H2("Teste de Hipótese: Comparação de Médias"),
        html.P(h0, style={"margin": "0"}),
        html.P(h1, style={"margin": "0 0 10px 0"}),

        html.P(f"Média de {nome_grupo1}: {media1:.2f} (n = {n1})"),
        html.P(f"Média de {nome_grupo2}: {media2:.2f} (n = {n2})"),
        html.P(f"t = {t_stat:.4f}"),
        html.P(f"p-valor = {p_valor:.4f}", style={"marginBottom": "10px"}),

        html.H4(decisao, style={"color": "#007bff" if p_valor >= alpha else "#dc3545"})
    ], style={
        "padding": "15px",
        "border": "1px solid #ccc",
        "borderRadius": "10px",
        "backgroundColor": "#f9f9f9",
        "boxShadow": "0px 2px 5px rgba(0,0,0,0.1)",
        "maxWidth": "500px",
        "margin": "auto",
        "fontFamily": "Arial"
    })



app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
    
# Carregar os dados
df = pd.read_csv("datasets/student_habits_performance.csv")

# Layout da aplicação
app.layout = html.Div([
    html.Label("Selecione a faixa de exam_score:"),
    dcc.RangeSlider(
        id='slider-exam-score',
        min=0,
        max=100,
        step=1,
        value=[50, 100],  # faixa inicial
        marks={0: '0',25: '25', 50: '50',75: '75', 100: '100'}
    ),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Demografia', value='tab-1'),
        dcc.Tab(label='Entreterimento', value='tab-2'),
        dcc.Tab(label='Healthy', value='tab-3'),
    ]),
    html.Div(id='tabs-content')
        
])
    
@callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value'),
    Input('slider-exam-score', 'value')
)
def render_content(tab, faixa):
    faixa_min, faixa_max = faixa
    df_filtrado = df[(df["exam_score"] >= faixa_min) & (df["exam_score"] <= faixa_max)]

    if tab == 'tab-1':
        if df_filtrado.empty:
            return html.Div("Nenhum dado disponível na faixa selecionada.")
        # Frequência de Idade dos Estudantes
        df_count = df_filtrado["age"].value_counts().reset_index()
        df_count.columns = ["age", "quantidade"]
        fig1 = px.bar(
            df_count,
            x="age",
            y="quantidade",
            title=None,
            text="quantidade"
        )
        fig1.update_traces(textposition='outside')
        fig1.update_layout(yaxis_title="Quantidade de Pessoas")

        #Valores da média, moda - Gráfico 1
        valor1 = calcular_estatisticas(df_filtrado["age"])

        #Valores da média, moda
        moda_genero = df_filtrado["gender"].mode().iloc[0] if not df_filtrado["gender"].mode().empty else "N/A"


        # Gráfico 2: Frequência dos Estudantes por gênero
        df_count = df_filtrado["gender"].value_counts().reset_index()
        df_count.columns = ["gender", "quantidade"]
        fig2 = px.bar(
            df_count,
            x="gender",
            y="quantidade",
            title=None,
            text="quantidade"
        )
        fig2.update_traces(textposition='outside')
        fig2.update_layout(yaxis_title="Quantidade de Pessoas")

        # Gráfico 3: Distribuição de Idades (Bloxplot)
        fig3 = px.box(df_filtrado, y="age", title="Distribuição de Valores (Boxplot)")
        fig3.update_layout(yaxis_title="Valores")

        return html.Div([
            # Gráfico de idade + textos dentro do mesmo bloco
            html.Div([
                html.Div([
                    html.H1(f"Quantidade de Pessoas por Idade ({faixa_min}-{faixa_max})", style={'margin': '0'}),
                    html.P(f"Média das idades: {valor1['média']:.2f}", style={'margin': '10px 0 0 0'}),
                    html.P(f"Moda: {valor1['moda']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Mediana : {valor1['mediana']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Desvio Padrão: {valor1['desvio_padrão']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q1 (25%): {valor1['Q1 (25%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q3 (75%): {valor1['Q3 (75%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"coef_variação (%): {valor1['coef_variação (%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Min): {valor1['Intervalo_min']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Max): {valor1['Intervalo_max']}", style={'margin': '0 0 0 0'}),
                ], style={'display': 'flex', 'textAlign': 'center','flexDirection': 'column'}),
                dcc.Graph(figure=fig1)
            ], style={
                'width': '50%',
                'padding': '10px',
                'boxSizing': 'border-box'
            }),

            # Segundo Blovo - Grafico Quantidade de Pessoas por Gênero
            
            html.Div([
                html.Div([
                    html.H1(f"Quantidade de Pessoas por Gênero ({faixa_min}-{faixa_max})", style={'margin': '0'}),
                    html.P(f"Gênero com maior frequência: {moda_genero}", style={'margin': '0'}),
                ], style={'display': 'flex', 'textAlign': 'center','flexDirection': 'column'}),
                dcc.Graph(figure=fig2)
            ], style={
                'width': '50%',
                'padding': '10px',
                'boxSizing': 'border-box'
            }),

            # Terceiro bloco - gráfico boxplot presença
            html.Div([
                html.Div([
                    html.H1(f"Distribuição das Idades ({faixa_min}-{faixa_max})", style={'margin': '0'}),
                    # Se quiser, pode acrescentar algum texto descritivo aqui
                    html.P("Boxplot do Frequência de idades.", style={'margin': '0 0 10px 0', 'textAlign': 'center'}),
                ], style={'display': 'flex', 'textAlign': 'center','flexDirection': 'column'}),
                dcc.Graph(figure=fig3)
            ], style={
                'width': '33%',
                'padding': '10px',
                'boxSizing': 'border-box'
            }),
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'flexWrap': 'wrap',
            'alignItems': 'flex-start',
            'justifyContent': 'center'
        })

    elif tab == 'tab-2':
        if df_filtrado.empty:
            return html.Div("Nenhum dado disponível na faixa selecionada.")
        # Gráfico 1: Frequência de horas nas mídias sociais
        df_count = df_filtrado["social_media_hours"].value_counts().reset_index()
        df_count.columns = ["social_media_hours", "quantidade"]
        fig1 = px.bar(
            df_count,
            x="social_media_hours",
            y="quantidade",
            title=None,
            text="quantidade"
        )
        fig1.update_traces(textposition='outside')
        fig1.update_layout(yaxis_title="Quantidade de Pessoas")

        #Medidas estatísticas - Grafico 1
        valor1 = calcular_estatisticas(df_filtrado["social_media_hours"])

        # Gráfico 2: Frequência de horas assistindo Netflix
        df_count = df_filtrado["netflix_hours"].value_counts().reset_index()
        df_count.columns = ["netflix_hours", "quantidade"]
        fig2 = px.bar(
            df_count,
            x="netflix_hours",
            y="quantidade",
            title=None,
            text="quantidade"
        )
        fig2.update_traces(textposition='outside')
        fig2.update_layout(yaxis_title="Quantidade de Pessoas")

        #Medidas estatísticas - Grafico 2
        valor2 = calcular_estatisticas(df_filtrado["netflix_hours"])

        # Gráfico 3: Distribuição de Idades (Bloxplot)
        fig3 = px.box(df_filtrado, y="netflix_hours", title="Distribuição de Valores (Boxplot)")
        fig3.update_layout(yaxis_title="Valores")

        # Teste de Hipótese: Comparação de Médias
        grupo_A = df[df["social_media_hours"] <= 3.5]["exam_score"]
        grupo_B = df[df["social_media_hours"] > 3.5]["exam_score"]
        teste_html_1 = teste_hipotese_duas_medias(grupo_A, grupo_B, nome_grupo1="≤ 3h Social Media", nome_grupo2="> 3   h Social Media")
        
        # Teste de Hipótese: Comparação de Médias
        grupo_A = df[df["netflix_hours"] <= 2]["exam_score"]
        grupo_B = df[df["netflix_hours"] > 2]["exam_score"]
        teste_html_2 = teste_hipotese_duas_medias(grupo_A, grupo_B, nome_grupo1="≤ 2h Netflix", nome_grupo2="> 2h Netflix")
        
        return html.Div([
            # Gráfico de Consumo de Mídias Socias
            html.Div([
                html.Div([
                    html.H1(f"Consumo de Mídias Socias (em horas) por Pessoa ({faixa_min}-{faixa_max})", style={'margin': '0'}),
                    html.P(f"Média: {valor1['média']:.2f}", style={'margin': '10px 0 0 0'}),
                    html.P(f"Moda: {valor1['moda']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Mediana : {valor1['mediana']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Desvio Padrão: {valor1['desvio_padrão']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q1 (25%): {valor1['Q1 (25%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q3 (75%): {valor1['Q3 (75%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"coef_variação (%): {valor1['coef_variação (%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Min): {valor1['Intervalo_min']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Max): {valor1['Intervalo_max']}", style={'margin': '0 0 0 0'}),
                ], style={'display': 'flex', 'textAlign': 'center','flexDirection': 'column'}),
                dcc.Graph(figure=fig1)
            ], style={
                'width': '50%',
                'padding': '10px',
                'boxSizing': 'border-box'
            }),

            # Gráfico de Consumo de Netflix
            
            html.Div([
                html.Div([
                    html.H1(f"Consumo de Netflix (em horas) por Pessoa ({faixa_min}-{faixa_max})", style={'margin': '0'}),
                    html.P(f"Média: {valor2['média']:.2f}", style={'margin': '10px 0 0 0'}),
                    html.P(f"Moda: {valor2['moda']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Mediana : {valor2['mediana']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Desvio Padrão: {valor2['desvio_padrão']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q1 (25%): {valor2['Q1 (25%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q3 (75%): {valor2['Q3 (75%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"coef_variação (%): {valor2['coef_variação (%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Min): {valor1['Intervalo_min']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Max): {valor1['Intervalo_max']}", style={'margin': '0 0 0 0'}),
                ], style={'display': 'flex', 'textAlign': 'center','flexDirection': 'column'}),
                dcc.Graph(figure=fig2)
            ], style={
                'width': '50%',
                'padding': '10px',
                'boxSizing': 'border-box'
            }),
            # Terceiro bloco - gráfico boxplot presença
            html.Div([
                html.Div([
                    html.H1(f"Distribuição do Consumo da Netflix ({faixa_min}-{faixa_max})", style={'margin': '0'}),
                    # Se quiser, pode acrescentar algum texto descritivo aqui
                    html.P("Boxplot do Consumo da Netflix.", style={'margin': '0 0 10px 0', 'textAlign': 'center'}),
                ], style={'display': 'flex', 'textAlign': 'center','flexDirection': 'column'}),
                dcc.Graph(figure=fig3)
            ], style={
                'width': '33%',
                'padding': '10px',
                'boxSizing': 'border-box'
            }),
            html.Div([
                html.H1("Análise: Impacto do Consumo de Mídias Sociais e do Consumo da Netflix nas Notas"),
                teste_html_1,
                teste_html_2
            ], style={
                'width': '100%',
                'padding': '20px',
                'marginTop': '30px',
                'boxSizing': 'border-box',
                'display': 'flex',
                'flexDirection': 'row',
                'flexWrap': 'wrap',
            }),
            
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'flexWrap': 'wrap',
            'alignItems': 'flex-start',
            'justifyContent': 'center'
        })
    

    elif tab == 'tab-3':
        if df_filtrado.empty:
            return html.Div("Nenhum dado disponível na faixa selecionada.")
        # Gráfico 1: Qualidade da dieta por pessoa
        df_count = df_filtrado["diet_quality"].value_counts().reset_index()
        df_count.columns = ["diet_quality", "quantidade"]
        fig1 = px.bar(
            df_count,
            x="diet_quality",
            y="quantidade",
            title=None,
            text="quantidade"
        )
        fig1.update_traces(textposition='outside')
        fig1.update_layout(yaxis_title="Quantidade de Pessoas")

        #Valores da média, moda
        moda_genero = df_filtrado["diet_quality"].mode().iloc[0] if not df_filtrado["diet_quality"].mode().empty else "N/A"
        

        # Gráfico 2: Avaliação de Saúde Mental por Pessoa
        df_count = df_filtrado["mental_health_rating"].value_counts().reset_index()
        df_count.columns = ["mental_health_rating", "quantidade"]
        fig2 = px.bar(
            df_count,
            x="mental_health_rating",
            y="quantidade",
            title=None,
            text="quantidade"
        )
        fig2.update_traces(textposition='outside')
        fig2.update_layout(yaxis_title="Quantidade de Pessoas")

        #Medidas estatísticas - Grafico 2
        valor1 = calcular_estatisticas(df_filtrado["mental_health_rating"])

        # Gráfico 3: Frequência de Exercício por Pessoa
        df_count = df_filtrado["exercise_frequency"].value_counts().reset_index()
        df_count.columns = ["exercise_frequency", "quantidade"]
        fig3 = px.bar(
            df_count,
            x="exercise_frequency",
            y="quantidade",
            title=f"Frequência de Exercício por Pessoa ({faixa_min}-{faixa_max})",
            text="quantidade"
        )
        fig3.update_traces(textposition='outside')
        fig3.update_layout(yaxis_title="Quantidade de Pessoas")

        #Medidas estatísticas - Grafico 3
        valor2 = calcular_estatisticas(df_filtrado["exercise_frequency"])

        # Gráfico 4: Quantidade por gênero
        df_count = df_filtrado["sleep_hours"].value_counts().reset_index()
        df_count.columns = ["sleep_hours", "quantidade"]
        fig4 = px.bar(
            df_count,
            x="sleep_hours",
            y="quantidade",
            title=None,
            text="quantidade"
        )
        fig4.update_traces(textposition='outside')
        fig4.update_layout(yaxis_title="Quantidade de Pessoas")

        #Medidas estatísticas - Grafico 3
        valor3 = calcular_estatisticas(df_filtrado["sleep_hours"])

        # Teste de Hipótese: Comparação de Médias
        grupo_A = df[df["sleep_hours"] <= 6]["exam_score"]
        grupo_B = df[df["sleep_hours"] > 6]["exam_score"]
        teste_html_1 = teste_hipotese_duas_medias(grupo_A, grupo_B, nome_grupo1="≤ 6 Sleep Hours", nome_grupo2="> 6 Sleep Hours")
        
        # Teste de Hipótese: Comparação de Médias
        grupo_A = df[df["exercise_frequency"] <= 2]["exam_score"]
        grupo_B = df[df["exercise_frequency"] > 2]["exam_score"]
        teste_html_2 = teste_hipotese_duas_medias(grupo_A, grupo_B, nome_grupo1="≤ 2 Exercise Frequency", nome_grupo2="> 2 Exercise Frequency")

        return html.Div([
            # Gráfico de Qualidade da dieta
            html.Div([
                html.Div([
                    html.H1(f"Qualidade da dieta por pessoa ({faixa_min}-{faixa_max})", style={'margin': '0'}),
                    html.P(f"Qualidade de dieta (maior frequência): {moda_genero}", style={'margin': '0'}),
                ], style={'display': 'flex', 'textAlign': 'center','flexDirection': 'column'}),
                dcc.Graph(figure=fig1)
            ], style={
                'width': '50%',
                'padding': '10px',
                'boxSizing': 'border-box'
            }),

            # Gráfico de Avaliação de Saúde Mental
            html.Div([
                html.Div([
                    html.H1(f"Avaliação de Saúde Mental por Pessoa ({faixa_min}-{faixa_max})", style={'margin': '0'}),
                    html.P(f"Média: {valor1['média']:.2f}", style={'margin': '10px 0 0 0'}),
                    html.P(f"Moda: {valor1['moda']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Mediana : {valor1['mediana']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Desvio Padrão: {valor1['desvio_padrão']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q1 (25%): {valor1['Q1 (25%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q3 (75%): {valor1['Q3 (75%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"coef_variação (%): {valor1['coef_variação (%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Min): {valor1['Intervalo_min']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Max): {valor1['Intervalo_max']}", style={'margin': '0 0 0 0'}),
                ], style={'display': 'flex', 'textAlign': 'center','flexDirection': 'column'}),
                dcc.Graph(figure=fig2)
            ], style={
                'width': '50%',
                'padding': '10px',
                'boxSizing': 'border-box'
            }),

            # Gráfico de Frequência de Exercício
            
            html.Div([
                html.Div([
                    html.H1(f"Frequência de Exercício por Pessoa ({faixa_min}-{faixa_max})", style={'margin': '0'}),
                    html.P(f"Média: {valor2['média']:.2f}", style={'margin': '10px 0 0 0'}),
                    html.P(f"Moda: {valor2['moda']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Mediana : {valor2['mediana']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Desvio Padrão: {valor2['desvio_padrão']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q1 (25%): {valor2['Q1 (25%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q3 (75%): {valor2['Q3 (75%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"coef_variação (%): {valor2['coef_variação (%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Min): {valor1['Intervalo_min']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Max): {valor1['Intervalo_max']}", style={'margin': '0 0 0 0'}),
                ], style={'display': 'flex', 'textAlign': 'center','flexDirection': 'column'}),
                
                dcc.Graph(figure=fig3)
            ], style={
                'width': '50%',
                'padding': '10px',
                'boxSizing': 'border-box'
            }),

            html.Div([
                html.Div([
                    html.H1(f"Frenquência de Horas Dormidas por Pessoa ({faixa_min}-{faixa_max})", style={'margin': '0'}),
                    html.P(f"Média: {valor3['média']:.2f}", style={'margin': '10px 0 0 0'}),
                    html.P(f"Moda: {valor3['moda']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Mediana : {valor3['mediana']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Desvio Padrão: {valor3['desvio_padrão']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q1 (25%): {valor3['Q1 (25%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Q3 (75%): {valor3['Q3 (75%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"coef_variação (%): {valor3['coef_variação (%)']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Min): {valor1['Intervalo_min']}", style={'margin': '0 0 0 0'}),
                    html.P(f"Intervalo de Confiança (Max): {valor1['Intervalo_max']}", style={'margin': '0 0 0 0'}),
                ], style={'display': 'flex', 'textAlign': 'center','flexDirection': 'column'}),
                
                dcc.Graph(figure=fig4)
            ], style={
                'width': '50%',
                'padding': '10px',
                'boxSizing': 'border-box'
            }),
            html.Div([
                html.H1("Análise: Impacto do Exercício por Pessoa e Avaliação de Saúde Mental nas Notas"),
                teste_html_1,
                teste_html_2
            ], style={
                'width': '100%',
                'padding': '20px',
                'marginTop': '30px',
                'boxSizing': 'border-box',
                'display': 'flex',
                'flexDirection': 'row',
                'flexWrap': 'wrap',
            }),
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'flexWrap': 'wrap',
            'alignItems': 'flex-start',
            'justifyContent': 'center'
        })
    

if __name__ == '__main__':
    app.run(debug=True)