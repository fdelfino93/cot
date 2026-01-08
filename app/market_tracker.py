"""
Market Tracker - Sistema de Tracking Diario de Ativos
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import plotly.graph_objects as go
import sys
import os
import time as time_module

# Adiciona o diretorio pai ao path para importar utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.utils import load_market_data, load_events_data, save_market_data, save_event_data, ensure_data_files


# Funcao para normalizar numeros com virgula
def normalize_number(value):
    """Converte vírgula para ponto e retorna float ou None"""
    if value is None:
        return None
    if isinstance(value, str):
        # Remove espaços e troca vírgula por ponto
        value = value.strip().replace(',', '.')
        try:
            return float(value) if value else None
        except ValueError:
            return None
    return value


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
        dxy = st.text_input("DXY - Valor", value="", key="dxy_val")
    with col2:
        dxy_chg = st.text_input("DXY - Var %", value="", key="dxy_chg", help="Variação % vs fechamento anterior")

    col1, col2 = st.columns(2)
    with col1:
        vix = st.text_input("VIX - Valor", value="", key="vix_val")
    with col2:
        vix_chg = st.text_input("VIX - Var %", value="", key="vix_chg")

    col1, col2 = st.columns(2)
    with col1:
        sp500_fut = st.text_input("S&P 500 Fut - Valor", value="", key="sp500_val")
    with col2:
        sp500_chg = st.text_input("S&P 500 Fut - Var %", value="", key="sp500_chg")

    st.subheader("🛢️ Commodities")
    col1, col2 = st.columns(2)
    with col1:
        iron_ore = st.text_input("Minério Ferro - Valor (USD/ton)", value="", key="iron_val")
    with col2:
        iron_ore_chg = st.text_input("Minério Ferro - Var %", value="", key="iron_chg")

    col1, col2 = st.columns(2)
    with col1:
        brent = st.text_input("Brent - Valor (USD/bbl)", value="", key="brent_val")
    with col2:
        brent_chg = st.text_input("Brent - Var %", value="", key="brent_chg")

    col1, col2 = st.columns(2)
    with col1:
        wti = st.text_input("WTI - Valor (USD/bbl)", value="", key="wti_val")
    with col2:
        wti_chg = st.text_input("WTI - Var %", value="", key="wti_chg")

    st.subheader("💱 Pares de Moeda (USD/XXX)")

    # USD/ARS
    col1, col2 = st.columns(2)
    with col1:
        usd_ars = st.text_input("USD/ARS - Valor", value="", key="ars_val")
    with col2:
        usd_ars_chg = st.text_input("USD/ARS - Var %", value="", key="ars_chg")

    # USD/AUD
    col1, col2 = st.columns(2)
    with col1:
        usd_aud = st.text_input("USD/AUD - Valor", value="", key="aud_val")
    with col2:
        usd_aud_chg = st.text_input("USD/AUD - Var %", value="", key="aud_chg")

    # USD/CLP
    col1, col2 = st.columns(2)
    with col1:
        usd_clp = st.text_input("USD/CLP - Valor", value="", key="clp_val")
    with col2:
        usd_clp_chg = st.text_input("USD/CLP - Var %", value="", key="clp_chg")

    # USD/MXN
    col1, col2 = st.columns(2)
    with col1:
        usd_mxn = st.text_input("USD/MXN - Valor", value="", key="mxn_val")
    with col2:
        usd_mxn_chg = st.text_input("USD/MXN - Var %", value="", key="mxn_chg")

    # USD/INR
    col1, col2 = st.columns(2)
    with col1:
        usd_inr = st.text_input("USD/INR - Valor", value="", key="inr_val")
    with col2:
        usd_inr_chg = st.text_input("USD/INR - Var %", value="", key="inr_chg")

    # USD/TRY
    col1, col2 = st.columns(2)
    with col1:
        usd_try = st.text_input("USD/TRY - Valor", value="", key="try_val")
    with col2:
        usd_try_chg = st.text_input("USD/TRY - Var %", value="", key="try_chg")

    # USD/ZAR
    col1, col2 = st.columns(2)
    with col1:
        usd_zar = st.text_input("USD/ZAR - Valor", value="", key="zar_val")
    with col2:
        usd_zar_chg = st.text_input("USD/ZAR - Var %", value="", key="zar_chg")

    st.subheader("💵 Treasuries")
    col1, col2 = st.columns(2)
    with col1:
        us_2y = st.text_input("U.S. 2Y - Yield (%)", value="", key="us2y_val")
    with col2:
        us_2y_chg = st.text_input("U.S. 2Y - Var (bps)", value="", key="us2y_chg", help="Variação em basis points")

    col1, col2 = st.columns(2)
    with col1:
        us_10y = st.text_input("U.S. 10Y - Yield (%)", value="", key="us10y_val")
    with col2:
        us_10y_chg = st.text_input("U.S. 10Y - Var (bps)", value="", key="us10y_chg", help="Variação em basis points")

    st.subheader("🇧🇷 Risco Brasil")
    col1, col2 = st.columns(2)
    with col1:
        cds_br_5y = st.text_input("CDS BR 5Y - Valor (bps)", value="", key="cds_val")
    with col2:
        cds_br_chg = st.text_input("CDS BR 5Y - Var %", value="", key="cds_chg")

    st.subheader("📈 BRL Futures (CME) - Pregão Anterior")
    st.caption("Preencha ANTES do mercado abrir com os dados do dia anterior (para referência)")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        brl_fut_prev_settle = st.text_input("Ajuste Anterior", value="", key="brl_prev_settle", help="Settlement do dia anterior")
    with col2:
        brl_fut_prev_high = st.text_input("Máxima Anterior", value="", key="brl_prev_high")
    with col3:
        brl_fut_prev_low = st.text_input("Mínima Anterior", value="", key="brl_prev_low")
    with col4:
        brl_fut_prev_poc = st.text_input("POC Anterior", value="", key="brl_prev_poc", help="Point of Control do dia anterior")

    st.subheader("📊 ETFs - Países/Emergentes")

    # EWZ
    col1, col2 = st.columns(2)
    with col1:
        ewz = st.text_input("EWZ - Valor", value="", key="ewz_val")
    with col2:
        ewz_chg = st.text_input("EWZ - Var %", value="", key="ewz_chg")

    # EWW
    col1, col2 = st.columns(2)
    with col1:
        eww = st.text_input("EWW - Valor", value="", key="eww_val")
    with col2:
        eww_chg = st.text_input("EWW - Var %", value="", key="eww_chg")

    # TUR
    col1, col2 = st.columns(2)
    with col1:
        tur = st.text_input("TUR - Valor", value="", key="tur_val")
    with col2:
        tur_chg = st.text_input("TUR - Var %", value="", key="tur_chg")

    # EMB
    col1, col2 = st.columns(2)
    with col1:
        emb = st.text_input("EMB - Valor", value="", key="emb_val")
    with col2:
        emb_chg = st.text_input("EMB - Var %", value="", key="emb_chg")

    st.subheader("🏢 ADRs Brasileiras (NYSE)")
    col1, col2 = st.columns(2)
    with col1:
        vale = st.text_input("VALE - Valor", value="", key="vale_val")
    with col2:
        vale_chg = st.text_input("VALE - Var %", value="", key="vale_chg")

    col1, col2 = st.columns(2)
    with col1:
        pbr_a = st.text_input("PBR-A - Valor", value="", key="pbr_val")
    with col2:
        pbr_chg = st.text_input("PBR-A - Var %", value="", key="pbr_chg")

    col1, col2 = st.columns(2)
    with col1:
        itub = st.text_input("ITUB - Valor", value="", key="itub_val")
    with col2:
        itub_chg = st.text_input("ITUB - Var %", value="", key="itub_chg")

    col1, col2 = st.columns(2)
    with col1:
        bbdo = st.text_input("BBDO - Valor", value="", key="bbdo_val", help="Bradesco ADR (NYSE)")
    with col2:
        bbdo_chg = st.text_input("BBDO - Var %", value="", key="bbdo_chg")

    st.subheader("📝 Observações")
    notes = st.text_area("Notas (opcional)", placeholder="Ex: Dia de volatilidade alta, Fed spoke, etc.")

    # Botao salvar
    if st.button("💾 Salvar Registro", type="primary", use_container_width=True):
        # Monta dicionario (normaliza todos os valores numéricos)
        data_dict = {
            'date': str(input_date),
            'time': str(input_time),
            'dxy': normalize_number(dxy), 'dxy_chg': normalize_number(dxy_chg),
            'vix': normalize_number(vix), 'vix_chg': normalize_number(vix_chg),
            'sp500_fut': normalize_number(sp500_fut), 'sp500_chg': normalize_number(sp500_chg),
            'iron_ore': normalize_number(iron_ore), 'iron_ore_chg': normalize_number(iron_ore_chg),
            'brent': normalize_number(brent), 'brent_chg': normalize_number(brent_chg),
            'wti': normalize_number(wti), 'wti_chg': normalize_number(wti_chg),
            'usd_ars': normalize_number(usd_ars), 'usd_ars_chg': normalize_number(usd_ars_chg),
            'usd_aud': normalize_number(usd_aud), 'usd_aud_chg': normalize_number(usd_aud_chg),
            'usd_clp': normalize_number(usd_clp), 'usd_clp_chg': normalize_number(usd_clp_chg),
            'usd_mxn': normalize_number(usd_mxn), 'usd_mxn_chg': normalize_number(usd_mxn_chg),
            'usd_inr': normalize_number(usd_inr), 'usd_inr_chg': normalize_number(usd_inr_chg),
            'usd_try': normalize_number(usd_try), 'usd_try_chg': normalize_number(usd_try_chg),
            'usd_zar': normalize_number(usd_zar), 'usd_zar_chg': normalize_number(usd_zar_chg),
            'us_2y': normalize_number(us_2y), 'us_2y_chg': normalize_number(us_2y_chg),
            'us_10y': normalize_number(us_10y), 'us_10y_chg': normalize_number(us_10y_chg),
            'cds_br_5y': normalize_number(cds_br_5y), 'cds_br_chg': normalize_number(cds_br_chg),
            'brl_fut_prev_settle': normalize_number(brl_fut_prev_settle),
            'brl_fut_prev_high': normalize_number(brl_fut_prev_high),
            'brl_fut_prev_low': normalize_number(brl_fut_prev_low),
            'brl_fut_prev_poc': normalize_number(brl_fut_prev_poc),
            'ewz': normalize_number(ewz), 'ewz_chg': normalize_number(ewz_chg),
            'eww': normalize_number(eww), 'eww_chg': normalize_number(eww_chg),
            'tur': normalize_number(tur), 'tur_chg': normalize_number(tur_chg),
            'emb': normalize_number(emb), 'emb_chg': normalize_number(emb_chg),
            'vale': normalize_number(vale), 'vale_chg': normalize_number(vale_chg),
            'pbr_a': normalize_number(pbr_a), 'pbr_chg': normalize_number(pbr_chg),
            'itub': normalize_number(itub), 'itub_chg': normalize_number(itub_chg),
            'bbdo': normalize_number(bbdo), 'bbdo_chg': normalize_number(bbdo_chg),
            'notes': notes
        }

        action = save_market_data(data_dict)
        st.success(f"✅ Registro {action} com sucesso para {input_date}!", icon="✅")
        st.balloons()
        time_module.sleep(2)  # Pausa para mostrar mensagem
        st.rerun()

# ===== TAB 2: EVENTOS ECONOMICOS =====
with tab2:
    st.header("📰 Eventos Econômicos")

    # Adicionar novo evento
    st.subheader("Adicionar Novo Evento")

    col1, col2 = st.columns(2)
    with col1:
        event_date = st.date_input("Data", value=date.today(), max_value=date.today(), key="event_date")
    with col2:
        event_time = st.time_input("Hora (opcional)", value=None, key="event_time")

    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox(
            "Categoria",
            ["Inflação", "Focus", "Fiscal", "Emprego", "Político", "Monetário", "PIB", "Produção", "Outro"]
        )
    with col2:
        indicator = st.text_input("Indicador", placeholder="Ex: IPCA-15, Payroll, Selic, PIM-PF")

    col1, col2, col3 = st.columns(3)
    with col1:
        forecast = st.text_input("Expectativa", placeholder="Ex: 0,42%")
    with col2:
        previous = st.text_input("Anterior", placeholder="Ex: 0,62%")
    with col3:
        actual = st.text_input("Real", placeholder="Ex: 0,48%")

    impact = st.select_slider("Impacto", options=["Baixo", "Médio", "Alto"])
    event_notes = st.text_area("Observações", placeholder="Ex: Veio acima do esperado", key="event_notes")

    if st.button("➕ Adicionar Evento", type="primary"):
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
        st.success("✅ Evento adicionado!", icon="✅")
        st.balloons()
        time_module.sleep(1)
        st.rerun()

    # Tabela editável de eventos
    st.markdown("---")
    st.subheader("📋 Eventos Cadastrados - Clique para Editar")

    events_df = load_events_data()

    if len(events_df) > 0:
        # Formatar data para exibição
        display_df = events_df.copy()
        display_df['date'] = pd.to_datetime(display_df['date']).dt.strftime('%d/%m/%Y')

        # Editor de dados
        edited_df = st.data_editor(
            display_df,
            use_container_width=True,
            height=400,
            num_rows="dynamic",
            column_config={
                "date": st.column_config.TextColumn("Data", help="dd/mm/aaaa", width="small"),
                "time": st.column_config.TextColumn("Hora", width="small"),
                "category": st.column_config.SelectboxColumn("Categoria", options=["Inflação", "Focus", "Fiscal", "Emprego", "Político", "Monetário", "PIB", "Produção", "Outro"], width="small"),
                "indicator": st.column_config.TextColumn("Indicador", width="medium"),
                "forecast": st.column_config.TextColumn("Expectativa", width="small"),
                "previous": st.column_config.TextColumn("Anterior", width="small"),
                "actual": st.column_config.TextColumn("Real", width="small"),
                "impact": st.column_config.SelectboxColumn("Impacto", options=["Baixo", "Médio", "Alto"], width="small"),
                "notes": st.column_config.TextColumn("Observações", width="large")
            },
            hide_index=True
        )

        # Botão para salvar mudanças
        if st.button("💾 Salvar Alterações da Tabela", type="secondary"):
            # Converter data de volta para formato ISO
            edited_df['date'] = pd.to_datetime(edited_df['date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
            edited_df.to_csv("data/economic_events.csv", index=False)
            st.success("✅ Alterações salvas!", icon="✅")
            time_module.sleep(1)
            st.rerun()
    else:
        st.info("Nenhum evento cadastrado ainda.")

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
        # Formatar data para exibição brasileira
        display_df = df.copy()
        display_df['date'] = pd.to_datetime(display_df['date']).dt.strftime('%d/%m/%Y')
        st.dataframe(display_df, use_container_width=True, height=400)

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
