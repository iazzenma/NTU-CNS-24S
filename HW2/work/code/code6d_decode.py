c = 6446630351614507838738422614489672792615571834598810749
message = c.to_bytes((c.bit_length() + 7) // 8, 'big')
print(message.decode())
import os
if os.path.exists('data.py'):
    os.remove('data.py')