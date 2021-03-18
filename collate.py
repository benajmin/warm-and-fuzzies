#!/usr/bin/env python3
import argparse
import requests
import shutil
import os


def get_submissions(api_key, form_id):
  r = requests.get(f'https://api.jotform.com/form/{form_id}/submissions?apiKey={api_key}')
  return [y for x in r.json()['content'] for y in x['answers'].values() if 'answer' in y]


def parse_args():
  parser = argparse.ArgumentParser(description='Download responses from JotForm and collate into individual files')
  parser.add_argument('apikey', help='JotForm API key')
  parser.add_argument('formID', help='Form ID to be collate')
  return parser.parse_args()


def main():
  args = parse_args()

  shutil.rmtree('tmp', ignore_errors=True)
  shutil.rmtree('out', ignore_errors=True)
  os.mkdir('out')

  answers = get_submissions(args.apikey, args.formID)
  names = set(x['text'] for x in answers)
  for name in names:
    os.mkdir('tmp')
    with open('tmp/text.txt', 'w') as f_text:
      for answer in answers:
        if answer['text'] == name:
          if answer['name'].endswith('Drawing'):
            url = answer['answer']
            filename = url.split('/')[-1]
            r = requests.get(url)
            with open(os.path.join('tmp', filename), 'wb') as f_img:
              f_img.write(r.content)
          else:
            print(answer['answer'], file=f_text)
    shutil.rmtree('tmp', ignore_errors=True)


if __name__ == '__main__':
  main()
