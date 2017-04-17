class User():
    def __init__(self):
        self._username = ""
        self._token = ""
        self._client_id = ""
        self._client_secret = ""
        self.config()

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, x):
        self._username = x

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, x):
        self._token = x

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, x):
        self._client_id = x

    @property
    def client_secret(self):
        return self._client_secret

    @client_secret.setter
    def client_secret(self, x):
        self._client_secret = x
        
    def config(self):
        with open("config", "r") as f:
            for i in f:
                lhs = i.split("=")[0].rstrip()
                rhs = i.split("=")[1].lstrip().split("\n")[0]
                if lhs == "username":
                    self.username = rhs
                elif lhs == "token":
                    self.token = "Bearer " + rhs
                elif lhs == "client_id":
                    self.client_id = rhs
                elif lhs == "client_secret":
                    self.client_secret = rhs
