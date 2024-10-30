from scheduler import bitpoll

page = bitpoll.get_poll_webpage("23fd6020-cd54-4397-b4ff-f0ee748c7f4d")
table = bitpoll.get_voting_table(page)
print(table)