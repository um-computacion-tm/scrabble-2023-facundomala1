if [ ! -f "/usr/local/bin/codeclimate" ]
then
	curl -L https://github.com/codeclimate/codeclimate/archive/master.tar.gz | tar xvz -C /home/$USER/
	(cd /home/$USER/codeclimate-* && sudo make install)
fi

codeclimate engines:install
python3 tests/test.py
codeclimate analyze 