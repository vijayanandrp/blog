#!/usr/bin/env python3.5
# encoding: utf-8

import configparser

config = configparser.ConfigParser()

# I believe this config parser should use the perl autovivification method to create dynamic objects
config['DEFAULT'] = {
                        'Name': 'Vijay Anand',
                        'Sex': 'M',
                        'Age': 26,
                        'Married': False
                    }

# Always initiate dictionary for any new sections
config['www.facebook.com'] = {}
config['www.facebook.com']['user_name'] = 'VjyAnnd'

# Always initiate dictionary for any new sections
config['www.twitter.com'] = {}
twitter = config['www.twitter.com']
twitter['user_name'] = 'vijayanandrp'

config['DEFAULT']['Nationality'] = 'Indian'

import os
base_dir = os.getcwd()
config_path = os.path.join(base_dir, 'conf')
if not os.path.exists(config_path):
    os.mkdir(config_path)
config_file = os.path.join(config_path, 'example.ini')


with open(config_file, 'w') as cfile:
    config.write(cfile)

# ########## Reading Part ###############
config = configparser.ConfigParser()
print('Before reading -> ', config.sections())

config.read(config_file)
print('Now -> ', config.sections())

print('www.twitter.com' in config)
print('www.linkedin.com' in config)

print(config['DEFAULT']['Name'])

for key in config['DEFAULT']:
    print(key)


print(config['DEFAULT'].getboolean('Married'))

print(int(config['DEFAULT']['Age']))

