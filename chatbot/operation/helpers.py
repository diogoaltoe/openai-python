def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except IOError as error:
        print(f"Failed to read the file {filename}. Error: {e}")