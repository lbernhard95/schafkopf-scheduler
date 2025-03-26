FROM joyzoursky/python-chromedriver:3.7-selenium

# Copy all necessary files from the core folder
COPY core/ /app/core/

# Set the working directory
WORKDIR /app

# Command to run the application
CMD ["python", "core/main.py"]

