from pydantic import BaseModel


class OrderCreateSchema(BaseModel):
    pass


class BaseDTO(BaseModel):
    def serialize(self) -> bytes:
        return self.model_dump_json().encode('utf-8')

    @classmethod
    def deserialize(cls, data: bytes) -> 'BaseDTO':
        data_str = data.decode('utf-8')
        return cls.model_validate_json(data_str)


class OrderDTO(BaseDTO):
    id: int
    status: str