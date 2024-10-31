echo "是否要在当前环境安装依赖？(y/n)"
read -r response

if [[ "$response" == "y" || "$response" == "Y" ]]; then
    pip install -r requirements.txt
fi

python src/run.py
