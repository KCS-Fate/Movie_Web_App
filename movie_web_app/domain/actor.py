class Actor:
    def __init__(self, actor_name: str):
        if actor_name == "" or type(actor_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_name.strip()
        self.__actor_colleagues = []

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other):
        return other.__actor_full_name > self.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        if not self.check_if_this_actor_worked_with(colleague):
            self.__actor_colleagues.append(colleague)
        return

    def check_if_this_actor_worked_with(self, colleague):
        if colleague in self.__actor_colleagues:
            return True
        else:
            return False