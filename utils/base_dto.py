class BaseDto:

    @classmethod
    def from_json(cls, json_data: dict):
        expected_fields = cls.__annotations__.keys()
        filtered_json_data = {key: value for key, value in json_data.items() if key in expected_fields}
        return cls(**filtered_json_data)
