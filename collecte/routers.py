class PrimaryReplicaRouter:
    """
    Routeur pour séparer les lectures et les écritures entre la base de données primaire et les répliques.
    """
    
    def db_for_read(self, model, **hints):
        """
        Les lectures vont vers la base de données 'replica' si elle existe, sinon 'default'.
        """
        return 'replica' if 'replica' in connections.databases else 'default'

    def db_for_write(self, model, **hints):
        """
        Les écritures vont toujours vers la base de données 'default'.
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Autorise les relations si les objets sont dans la même base de données.
        """
        db_set = {'default', 'replica'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Les migrations ne s'exécutent que sur la base de données 'default'.
        """
        return db == 'default'
