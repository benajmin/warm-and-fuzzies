#!/usr/bin/env python3
import argparse
import requests
import shutil
import os
import subprocess
import html
from createForm import get_term
import re


def tex_escape(text):
  """
    :param text: a plain text message
    :return: the message escaped to appear correctly in LaTeX
  """
  conv = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\^{}',
    '\\': r'\textbackslash{}',
    '<': r'\textless{}',
    '>': r'\textgreater{}',
  }
  regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
  return regex.sub(lambda match: conv[match.group()], text)


def get_submissions(api_key, form_id):
  r = requests.get(f'https://api.jotform.com/form/{form_id}/submissions?apiKey={api_key}&limit=1000')
  return [y for x in r.json()['content'] for y in x['answers'].values() if 'answer' in y]


def parse_args():
  parser = argparse.ArgumentParser(description='Download responses from JotForm and collate into individual files')
  parser.add_argument('apikey', help='JotForm API key')
  parser.add_argument('formID', help='Form ID to be collate')
  return parser.parse_args()


def download_answers(answers):
  for i, answer in enumerate(answers):
    if answer['name'].endswith('Drawing') and answer['answer']:
      url = answer['answer']
      r = requests.get(url)
      if len(r.content) > 6000:
        with open(f'tmp/{i}.png', 'wb') as f_img:
          f_img.write(r.content)
    else:
      with open(f'tmp/{i}.txt', 'w') as f_text:
        f_text.write(tex_escape(html.unescape(answer['answer'])))


def main():
  args = parse_args()

  shutil.rmtree('tmp', ignore_errors=True)
  shutil.rmtree('out', ignore_errors=True)
  os.mkdir('out')

  answers = get_submissions(args.apikey, args.formID)
  names = set(x['text'] for x in answers)
  for name in names:
    os.mkdir('tmp')
    download_answers(x for x in answers if x['text'] == name)
    shutil.copy('template.tex', f'tmp/{name.split()[0]}.tex')
    subprocess.Popen(['xelatex', f'{name.split()[0]}.tex'], cwd='tmp', stdout=subprocess.DEVNULL).wait()
    shutil.copy(f'tmp/{name.split()[0]}.pdf', f'out/{get_term()}_{name.replace(" ", "")}_WarmAndFuzzies.pdf')
    shutil.rmtree('tmp', ignore_errors=True)


if __name__ == '__main__':
  main()
