from store.models import Store


class StoreResponse:

    def to_json(self, store: Store) -> dict:
        return {
            'id': str(store.id),
            'name': store.name,
            'description': store.description,
            'type': store.type,
            'url': store.url,
            'active': store.active,
            'created_at': str(store.created_at),
            'updated_at': str(store.updated_at)
        }

