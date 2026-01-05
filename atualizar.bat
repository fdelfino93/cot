@echo off
echo ============================================================
echo ATUALIZADOR COT AUTOMATICO
echo ============================================================
echo.
echo Este script vai:
echo   1. Baixar dados mais recentes da CFTC
echo   2. Atualizar o script com os novos dados
echo   3. Gerar o relatorio atualizado
echo.
echo ------------------------------------------------------------
echo.
python scripts/atualizar_cot.py
echo.
echo ------------------------------------------------------------
echo Concluido! Arquivos atualizados:
echo   - cot_report.md (relatorio principal)
echo   - cot_evolucao.md (evolucao semanal)
echo   - historico/cot_report_YYYY-MM-DD.md (copia datada)
echo.
pause
