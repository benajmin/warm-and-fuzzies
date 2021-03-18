#!/usr/bin/env python3
import argparse
import requests

def get_title():
  # TODO term
  return {
    'headerType': 'Default',
    'imageAlign': 'Left',
    'name': 'warmAnd',
    'order': '1',
    'text': 'Warm and Fuzzies',
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
    'name': 'submit2',
    'order': f'{n+2}', # TODO x2
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
    'labelAlign': 'Auto',
    'maxWidth': '587',
    'name': name.replace(' ', ''),
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

def create_form(api_key, names):
  questions = [
      get_title(),
      get_submit(len(names)),
      *[get_drawing(name, i+2) for i, name in enumerate(names)]
  ]
  payload = {
    'questions': questions,
    'properties': {
      'title': 'Warm and Fuzzies', # TODO term
      'height': '539'
    }
  }
  r = requests.put(f'https://api.jotform.com/form?apiKey={api_key}', json=payload)
  print(r.content)

def parse_args():
  parser = argparse.ArgumentParser(description='Create JotForm for UWCRT Warm and Fuzzies')
  parser.add_argument('apikey', help='JotForm API key')
  parser.add_argument('file', help='Test file with responder names separated by new lines')
  return parser.parse_args()

def main():
  args = parse_args()

  names = [line.strip() for line in open(args.file, 'r')]
  create_form(args.apikey, names)

if __name__ == '__main__':
  main()
