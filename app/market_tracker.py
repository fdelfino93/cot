"""
Market Tracker - Sistema de Tracking Diario de Ativos
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import plotly.graph_objects as go
import sys
import os

# Adiciona o diretorio pai ao path para importar utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.utils import load_market_data, load_events_data, save_market_data, save_event_data, ensure_data_files


# Configuracao da pagina
st.set_page_config(
    page_title="Market Tracker",
    page_icon="📊",
    layout="wide"
)

# Inicializa arquivos
ensure_data_files()

# Titulo principal
st.title("📊 Market Tracker - Dados Diários")
st.markdown("**Sistema de tracking de ativos financeiros globais**")

# Tabs principais
tab1, tab2, tab3, tab4 = st.tabs(["📈 Novo Registro", "📰 Eventos Econômicos", "📊 Visualizações", "📋 Dados"])

# ===== TAB 1: NOVO REGISTRO DE MERCADO =====
with tab1:
    st.header("Novo Registro de Mercado")

    st.info("ℹ️ **Preencha com valores absolutos** (preços, yields, índices). As variações percentuais serão calculadas automaticamente depois.")

    col1, col2 = st.columns(2)

    with col1:
        input_date = st.date_input("Data", value=date.today(), max_value=date.today())
    with col2:
        input_time = st.time_input("Hora", value=datetime.now().time(), help="Editável - ajuste se necessário")

    # Dividir em secoes
    st.subheader("📉 Índices e Volatilidade")
    col1, col2 = st.columns(2)
    with col1:
        dxy = st.number_input("DXY - Valor", value=None, format="%.2f", step=0.01, key="dxy_val")
    with col2:
        dxy_chg = st.number_input("DXY - Var %", value=None, format="%.2f", step=0.01, key="dxy_chg", help="Variação % vs fechamento anterior")

    col1, col2 = st.columns(2)
    with col1:
        vix = st.number_input("VIX - Valor", value=None, format="%.2f", step=0.01, key="vix_val")
    with col2:
        vix_chg = st.number_input("VIX - Var %", value=None, format="%.2f", step=0.01, key="vix_chg")

    col1, col2 = st.columns(2)
    with col1:
        sp500_fut = st.number_input("S&P 500 Fut - Valor", value=None, format="%.2f", step=0.01, key="sp500_val")
    with col2:
        sp500_chg = st.number_input("S&P 500 Fut - Var %", value=None, format="%.2f", step=0.01, key="sp500_chg")

    st.subheader("🛢️ Commodities")
    col1, col2 = st.columns(2)
    with col1:
        iron_ore = st.number_input("Minério Ferro - Valor (USD/ton)", value=None, format="%.2f", step=0.01, key="iron_val")
    with col2:
        iron_ore_chg = st.number_input("Minério Ferro - Var %", value=None, format="%.2f", step=0.01, key="iron_chg")

    col1, col2 = st.columns(2)
    with col1:
        brent = st.number_input("Brent - Valor (USD/bbl)", value=None, format="%.2f", step=0.01, key="brent_val")
    with col2:
        brent_chg = st.number_input("Brent - Var %", value=None, format="%.2f", step=0.01, key="brent_chg")

    col1, col2 = st.columns(2)
    with col1:
        wti = st.number_input("WTI - Valor (USD/bbl)", value=None, format="%.2f", step=0.01, key="wti_val")
    with col2:
        wti_chg = st.number_input("WTI - Var %", value=None, format="%.2f", step=0.01, key="wti_chg")

    st.subheader("💱 Pares de Moeda (USD/XXX)")

    # USD/ARS
    col1, col2 = st.columns(2)
    with col1:
        usd_ars = st.number_input("USD/ARS - Valor", value=None, format="%.2f", step=0.01, key="ars_val")
    with col2:
        usd_ars_chg = st.number_input("USD/ARS - Var %", value=None, format="%.2f", step=0.01, key="ars_chg")

    # USD/AUD
    col1, col2 = st.columns(2)
    with col1:
        usd_aud = st.number_input("USD/AUD - Valor", value=None, format="%.4f", step=0.0001, key="aud_val")
    with col2:
        usd_aud_chg = st.number_input("USD/AUD - Var %", value=None, format="%.2f", step=0.01, key="aud_chg")

    # USD/CLP
    col1, col2 = st.columns(2)
    with col1:
        usd_clp = st.number_input("USD/CLP - Valor", value=None, format="%.2f", step=0.01, key="clp_val")
    with col2:
        usd_clp_chg = st.number_input("USD/CLP - Var %", value=None, format="%.2f", step=0.01, key="clp_chg")

    # USD/MXN
    col1, col2 = st.columns(2)
    with col1:
        usd_mxn = st.number_input("USD/MXN - Valor", value=None, format="%.4f", step=0.0001, key="mxn_val")
    with col2:
        usd_mxn_chg = st.number_input("USD/MXN - Var %", value=None, format="%.2f", step=0.01, key="mxn_chg")

    # USD/INR
    col1, col2 = st.columns(2)
    with col1:
        usd_inr = st.number_input("USD/INR - Valor", value=None, format="%.2f", step=0.01, key="inr_val")
    with col2:
        usd_inr_chg = st.number_input("USD/INR - Var %", value=None, format="%.2f", step=0.01, key="inr_chg")

    # USD/TRY
    col1, col2 = st.columns(2)
    with col1:
        usd_try = st.number_input("USD/TRY - Valor", value=None, format="%.2f", step=0.01, key="try_val")
    with col2:
        usd_try_chg = st.number_input("USD/TRY - Var %", value=None, format="%.2f", step=0.01, key="try_chg")

    # USD/ZAR
    col1, col2 = st.columns(2)
    with col1:
        usd_zar = st.number_input("USD/ZAR - Valor", value=None, format="%.2f", step=0.01, key="zar_val")
    with col2:
        usd_zar_chg = st.number_input("USD/ZAR - Var %", value=None, format="%.2f", step=0.01, key="zar_chg")

    st.subheader("💵 Treasuries")
    col1, col2 = st.columns(2)
    with col1:
        us_2y = st.number_input("U.S. 2Y - Yield (%)", value=None, format="%.3f", step=0.001, key="us2y_val")
    with col2:
        us_2y_chg = st.number_input("U.S. 2Y - Var (bps)", value=None, format="%.1f", step=0.1, key="us2y_chg", help="Variação em basis points")

    col1, col2 = st.columns(2)
    with col1:
        us_10y = st.number_input("U.S. 10Y - Yield (%)", value=None, format="%.3f", step=0.001, key="us10y_val")
    with col2:
        us_10y_chg = st.number_input("U.S. 10Y - Var (bps)", value=None, format="%.1f", step=0.1, key="us10y_chg", help="Variação em basis points")

    st.subheader("🇧🇷 Risco Brasil")
    col1, col2 = st.columns(2)
    with col1:
        cds_br_5y = st.number_input("CDS BR 5Y - Valor (bps)", value=None, format="%.2f", step=0.01, key="cds_val")
    with col2:
        cds_br_chg = st.number_input("CDS BR 5Y - Var %", value=None, format="%.2f", step=0.01, key="cds_chg")

    st.subheader("📈 BRL Futures (CME)")
    st.caption("Valores absolutos do contrato futuro de Real na bolsa de Chicago")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        brl_fut_open = st.number_input("Abertura", value=None, format="%.4f", step=0.0001, key="brl_open")
    with col2:
        brl_fut_high = st.number_input("Máxima", value=None, format="%.4f", step=0.0001, key="brl_high")
    with col3:
        brl_fut_low = st.number_input("Mínima", value=None, format="%.4f", step=0.0001, key="brl_low")
    with col4:
        brl_fut_last = st.number_input("Atual/Fechamento", value=None, format="%.4f", step=0.0001, key="brl_last")

    st.subheader("📊 ETFs - Países/Emergentes")

    # EWZ
    col1, col2 = st.columns(2)
    with col1:
        ewz = st.number_input("EWZ - Valor", value=None, format="%.2f", step=0.01, key="ewz_val")
    with col2:
        ewz_chg = st.number_input("EWZ - Var %", value=None, format="%.2f", step=0.01, key="ewz_chg")

    # EWW
    col1, col2 = st.columns(2)
    with col1:
        eww = st.number_input("EWW - Valor", value=None, format="%.2f", step=0.01, key="eww_val")
    with col2:
        eww_chg = st.number_input("EWW - Var %", value=None, format="%.2f", step=0.01, key="eww_chg")

    # TUR
    col1, col2 = st.columns(2)
    with col1:
        tur = st.number_input("TUR - Valor", value=None, format="%.2f", step=0.01, key="tur_val")
    with col2:
        tur_chg = st.number_input("TUR - Var %", value=None, format="%.2f", step=0.01, key="tur_chg")

    # EMB
    col1, col2 = st.columns(2)
    with col1:
        emb = st.number_input("EMB - Valor", value=None, format="%.2f", step=0.01, key="emb_val")
    with col2:
        emb_chg = st.number_input("EMB - Var %", value=None, format="%.2f", step=0.01, key="emb_chg")

    st.subheader("🏢 ADRs Brasileiras (NYSE)")
    col1, col2 = st.columns(2)
    with col1:
        vale = st.number_input("VALE - Valor", value=None, format="%.2f", step=0.01, key="vale_val")
    with col2:
        vale_chg = st.number_input("VALE - Var %", value=None, format="%.2f", step=0.01, key="vale_chg")

    col1, col2 = st.columns(2)
    with col1:
        pbr_a = st.number_input("PBR-A - Valor", value=None, format="%.2f", step=0.01, key="pbr_val")
    with col2:
        pbr_chg = st.number_input("PBR-A - Var %", value=None, format="%.2f", step=0.01, key="pbr_chg")

    col1, col2 = st.columns(2)
    with col1:
        itub = st.number_input("ITUB - Valor", value=None, format="%.2f", step=0.01, key="itub_val")
    with col2:
        itub_chg = st.number_input("ITUB - Var %", value=None, format="%.2f", step=0.01, key="itub_chg")

    col1, col2 = st.columns(2)
    with col1:
        bbdc = st.number_input("BBDC - Valor", value=None, format="%.2f", step=0.01, key="bbdc_val")
    with col2:
        bbdc_chg = st.number_input("BBDC - Var %", value=None, format="%.2f", step=0.01, key="bbdc_chg")

    st.subheader("📝 Observações")
    notes = st.text_area("Notas (opcional)", placeholder="Ex: Dia de volatilidade alta, Fed spoke, etc.")

    # Botao salvar
    if st.button("💾 Salvar Registro", type="primary", use_container_width=True):
        # Monta dicionario
        data_dict = {
            'date': str(input_date),
            'time': str(input_time),
            'dxy': dxy, 'dxy_chg': dxy_chg,
            'vix': vix, 'vix_chg': vix_chg,
            'sp500_fut': sp500_fut, 'sp500_chg': sp500_chg,
            'iron_ore': iron_ore, 'iron_ore_chg': iron_ore_chg,
            'brent': brent, 'brent_chg': brent_chg,
            'wti': wti, 'wti_chg': wti_chg,
            'usd_ars': usd_ars, 'usd_ars_chg': usd_ars_chg,
            'usd_aud': usd_aud, 'usd_aud_chg': usd_aud_chg,
            'usd_clp': usd_clp, 'usd_clp_chg': usd_clp_chg,
            'usd_mxn': usd_mxn, 'usd_mxn_chg': usd_mxn_chg,
            'usd_inr': usd_inr, 'usd_inr_chg': usd_inr_chg,
            'usd_try': usd_try, 'usd_try_chg': usd_try_chg,
            'usd_zar': usd_zar, 'usd_zar_chg': usd_zar_chg,
            'us_2y': us_2y, 'us_2y_chg': us_2y_chg,
            'us_10y': us_10y, 'us_10y_chg': us_10y_chg,
            'cds_br_5y': cds_br_5y, 'cds_br_chg': cds_br_chg,
            'brl_fut_open': brl_fut_open,
            'brl_fut_high': brl_fut_high,
            'brl_fut_low': brl_fut_low,
            'brl_fut_last': brl_fut_last,
            'ewz': ewz, 'ewz_chg': ewz_chg,
            'eww': eww, 'eww_chg': eww_chg,
            'tur': tur, 'tur_chg': tur_chg,
            'emb': emb, 'emb_chg': emb_chg,
            'vale': vale, 'vale_chg': vale_chg,
            'pbr_a': pbr_a, 'pbr_chg': pbr_chg,
            'itub': itub, 'itub_chg': itub_chg,
            'bbdc': bbdc, 'bbdc_chg': bbdc_chg,
            'notes': notes
        }

        action = save_market_data(data_dict)
        st.success(f"✅ Registro {action} com sucesso para {input_date}!")
        st.rerun()

# ===== TAB 2: EVENTOS ECONOMICOS =====
with tab2:
    st.header("📰 Registrar Evento Econômico")

    col1, col2 = st.columns(2)
    with col1:
        event_date = st.date_input("Data do Evento", value=date.today(), max_value=date.today(), key="event_date")
    with col2:
        event_time = st.time_input("Hora (opcional)", value=None, key="event_time")

    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox(
            "Categoria",
            ["Inflação", "Focus", "Fiscal", "Emprego", "Político", "Monetário", "PIB", "Outro"]
        )
    with col2:
        indicator = st.text_input("Indicador", placeholder="Ex: IPCA-15, Payroll, Selic")

    col1, col2, col3 = st.columns(3)
    with col1:
        forecast = st.text_input("Expectativa (Forecast)", placeholder="Ex: 0.42%")
    with col2:
        previous = st.text_input("Dado Anterior", placeholder="Ex: 0.62%")
    with col3:
        actual = st.text_input("Dado Real (Actual)", placeholder="Ex: 0.48%")

    impact = st.select_slider("Impacto no Mercado", options=["Baixo", "Médio", "Alto"])

    event_notes = st.text_area("Observações / Contexto", placeholder="Ex: Veio acima do esperado mas abaixo do anterior. Real caiu 0.5%.", key="event_notes")

    if st.button("💾 Salvar Evento", type="primary", use_container_width=True):
        event_dict = {
            'date': str(event_date),
            'time': str(event_time) if event_time else "",
            'category': category,
            'indicator': indicator,
            'forecast': forecast,
            'previous': previous,
            'actual': actual,
            'impact': impact,
            'notes': event_notes
        }

        save_event_data(event_dict)
        st.success(f"✅ Evento registrado com sucesso!")
        st.rerun()

    # Mostra ultimos eventos
    st.markdown("---")
    st.subheader("Últimos Eventos Registrados")
    events_df = load_events_data()
    if len(events_df) > 0:
        st.dataframe(events_df.head(10), use_container_width=True)
    else:
        st.info("Nenhum evento registrado ainda.")

# ===== TAB 3: VISUALIZACOES =====
with tab3:
    st.header("📊 Visualizações")

    df = load_market_data()

    if len(df) == 0:
        st.info("📭 Nenhum dado registrado ainda. Adicione dados na aba 'Novo Registro'.")
    else:
        # Selecionar ativos para plotar
        st.subheader("Selecione os ativos para visualizar")

        available_cols = [col for col in df.columns if col not in ['date', 'time', 'notes']]

        selected_assets = st.multiselect(
            "Ativos",
            available_cols,
            default=['dxy', 'vix'] if 'dxy' in available_cols else available_cols[:2]
        )

        if selected_assets:
            # Cria grafico
            fig = go.Figure()

            for asset in selected_assets:
                fig.add_trace(go.Scatter(
                    x=df['date'],
                    y=df[asset],
                    mode='lines+markers',
                    name=asset.upper()
                ))

            fig.update_layout(
                title="Evolução dos Ativos",
                xaxis_title="Data",
                yaxis_title="Valor",
                hovermode='x unified',
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

        # Estatisticas
        st.subheader("Estatísticas (Últimos 30 dias)")

        if len(df) > 0:
            # Filtra ultimos 30 dias
            df_30d = df.head(min(30, len(df)))

            stats_cols = st.columns(4)

            numeric_cols = df_30d.select_dtypes(include=['float64', 'int64']).columns

            for i, col in enumerate(numeric_cols[:4]):  # Mostra primeiros 4
                with stats_cols[i % 4]:
                    if df_30d[col].notna().any():
                        st.metric(
                            label=col.upper(),
                            value=f"{df_30d[col].iloc[0]:.2f}" if pd.notna(df_30d[col].iloc[0]) else "N/A",
                            delta=f"{df_30d[col].iloc[0] - df_30d[col].mean():.2f} vs média" if pd.notna(df_30d[col].iloc[0]) else None
                        )

# ===== TAB 4: DADOS =====
with tab4:
    st.header("📋 Dados Registrados")

    # Market data
    st.subheader("Dados de Mercado")
    df = load_market_data()

    if len(df) > 0:
        st.dataframe(df, use_container_width=True, height=400)

        # Botao para download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"market_tracking_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("📭 Nenhum dado registrado ainda.")

    st.markdown("---")

    # Events data
    st.subheader("Eventos Econômicos")
    events_df = load_events_data()

    if len(events_df) > 0:
        st.dataframe(events_df, use_container_width=True, height=400)

        csv_events = events_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Eventos CSV",
            data=csv_events,
            file_name=f"economic_events_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="download_events"
        )
    else:
        st.info("📭 Nenhum evento registrado ainda.")
