import datetime
from store.models import Store
from user.models import User


class StoreDummyData:

    def build_store(self):
        store = Store()
        store.name = 'Dummy Store'
        store.type = 'DIGITAL'
        store.active = True
        store.created_at = datetime.datetime.today()
        store.updated_at = datetime.datetime.today()

        return store

    def build_user_test(self, email='testing@exitosa.test'):
        user = User()
        user.first_name = 'test'
        user.last_name = 'tets last name'
        user.email = email

        return user