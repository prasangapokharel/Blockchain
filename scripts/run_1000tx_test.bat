@echo off
echo ===============================================
echo PHN Blockchain - Complete System Test
echo ===============================================
echo.
echo This will:
echo   1. Start the blockchain node
echo   2. Run 1000 transactions test (1 PHN each)
echo   3. Verify all components and fees
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo [1/2] Starting blockchain node...
start "PHN Node" python app/main.py

echo Waiting 5 seconds for node to start...
timeout /t 5 /nobreak > nul

echo.
echo [2/2] Running 1000 transaction test...
python test_1000_transactions.py

echo.
echo Test complete! Check the results above.
pause
