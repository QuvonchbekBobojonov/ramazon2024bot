from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("BOT_TOKEN")

CHANNELS = [
    ('https://t.me/Urganch_lenta_N1', '@Urganch_lenta_N1'),
    ('https://t.me/ish_kadr', '@ish_kadr'),
    ('https://t.me/+hsbS2jIYLME2OWQy', '@QuvonchbekBobojonov'),
]
