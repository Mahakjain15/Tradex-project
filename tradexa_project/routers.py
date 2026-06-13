class ProductsRouter:
    """
    Routes all Product model queries to the 'products_db' database.
    All other models (User, Post, Django internals) use 'default'.
    """
    PRODUCTS_APP = 'products'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.PRODUCTS_APP:
            return 'products_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.PRODUCTS_APP:
            return 'products_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations within the same app
        if obj1._meta.app_label == obj2._meta.app_label:
            return True
        # Disallow cross-database relations
        if self.PRODUCTS_APP in {obj1._meta.app_label, obj2._meta.app_label}:
            return False
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.PRODUCTS_APP:
            return db == 'products_db'
        return db == 'default'
