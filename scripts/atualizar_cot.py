"""
Script para atualizar automaticamente os dados COT

Este script:
1. Baixa o arquivo ZIP mais recente da CFTC
2. Extrai os dados de BRL, DXY e T10Y
3. Atualiza o CURRENT_DATA no cot_final_report.py
4. Executa o cot_final_report.py para gerar o relatorio

Uso: python scripts/atualizar_cot.py
"""

import pandas as pd
import requests
import zipfile
import io
import re
import os
from datetime import datetime


def get_latest_cot_data():
    """Baixa e extrai os dados COT mais recentes"""

    print("=" * 60)
    print("ATUALIZADOR COT")
    print("=" * 60)

    # Tenta baixar de 2026 primeiro, depois 2025
    years_to_try = [2026, 2025, 2024]
    df = None

    for year in years_to_try:
        url = f"https://www.cftc.gov/files/dea/history/fut_fin_txt_{year}.zip"
        print(f"\nTentando {year}...")

        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                z = zipfile.ZipFile(io.BytesIO(response.content))
                for filename in z.namelist():
                    if filename.endswith('.txt'):
                        with z.open(filename) as f:
                            df_year = pd.read_csv(f)
                            if df is None:
                                df = df_year
                            else:
                                df = pd.concat([df, df_year], ignore_index=True)
                print(f"  -> OK ({len(df_year)} registros)")
            else:
                print(f"  -> Nao disponivel (status {response.status_code})")
        except Exception as e:
            print(f"  -> Erro: {e}")

    if df is None:
        print("\nERRO: Nao foi possivel baixar dados!")
        return None

    # Encontra a data mais recente
    latest_date = df['Report_Date_as_YYYY-MM-DD'].max()
    print(f"\nData mais recente disponivel: {latest_date}")

    # Filtra para a data mais recente
    df_latest = df[df['Report_Date_as_YYYY-MM-DD'] == latest_date]

    # Extrai dados de cada ativo
    data = {
        'report_date': latest_date,
        'extracted_at': datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    # BRL
    brl = df_latest[df_latest['Market_and_Exchange_Names'].str.contains('BRAZILIAN REAL', case=False, na=False)]
    if len(brl) > 0:
        brl = brl.iloc[0]
        data['BRL'] = {
            'open_interest': int(brl['Open_Interest_All']),
            'asset_manager': {
                'long': int(brl['Asset_Mgr_Positions_Long_All']),
                'short': int(brl['Asset_Mgr_Positions_Short_All']),
                'net': int(brl['Asset_Mgr_Positions_Long_All'] - brl['Asset_Mgr_Positions_Short_All'])
            },
            'leveraged_funds': {
                'long': int(brl['Lev_Money_Positions_Long_All']),
                'short': int(brl['Lev_Money_Positions_Short_All']),
                'net': int(brl['Lev_Money_Positions_Long_All'] - brl['Lev_Money_Positions_Short_All'])
            },
            'dealer': {
                'long': int(brl['Dealer_Positions_Long_All']),
                'short': int(brl['Dealer_Positions_Short_All']),
                'net': int(brl['Dealer_Positions_Long_All'] - brl['Dealer_Positions_Short_All'])
            }
        }
        print(f"\nBRL: OK")
        print(f"  Asset Manager Net: {data['BRL']['asset_manager']['net']:+,}")

    # DXY (USD INDEX)
    dxy = df_latest[df_latest['Market_and_Exchange_Names'].str.contains('USD INDEX', case=False, na=False)]
    if len(dxy) > 0:
        dxy = dxy.iloc[0]
        data['DXY'] = {
            'open_interest': int(dxy['Open_Interest_All']),
            'asset_manager': {
                'long': int(dxy['Asset_Mgr_Positions_Long_All']),
                'short': int(dxy['Asset_Mgr_Positions_Short_All']),
                'net': int(dxy['Asset_Mgr_Positions_Long_All'] - dxy['Asset_Mgr_Positions_Short_All'])
            },
            'leveraged_funds': {
                'long': int(dxy['Lev_Money_Positions_Long_All']),
                'short': int(dxy['Lev_Money_Positions_Short_All']),
                'net': int(dxy['Lev_Money_Positions_Long_All'] - dxy['Lev_Money_Positions_Short_All'])
            },
            'dealer': {
                'long': int(dxy['Dealer_Positions_Long_All']),
                'short': int(dxy['Dealer_Positions_Short_All']),
                'net': int(dxy['Dealer_Positions_Long_All'] - dxy['Dealer_Positions_Short_All'])
            }
        }
        print(f"\nDXY: OK")
        print(f"  Leveraged Funds Net: {data['DXY']['leveraged_funds']['net']:+,}")

    # T10Y (UST 10Y NOTE)
    t10y = df_latest[df_latest['Market_and_Exchange_Names'].str.contains('UST 10Y NOTE', case=False, na=False)]
    if len(t10y) > 0:
        t10y = t10y.iloc[0]
        data['T10Y'] = {
            'open_interest': int(t10y['Open_Interest_All']),
            'asset_manager': {
                'long': int(t10y['Asset_Mgr_Positions_Long_All']),
                'short': int(t10y['Asset_Mgr_Positions_Short_All']),
                'net': int(t10y['Asset_Mgr_Positions_Long_All'] - t10y['Asset_Mgr_Positions_Short_All'])
            },
            'leveraged_funds': {
                'long': int(t10y['Lev_Money_Positions_Long_All']),
                'short': int(t10y['Lev_Money_Positions_Short_All']),
                'net': int(t10y['Lev_Money_Positions_Long_All'] - t10y['Lev_Money_Positions_Short_All'])
            },
            'dealer': {
                'long': int(t10y['Dealer_Positions_Long_All']),
                'short': int(t10y['Dealer_Positions_Short_All']),
                'net': int(t10y['Dealer_Positions_Long_All'] - t10y['Dealer_Positions_Short_All'])
            }
        }
        print(f"\nT10Y: OK")
        print(f"  Leveraged Funds Net: {data['T10Y']['leveraged_funds']['net']:+,}")

    return data


def update_script_data(data):
    """Atualiza o CURRENT_DATA no cot_final_report.py"""

    script_path = os.path.join(os.path.dirname(__file__), 'cot_final_report.py')

    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Cria o novo CURRENT_DATA
    new_data = f'''# DADOS ATUAIS (extraidos automaticamente em {data['extracted_at']}, relatorio de {data['report_date']})
CURRENT_DATA = {{
    "report_date": "{data['report_date']}",
    "BRL": {{
        "open_interest": {data['BRL']['open_interest']},
        "asset_manager": {{"long": {data['BRL']['asset_manager']['long']}, "short": {data['BRL']['asset_manager']['short']}, "net": {data['BRL']['asset_manager']['net']}}},
        "leveraged_funds": {{"long": {data['BRL']['leveraged_funds']['long']}, "short": {data['BRL']['leveraged_funds']['short']}, "net": {data['BRL']['leveraged_funds']['net']}}},
        "dealer": {{"long": {data['BRL']['dealer']['long']}, "short": {data['BRL']['dealer']['short']}, "net": {data['BRL']['dealer']['net']}}}
    }},
    "DXY": {{
        "open_interest": {data['DXY']['open_interest']},
        "asset_manager": {{"long": {data['DXY']['asset_manager']['long']}, "short": {data['DXY']['asset_manager']['short']}, "net": {data['DXY']['asset_manager']['net']}}},
        "leveraged_funds": {{"long": {data['DXY']['leveraged_funds']['long']}, "short": {data['DXY']['leveraged_funds']['short']}, "net": {data['DXY']['leveraged_funds']['net']}}},
        "dealer": {{"long": {data['DXY']['dealer']['long']}, "short": {data['DXY']['dealer']['short']}, "net": {data['DXY']['dealer']['net']}}}
    }},
    "T10Y": {{
        "open_interest": {data['T10Y']['open_interest']},
        "asset_manager": {{"long": {data['T10Y']['asset_manager']['long']}, "short": {data['T10Y']['asset_manager']['short']}, "net": {data['T10Y']['asset_manager']['net']}}},
        "leveraged_funds": {{"long": {data['T10Y']['leveraged_funds']['long']}, "short": {data['T10Y']['leveraged_funds']['short']}, "net": {data['T10Y']['leveraged_funds']['net']}}},
        "dealer": {{"long": {data['T10Y']['dealer']['long']}, "short": {data['T10Y']['dealer']['short']}, "net": {data['T10Y']['dealer']['net']}}}
    }}
}}'''

    # Substitui o CURRENT_DATA existente
    pattern = r'# DADOS ATUAIS.*?CURRENT_DATA = \{.*?\n\}'
    new_content = re.sub(pattern, new_data, content, flags=re.DOTALL)

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\n-> Script atualizado: {script_path}")


def main():
    # 1. Baixa dados mais recentes
    data = get_latest_cot_data()

    if data is None:
        print("\nERRO: Nao foi possivel extrair dados!")
        return

    if 'BRL' not in data or 'DXY' not in data or 'T10Y' not in data:
        print("\nERRO: Dados incompletos!")
        return

    # 2. Atualiza o script
    print("\n" + "-" * 40)
    print("Atualizando script...")
    update_script_data(data)

    # 3. Executa o script principal
    print("\n" + "-" * 40)
    print("Gerando relatorio...")
    print("-" * 40 + "\n")

    import subprocess
    result = subprocess.run(
        ['python', os.path.join(os.path.dirname(__file__), 'cot_final_report.py')],
        cwd=os.path.dirname(os.path.dirname(__file__))
    )

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("ATUALIZACAO CONCLUIDA COM SUCESSO!")
        print("=" * 60)
    else:
        print("\nERRO ao gerar relatorio!")


if __name__ == "__main__":
    main()
