class BaseResponseModel:

    def to_json(self, object_model) -> dict:
        return {field.name: getattr(object_model, field.name) for field in object_model._meta.fields}

