# Makefile Commands for Task Manager

# Default command to display help
help:
	@echo "Available commands:"
	@echo "  make run          - Start the Flask server"
	@echo "  make install      - Install project dependencies"
	@echo "  make clean        - Clean temporary files"

# Command to start the Flask server
run:
	python app.py

# Command to install project dependencies
install:
	pipx install -r requirements.txt

# Command to clean temporary files
clean:
	rm tasks.db task_manager.log