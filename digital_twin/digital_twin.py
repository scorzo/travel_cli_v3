import json

class JSONReader:
    def __init__(self, filename):
        """
        Initializes the JSONReader instance with a filename.

        Args:
            filename (str): The name of the file to read.
        """
        self.filename = filename

    def read_json(self):
        """
        Reads a JSON file specified by the filename attribute and returns the data as a Python dictionary.

        Returns:
            dict: The data contained in the JSON file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            json.JSONDecodeError: If the file is not a valid JSON.

        Example:
            >>> reader = JSONReader("user_preferences.json")
            >>> data = reader.read_json()
            >>> print(data)
        """
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {self.filename} does not exist.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError("Failed to decode JSON, please check the file format.")

def main():
    filename = input("Enter the name of the JSON file to read: ")
    reader = JSONReader(filename)
    try:
        json_data = reader.read_json()
        print("JSON Data Read Successfully:")
        print(json.dumps(json_data, indent=4))
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
