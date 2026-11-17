@echo off
title GEN-ART Global Patient Intelligence Dashboard
echo ===================================================
echo   GEN-ART Global Patient Intelligence Platform
echo   ST-0625 Yetkili Saglik Turizmi Karar Destek Paneli
echo ===================================================
echo.
echo Sunucu baslatiliyor... Lutfen bekleyin.
echo Tarayicinizda acilacak adres: http://localhost:8501
echo.
start http://localhost:8501
python -m streamlit run app.py
pause
