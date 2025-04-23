import datetime

def generate_header():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"PXTOOL - {timestamp}\n(c) Misagh | github.com/misagh021kid\n\n"
