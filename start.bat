@echo off
echo 是否要在当前环境安装依赖？(y/n)
set /p response=

if /i "%response%"=="y" (
    pip install -r requirements.txt
)

python src/run.py
