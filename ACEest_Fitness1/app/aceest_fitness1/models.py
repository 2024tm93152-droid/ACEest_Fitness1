class Member:
    def __init__(self, id, name, membership):
        self.id = id
        self.name = name
        self.membership = membership

    def to_dict(self):
        return {"id": self.id, "name": self.name, "membership": self.membership}
