cd /home/b5d045e6a2d7d567c0f95b76806cc81b/DAVAI-ciboulai/DAVAI-ciboulai/DAVAI
/usr/bin/python3 /home/b5d045e6a2d7d567c0f95b76806cc81b/.local/bin/gunicorn -t 100 -w 2 -b 127.0.0.1:8898 DAVAI.wsgi:application --access-logfile DAVAI.log 
