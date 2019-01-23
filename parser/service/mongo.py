from pymongo import MongoClient


class MongoService:

    @staticmethod
    def connect():
        client = MongoClient('localhost',
                             username='root',
                             password='example',
                             authMechanism='SCRAM-SHA-256')
        return client

    def salva(self, documento):
        conexao = self.connect()
        db = conexao['gamelog']
        db.gamelog.insert_many([documento])
