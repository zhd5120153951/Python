迁移步骤:
flask db
flask db init
flask db migrate -m 'init'
flask db upgrade
运行:flask run or python app.py(这个方式必须要把端口设为flask一致)