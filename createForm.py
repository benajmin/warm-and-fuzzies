#!/usr/bin/env python3
import argparse
import requests
import datetime


def get_term():
  d = datetime.datetime.now()
  season = 'W' if 1 <= d.month <= 4 else 'S' if 5 <= d.month <= 8 else 'F'
  return season + str(d.year)[2:]


def get_title():
  return {
    'headerType': 'Default',
    'imageAlign': 'Left',
    'name': 'warmAnd',
    'order': '1',
    'text': f'{get_term()} Warm and Fuzzies',
    'textAlign': 'Left',
    'type': 'control_head',
    'verticalTextAlign': 'Middle'
  }


def get_submit(n):
  return {
    'buttonAlign': 'Auto',
    'buttonStyle': 'None',
    'clear': 'No',
    'clearText': 'Clear Form',
    'encryptIcon': 'No',
    'name': 'submit',
    'order': f'{n}',
    'print': 'No',
    'printText': 'Print Form',
    'text': 'Submit',
    'type': 'control_button'
  }


def get_drawing(name, n):
  return {
    'boxAlign': 'Left',
    'builderDescription': '',
    'cfname': 'Drawing Board',
    'customCSS': '',
    'finalSrc': 'http://data-widgets.jotform.io/drawingboard/',
    'frameHeight': '375',
    'frameSrc': 'http://data-widgets.jotform.io/drawingboard/',
    'frameWidth': '640',
    'inlineEditDefaultValue': 'Type a question',
    'label': 'Yes',
    'labelAlign': 'Top',
    'maxWidth': '587',
    'name': name.replace(' ', '')+'Drawing',
    'order': f'{n}',
    'paramChunks': '',
    'required': 'No',
    'selectedField': '529cb089728b3bc46f000004',
    'settingNames': 'customCSS',
    'settingNamesCSS': '',
    'static': 'No',
    'text': name,
    'type': 'control_widget',
    'widgetTabs': '[[\'general\',\'settingNames\'],[\'customcss\',\'settingNamesCSS\']]',
    'widgetType': 'field'
  }


def get_text(name, n):
  return {
    'cols': '63',
    'defaultValue': '',
    'description': '',
    'entryLimit': 'None-0',
    'entryLimitMin': 'None-0',
    'hint': 'Type here...',
    'labelAlign': 'Top',
    'maxsize': '',
    'mde': 'No',
    'name': name.replace(' ', '') + 'Text',
    'order': f'{n}',
    'readonly': 'No',
    'required': 'No',
    'rows': '6',
    'subLabel': '',
    'text': name,
    'type': 'control_textarea',
    'validation': 'None',
    'wysiwyg': 'Disable'
  }


def create_form(api_key, names):
  questions = [
      get_title(),
      *[get_drawing(name, 2*i+2) for i, name in enumerate(names)],
      *[get_text(name, 2*i+3) for i, name in enumerate(names)],
      get_submit(len(names)*2+2),
  ]
  payload = {
    'properties': {
      'title': f'{get_term()} Warm and Fuzzies',
      'height': '539'
    }
  }

  r = requests.put(f'https://api.jotform.com/form?apiKey={api_key}', json=payload)
  if r.json()['responseCode'] == 200:
    form_id = r.json()['content']['id']
    print(f'Created form: {form_id}')
  else:
    print(r.content)
    return


  payload = {
    'questions': questions,
  }
  r = requests.put(f'https://api.jotform.com/form/{form_id}/questions?apiKey={api_key}', json=payload)
  if r.json()['responseCode'] == 200:
    print('Added questions')
  else:
    print(r.content)


def delete_form(api_key, form_id):
  r = requests.delete(f'https://api.jotform.com/form/{form_id}?apiKey={api_key}')
  if r.json()['responseCode'] == 200:
    print(f'Successfully deleted form {form_id}')
  else:
    print(r.content)


def parse_args():
  parser = argparse.ArgumentParser(description='Create JotForm for UWCRT Warm and Fuzzies')
  parser.add_argument('apikey', help='JotForm API key')
  parser.add_argument('-f', help='Text file with responder names separated by new lines')
  parser.add_argument('-d', help='Form ID to be deleted')
  return parser.parse_args()


def main():
  args = parse_args()

  if args.d:
    delete_form(args.apikey, args.d)
  else:
    names = [line.strip() for line in open(args.f, 'r')]
    create_form(args.apikey, names)


if __name__ == '__main__':
  main()
