#!/usr/bin/env python

'''
tag_generator.py
Copyright 2017 Long Qian
Contact: lqian8@jhu.edu
This script creates tags for your Jekyll blog hosted by Github page.
No plugins required.
'''

import glob
import os

post_dir = '_posts/'
category_dir = 'category/'

filenames = glob.glob(post_dir + '*md')

total_categories = []
for filename in filenames:
    f = open(filename, 'r')
    crawl = False
    for line in f:
        if crawl:
            current_categories = line.strip().split(':')
            print(current_categories)
            if current_categories[0] == 'categories':
                print('current tags are ', current_categories[1:])
                total_categories.extend(current_categories[1:])
                crawl = False
                break
        if line.strip() == '---':
            if not crawl:
                crawl = True
            else:
                crawl = False
                break
    f.close()
total_categories = set(total_categories)
total_categories = list(total_categories)

new_categories = []
for category in total_categories:
    category = category.split(',')
    for item in category:
        new_categories.append(item)

shortened_categories = []
for category in new_categories:
    if category[0] == ' ':
        short_category = category[1:]
        shortened_categories.append(short_category)
cleaned_categories = []
for category in shortened_categories:
    if category[0] == "[" and category[-1] == ']':
        clean_category = category[1:-1]
        clean_category = clean_category.replace(' ', '+')
        cleaned_categories.append(clean_category)
    elif category[0] == '[':
        print(category)
        clean_category = category[1:]
        clean_category = clean_category.replace(' ', '+')
        cleaned_categories.append(clean_category)
    elif category[-1] == ']':
        clean_category = category[:-1]
        clean_category = clean_category.replace(' ', '+')
        cleaned_categories.append(clean_category)
    else:
        category = category.replace(' ', '+')
        cleaned_categories.append(category)
print('clean categories are ', cleaned_categories)
old_categories = glob.glob(category_dir + '*.md')
for category in old_categories:
    os.remove(category)

if not os.path.exists(category_dir):
    os.makedirs(category_dir)

for category in cleaned_categories:
    category_filename = category_dir + category + '.md'
    f = open(category_filename, 'a')
    write_str = '---\nlayout: categorypage\ntitle: \"Category: ' + category + '\"\ncategory: ' + category + '\nrobots: noindex\n---\n'
    f.write(write_str)
    f.close()
print("Categories generated, count", cleaned_categories.__len__())
