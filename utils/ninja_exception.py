class MessageValueError(Exception):
    def __init__(self, message: str | None = None,
                 alias="validation_error",
                 message_type="error",
                 messages: list[str] | None = None,
                 inline: dict[str, str | list[str]] | None = None):
        self.message = message
        self.messages = messages
        self.alias = alias
        self.message_type = message_type
        self.inline = inline
        super().__init__(message)
