import regex as re



class Image:
    """
    Represents an image with a URL, name, painter, and associated epochs.
    """

    def __init__(self, url, name=None, painter=None, epochs=[]):
        """
        Initializes a new Image object.

        Args:
            url (string): The URL of the image.
            name (string, optional): The name of the image.
            painter (string, optional): The painter of the image.
            epochs (list, optional): A list of epochs associated with the image.
        """
        self.url = url
        self.name = name
        self.painter = painter
        self.epochs = epochs


    def generate_filename(self, index):
        """
        Generates a filename for the image based on its URL and associated epochs.

        Args:
            index (int): The index of the image.

        Returns:
            string: The filename for the image.
        """
        # Set filename from url if possible otherwise use string of i.
        epoch_string = ""
        if self.epochs != None:
            epoch_string = ";".join(self.epochs) + ";"

        try:
            # Use regular expressions to extract the filename from the URL.
            reg_results = re.search("images/(.+?)\.jpg", self.url)

            if reg_results == None:
                reg_results = re.search("images/(.+?)\.jpeg", self.url)
 
            if reg_results == None:
                reg_results = re.search("images/(.+?)\.png", self.url)  

            local_file_name = reg_results.group(1)
            local_file_name = local_file_name.replace("/", "_")
            local_file_name = local_file_name.replace("-", ".")
            local_file_name = epoch_string + local_file_name
        except Exception as e:
            # If there is an error with the regex, use the index i as the filename.
            local_file_name = epoch_string + str(index)

        return local_file_name

    def __eq__(self, other):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)