@echo off
title GEN-ART Global Patient Intelligence Dashboard
echo ===================================================
echo   GEN-ART Global Patient Intelligence Platform
echo   ST-0625 Yetkili Saglik Turizmi Karar Destek Paneli
echo ===================================================
echo.
echo Sunucu baslatiliyor... Lutfen bekleyin.
echo Tarayicinizda acilacak adres: http://localhost:8510
echo.
start http://localhost:8510
python -m streamlit run app.py --server.port 8510 --server.address 0.0.0.0
pause
