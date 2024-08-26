class InvalidInputException(Exception):
    def __init__(self, parameter_name: str, message: str = "Invalid parameter"):
        self.parameter_name = parameter_name
        self.message = f"{message}: {parameter_name}"
        super().__init__(self.message)