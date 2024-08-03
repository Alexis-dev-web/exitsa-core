from dataclasses import dataclass
from utils.base_dto import BaseDto
from store.models import Store


@dataclass
class CreateOrUpdateStoreDTO(BaseDto):
    name: str
    type: str
    is_provider: bool = False
    description: str = None
    url: str = None
    store_id: str = None
    store: Store = None

