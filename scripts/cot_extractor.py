"""
Extrator automatico de dados COT da pagina HTML da CFTC
Usa Playwright para acessar a pagina e extrair os dados mais recentes

Uso: python scripts/cot_extractor.py
"""

import asyncio
import re
from playwright.async_api import async_playwright


async def extract_cot_data():
    """Extrai dados COT da pagina da CFTC"""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Acessando pagina da CFTC...")
        await page.goto("https://www.cftc.gov/dea/futures/financial_lf.htm", timeout=60000)

        # Pega todo o texto da pagina
        content = await page.content()
        text = await page.inner_text("body")

        await browser.close()

        # Extrai a data do relatorio
        date_match = re.search(r'As of\s+(\w+\s+\d+,\s+\d{4})', text)
        if date_match:
            report_date = date_match.group(1)
            print(f"\nData do relatorio: {report_date}")

        # Funcao para extrair dados de um ativo
        def extract_asset_data(text, asset_name, categories):
            """Extrai dados de um ativo especifico"""
            results = {}

            # Encontra a secao do ativo
            pattern = rf'{asset_name}.*?(?=\n\n[A-Z]|\Z)'
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

            if match:
                section = match.group(0)

                for cat_name, cat_pattern in categories.items():
                    # Procura a linha da categoria
                    cat_match = re.search(rf'{cat_pattern}[:\s]+([0-9,]+)\s+([0-9,]+)', section)
                    if cat_match:
                        long_val = int(cat_match.group(1).replace(',', ''))
                        short_val = int(cat_match.group(2).replace(',', ''))
                        results[cat_name] = {
                            'long': long_val,
                            'short': short_val,
                            'net': long_val - short_val
                        }

            return results

        print("\n" + "=" * 60)
        print("DADOS EXTRAIDOS")
        print("=" * 60)

        # Procura por padroes especificos no texto
        # BRL
        brl_match = re.search(
            r'BRAZILIAN REAL.*?Asset Mgr.*?Positions.*?Long.*?All.*?:\s*([\d,]+).*?Short.*?All.*?:\s*([\d,]+)',
            text, re.DOTALL | re.IGNORECASE
        )

        # Abordagem alternativa: procurar tabelas
        print("\nBuscando dados por padrao de tabela...")

        # Extrai todas as linhas com numeros
        lines = text.split('\n')

        current_asset = None
        data = {
            'BRL': {'asset_manager': {}, 'leveraged_funds': {}, 'dealer': {}},
            'DXY': {'asset_manager': {}, 'leveraged_funds': {}, 'dealer': {}},
            'T10Y': {'asset_manager': {}, 'leveraged_funds': {}, 'dealer': {}}
        }

        for i, line in enumerate(lines):
            line_upper = line.upper()

            # Detecta o ativo
            if 'BRAZILIAN REAL' in line_upper:
                current_asset = 'BRL'
                print(f"\nEncontrado: {line.strip()}")
            elif 'USD INDEX' in line_upper or 'DOLLAR INDEX' in line_upper:
                current_asset = 'DXY'
                print(f"\nEncontrado: {line.strip()}")
            elif '10Y NOTE' in line_upper or '10-YEAR' in line_upper:
                current_asset = 'T10Y'
                print(f"\nEncontrado: {line.strip()}")

            # Se estamos em um ativo, procura os dados
            if current_asset:
                if 'ASSET MGR' in line_upper or 'ASSET MANAGER' in line_upper:
                    # Proximas linhas devem ter Long e Short
                    numbers = re.findall(r'[\d,]+', ' '.join(lines[i:i+5]))
                    if len(numbers) >= 2:
                        try:
                            long_val = int(numbers[0].replace(',', ''))
                            short_val = int(numbers[1].replace(',', ''))
                            data[current_asset]['asset_manager'] = {
                                'long': long_val,
                                'short': short_val,
                                'net': long_val - short_val
                            }
                        except:
                            pass

                elif 'LEV MONEY' in line_upper or 'LEVERAGED' in line_upper:
                    numbers = re.findall(r'[\d,]+', ' '.join(lines[i:i+5]))
                    if len(numbers) >= 2:
                        try:
                            long_val = int(numbers[0].replace(',', ''))
                            short_val = int(numbers[1].replace(',', ''))
                            data[current_asset]['leveraged_funds'] = {
                                'long': long_val,
                                'short': short_val,
                                'net': long_val - short_val
                            }
                        except:
                            pass

        # Mostra resultados
        print("\n" + "-" * 40)
        for asset, values in data.items():
            if values['asset_manager'] or values['leveraged_funds']:
                print(f"\n{asset}:")
                if values['asset_manager']:
                    am = values['asset_manager']
                    print(f"  Asset Manager: Long={am.get('long', 'N/A')}, Short={am.get('short', 'N/A')}, Net={am.get('net', 'N/A')}")
                if values['leveraged_funds']:
                    lf = values['leveraged_funds']
                    print(f"  Leveraged Funds: Long={lf.get('long', 'N/A')}, Short={lf.get('short', 'N/A')}, Net={lf.get('net', 'N/A')}")

        return data


if __name__ == "__main__":
    asyncio.run(extract_cot_data())
