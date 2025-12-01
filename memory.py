class SessionMemory:
    def __init__(self):
        self.history = []

    def add(self, user_msg, assistant_msg):
        self.history.append({"user": user_msg, "assistant": assistant_msg})

    def context(self):
        return "\n".join(
            f"User: {tick['user']}\nAssistant: {tick['assistant']}" 
            for tick in self.history
        )
