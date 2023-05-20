## 虚拟环境设置

生成虚拟环境目录
```python
python3 -m venv venv
```

切换到虚拟环境
```python
. venv/bin/activate
```

## 更新依赖包配置文件

前提是设置了项目的虚拟环境

如果在开发过程中安装了新的依赖包，请执行如下命令更新依赖库的配置文件

```python
pip3 freeze > ./requirements.txt
```

## 安装依赖

```
pip3 install -r requirements.txt
```
## 启动开发服务

```
flask --app flaskr run --debug
```