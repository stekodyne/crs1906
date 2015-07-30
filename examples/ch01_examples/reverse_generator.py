"""
reverse_generator.py - Example of generator function from Chapter 1
"""

def reverse(data):
    index = len(data)
    while index > 0:
        index -= 1
        yield data[index]
    return

print('{} reverse generator function {}'.format('-'*10, '-'*10))

for char in reverse('golf'):
    print(char)

print('{} double generator function {}'.format('-'*10, '-'*10))

def double(data):
    for index in range(0, len(data)):
        yield data[index]

for num in double([10, 20, 30, 40]):
    print(num)