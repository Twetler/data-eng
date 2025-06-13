
update_requirements:
	@pip3 freeze > requirements.txt
	@echo "Updated requirements.txt with current packages."

make_env:
	@python3 -m venv env
	@source env/bin/activate
	@pip3 install -r requirements.txt
