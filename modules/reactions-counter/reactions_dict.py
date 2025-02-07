from telethon.tl.types import ReactionEmoji, ReactionCustomEmoji

class ReactionsDict():
    def __init__(self, emoji: list[str], custom_emoji: list[int]):
        self.emoji = map(lambda emiticon: ReactionEmoji(emiticon), emoji)
        self.custom_emoji = map(lambda document_id: ReactionCustomEmoji(document_id), custom_emoji)