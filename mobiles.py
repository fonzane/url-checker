
def read_mobiles(db, numbers):
  numbers.clear()
  for number in db.get_numbers():
     numbers.append(number)
  print(f"read numbers from db: {numbers}")