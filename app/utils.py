"""
Funcoes auxiliares para o Market Tracker
"""

import pandas as pd
import os
from datetime import datetime


def ensure_data_files():
    """Garante que os arquivos CSV existem"""

    # Market tracking
    market_file = "data/market_tracking.csv"
    if not os.path.exists(market_file):
        columns = [
            'date', 'time',
            'dxy', 'dxy_chg', 'vix', 'vix_chg', 'sp500_fut', 'sp500_chg',
            'iron_ore', 'iron_ore_chg', 'brent', 'brent_chg', 'wti', 'wti_chg',
            'usd_ars', 'usd_ars_chg', 'usd_aud', 'usd_aud_chg', 'usd_clp', 'usd_clp_chg',
            'usd_mxn', 'usd_mxn_chg', 'usd_inr', 'usd_inr_chg', 'usd_try', 'usd_try_chg', 'usd_zar', 'usd_zar_chg',
            'us_2y', 'us_2y_chg', 'us_10y', 'us_10y_chg',
            'cds_br_5y', 'cds_br_chg',
            'brl_fut_prev_settle', 'brl_fut_prev_high', 'brl_fut_prev_low', 'brl_fut_prev_poc',
            'ewz', 'ewz_chg', 'eww', 'eww_chg', 'tur', 'tur_chg', 'emb', 'emb_chg',
            'vale', 'vale_chg', 'pbr_a', 'pbr_chg', 'itub', 'itub_chg', 'bbdo', 'bbdo_chg',
            'notes'
        ]
        df = pd.DataFrame(columns=columns)
        df.to_csv(market_file, index=False)

    # Economic events
    events_file = "data/economic_events.csv"
    if not os.path.exists(events_file):
        columns = [
            'date', 'time', 'category', 'indicator', 'forecast', 'previous', 'actual', 'impact', 'notes'
        ]
        df = pd.DataFrame(columns=columns)
        df.to_csv(events_file, index=False)


def load_market_data():
    """Carrega dados de mercado"""
    ensure_data_files()
    df = pd.read_csv("data/market_tracking.csv")
    if len(df) > 0:
        df['date'] = pd.to_datetime(df['date'])
    return df


def load_events_data():
    """Carrega dados de eventos economicos"""
    ensure_data_files()
    df = pd.read_csv("data/economic_events.csv")
    if len(df) > 0:
        df['date'] = pd.to_datetime(df['date'])
    return df


def save_market_data(data_dict):
    """Salva novo registro de dados de mercado"""
    df = load_market_data()

    # Verifica se ja existe registro para essa data
    existing = df[df['date'] == data_dict['date']]

    if len(existing) > 0:
        # Atualiza registro existente
        for key, value in data_dict.items():
            df.loc[df['date'] == data_dict['date'], key] = value
        action = "atualizado"
    else:
        # Adiciona novo registro
        new_row = pd.DataFrame([data_dict])
        df = pd.concat([df, new_row], ignore_index=True)
        action = "adicionado"

    # Ordena por data
    df = df.sort_values('date', ascending=False)
    df.to_csv("data/market_tracking.csv", index=False)

    return action


def save_event_data(data_dict):
    """Salva ou atualiza evento economico"""
    df = load_events_data()

    # Verifica se já existe evento com mesma data + indicador
    existing = df[
        (df['date'] == data_dict['date']) &
        (df['indicator'] == data_dict['indicator'])
    ]

    if len(existing) > 0:
        # Atualiza registro existente
        for key, value in data_dict.items():
            df.loc[
                (df['date'] == data_dict['date']) &
                (df['indicator'] == data_dict['indicator']),
                key
            ] = value
        action = "atualizado"
    else:
        # Adiciona novo registro
        new_row = pd.DataFrame([data_dict])
        df = pd.concat([df, new_row], ignore_index=True)
        action = "adicionado"

    # Ordena por data
    df = df.sort_values('date', ascending=False)
    df.to_csv("data/economic_events.csv", index=False)

    return action
