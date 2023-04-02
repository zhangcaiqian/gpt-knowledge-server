## 虚拟环境设置

Create a project folder and a venv folder within

mkdir myproject
cd myproject
python3 -m venv venv

Activate the environment

. venv/bin/activate

pip install Flask

## 更新依赖包配置文件

前提是设置了项目的虚拟环境

pip3 freeze > ./requirements.txt

## 安装依赖

pip3 install -r requirements.txt

## 启动开发服务

flask --app flaskr run --debug