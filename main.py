import requests
import hashlib
import sys

def request_api_function(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code}, check the API and try again')
    return res
  
def get_password_lieaks_count(hashes, hashes_to_check):
  hashes = (line.split(':') for line in hashes.text.splitlines())
  for h, count in hashes:
    if h == hashes_to_check:
      return count
  return 0

def check_password(password):
  # check password if it exists in API response
  sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
  query_char, tail = sha1password[:5], sha1password[5:]
  response = request_api_function(query_char)
  return get_password_lieaks_count(response, tail)

def main(args):
  for password in args:
    count = check_password(password)
    if count:
      print(f'{password} was found {count} times... you should probably change your password!\n')
    else:
      print(f'{password} was NOT found. Carry on!\n')
  return 'done!'

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))