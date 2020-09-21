pip install --target ./package/ aiohttp
pip install --target ./package/ requests
cd package/
zip -r9 ../function.zip .
cd ..
zip -g function.zip eventBriteHelper.py