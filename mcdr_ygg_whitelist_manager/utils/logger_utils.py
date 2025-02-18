from mcdreforged.api.all import *

def log(source: CommandSource,text):
    text = RTextList(text)
    source.get_server().broadcast(text)