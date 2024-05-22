FIFOCache = __import__('1-fifo_cache').FIFOCache

my_cache = FIFOCache()
my_cache.put("A", "Hello")
my_cache.put("B", "World")
my_cache.put("C", "Holberton")
my_cache.put("D", "School")
# my_cache.print_cache()

for key in my_cache.cache_data.keys():
    # print(key)
    break

key_list = list(my_cache.cache_data.keys())

print(key_list[0])