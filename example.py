from perplexityai import Perplexity

api = Perplexity()

# Start the Bot
api.start()

#Ask any query
query = "What yoga pose literally means ‘corpse pose’?"
result = api.ask(query)
print(result)

#Stop the Bot
api.stop()
