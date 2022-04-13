# ln -fs /usr/bin/python3 /usr/bin/python
# ln -fs /usr/bin/pip3 /usr/bin/pip

pip install -r requirements.txt
python manage.py migrate
supervisord -c supervisord.conf
