import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def load_stocks():
    try:
        df = pd.read_csv('acoes.csv')
        print(f"[INFO] CSV carregado: {len(df)} acoes")
        print(df)
        return df
    except Exception as e:
        print(f"[ERRO] ao carregar acoes.csv: {e}")
        return pd.DataFrame(columns=['ticker', 'shares'])

def get_stock_data(ticker):
    try:
        print(f"[INFO] Buscando dados para {ticker}...")
        stock = yf.Ticker(ticker)

        # Buscar historico de 5 dias para garantir dados
        hist = stock.history(period='5d')

        if hist.empty:
            print(f"[AVISO] Historico vazio para {ticker}")
            return None

        print(f"[INFO] Historico obtido para {ticker}: {len(hist)} dias")

        current_price = hist['Close'].iloc[-1]

        # Calcular variacao percentual baseado no dia anterior
        if len(hist) >= 2:
            prev_close = hist['Close'].iloc[-2]
            change_pct = ((current_price - prev_close) / prev_close) * 100
        else:
            change_pct = 0

        print(f"[INFO] {ticker}: Preco=R$ {current_price:.2f}, Variacao={change_pct:.2f}%")

        # Tentar buscar info adicional (pode falhar sem problema)
        try:
            info = stock.info
            sector = info.get('sector', 'Outros')
            longName = info.get('longName', ticker)
        except:
            sector = 'Outros'
            longName = ticker

        return {
            'ticker': ticker.replace('.SA', ''),
            'price': current_price,
            'change_pct': change_pct,
            'sector': sector,
            'longName': longName
        }
    except Exception as e:
        print(f"[ERRO] ao buscar {ticker}: {e}")
        return None

def create_alerts(df):
    alerts = []

    # Alertas de ganho acima de 10%
    high_gains = df[df['change_pct'] >= 10.0]
    for _, row in high_gains.iterrows():
        alerts.append(
            dbc.Alert(
                [
                    html.I(className="bi bi-graph-up-arrow me-2"),
                    html.Strong(f"{row['ticker']}: "),
                    f"Ganho de {row['change_pct']:+.2f}% - Considere realizar lucro"
                ],
                color="info",
                duration=15000,  # Some apos 15 segundos
                dismissable=True,
                className="mb-2"
            )
        )

    # Alertas de ganho entre 5% e 10%
    medium_gains = df[(df['change_pct'] >= 5.0) & (df['change_pct'] < 10.0)]
    for _, row in medium_gains.iterrows():
        alerts.append(
            dbc.Alert(
                [
                    html.I(className="bi bi-arrow-up-circle me-2"),
                    html.Strong(f"{row['ticker']}: "),
                    f"Alta de {row['change_pct']:+.2f}%"
                ],
                color="success",
                duration=15000,
                dismissable=True,
                className="mb-2"
            )
        )

    # Alertas de perda acima de 5%
    high_losses = df[df['change_pct'] <= -5.0]
    for _, row in high_losses.iterrows():
        alerts.append(
            dbc.Alert(
                [
                    html.I(className="bi bi-exclamation-triangle me-2"),
                    html.Strong(f"{row['ticker']}: "),
                    f"Queda de {row['change_pct']:.2f}% - Acompanhe de perto"
                ],
                color="warning",
                duration=15000,
                dismissable=True,
                className="mb-2"
            )
        )

    # Alertas de perda acima de 10%
    extreme_losses = df[df['change_pct'] <= -10.0]
    for _, row in extreme_losses.iterrows():
        alerts.append(
            dbc.Alert(
                [
                    html.I(className="bi bi-graph-down-arrow me-2"),
                    html.Strong(f"{row['ticker']}: "),
                    f"ALERTA! Queda de {row['change_pct']:.2f}%"
                ],
                color="danger",
                duration=15000,
                dismissable=True,
                className="mb-2"
            )
        )

    return alerts

def create_treemap():
    print(f"\n[INFO] Iniciando criacao do treemap - {datetime.now().strftime('%H:%M:%S')}")
    stocks_df = load_stocks()

    if stocks_df.empty:
        print("[ERRO] DataFrame vazio!")
        return go.Figure().update_layout(title="Erro: Nenhuma acao carregada"), []

    data_list = []
    for _, row in stocks_df.iterrows():
        ticker = row['ticker']
        shares = row['shares']

        stock_data = get_stock_data(ticker)
        if stock_data:
            stock_data['shares'] = shares
            stock_data['value'] = stock_data['price'] * shares
            data_list.append(stock_data)
            print(f"[OK] {ticker}: Valor total = R$ {stock_data['value']:.2f}")

    if not data_list:
        print("[ERRO] Nenhum dado obtido!")
        return go.Figure().update_layout(title="Erro: Falha ao buscar dados das acoes"), []

    df = pd.DataFrame(data_list)
    print(f"\n[INFO] DataFrame final com {len(df)} acoes:")
    print(df[['ticker', 'price', 'change_pct', 'value']])

    # Criar alertas baseado nas variacoes
    alerts = create_alerts(df)

    # Criar treemap SEM hierarquia - apenas acoes
    fig = go.Figure(go.Treemap(
        labels=df['ticker'],
        parents=[''] * len(df),
        values=df['value'],
        text=df.apply(lambda x: f"<b>{x['ticker']}</b><br>{x['change_pct']:+.2f}%<br>R$ {x['price']:.2f}", axis=1),
        textposition='middle center',
        textfont=dict(size=16, color='white', family='Arial Black'),
        marker=dict(
            colors=df['change_pct'],
            colorscale=[
                [0.0, '#D32F2F'],  # Vermelho escuro
                [0.4, '#FF5252'],  # Vermelho claro
                [0.5, '#FFFFFF'],  # Branco (zero)
                [0.6, '#66BB6A'],  # Verde claro
                [1.0, '#2E7D32']   # Verde escuro
            ],
            cmid=0,
            colorbar=dict(
                title="Variacao %",
                ticksuffix="%",
                x=1.02,
                thickness=20,
                len=0.7
            ),
            line=dict(width=3, color='#333333')
        ),
        hovertemplate='<b>%{label}</b><br>Variacao: %{color:+.2f}%<br>Valor: R$ %{value:,.2f}<br><extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text=f'Mapa de Acoes - {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
            x=0.5,
            xanchor='center',
            font=dict(size=28, family='Arial', color='#2c3e50')
        ),
        margin=dict(t=80, l=10, r=120, b=10),
        height=750,
        paper_bgcolor='#ecf0f1'
    )

    print(f"[INFO] Treemap criado com sucesso!\n")
    return fig, alerts

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Mapa de Acoes - Treemap', className='text-center my-4'),
            html.P('Atualizacao automatica a cada 5 minutos', className='text-center text-muted'),
            html.Div(id='alerts-container'),  # Container para alertas
            dcc.Graph(id='treemap-graph', style={'border': '1px solid #ddd', 'border-radius': '5px'}),
            dcc.Interval(
                id='interval-component',
                interval=5*60*1000,  # 5 minutos
                n_intervals=0
            )
        ])
    ])
], fluid=True, style={'padding': '20px'})

@app.callback(
    [Output('treemap-graph', 'figure'),
     Output('alerts-container', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    print(f"\n{'='*80}")
    print(f"[INFO] Callback acionado - Intervalo #{n}")
    print('='*80)
    fig, alerts = create_treemap()
    return fig, alerts

if __name__ == '__main__':
    print("\n" + "="*80)
    print("Iniciando Mapa de Acoes - Treemap")
    print("="*80 + "\n")
    app.run_server(host='0.0.0.0', port=8050, debug=True)
