from fastapi import HTTPException


class ElementNotFoundException(HTTPException):
    def __init__(self, element_name):
        super().__init__(
            status_code=404,
            detail=f"{element_name} not found"
        )


class CargoNotFoundException(ElementNotFoundException):
    def __init__(self):
        super().__init__("cargo")


class LocationNotFoundException(ElementNotFoundException):
    def __init__(self):
        super().__init__("location")


class CarNotFoundException(ElementNotFoundException):
    def __init__(self):
        super().__init__("car")