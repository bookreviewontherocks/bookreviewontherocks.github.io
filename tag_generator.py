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
tag_dir = 'tag/'

filenames = glob.glob(post_dir + '*md')

total_tags = []
for filename in filenames:
    f = open(filename, 'r')
    crawl = False
    for line in f:
        if crawl:
            current_tags = line.strip().split(':')
            print(current_tags)
            if current_tags[0] == 'tags':
                print('current tags are ',current_tags[1:])
                total_tags.extend(current_tags[1:])
                crawl = False
                break
        if line.strip() == '---':
            if not crawl:
                crawl = True
            else:
                crawl = False
                break
    f.close()
total_tags = set(total_tags)
total_tags = list(total_tags)

new_tags = []
for tag in total_tags:
    tag = tag.split(',')
    for item in tag:
        new_tags.append(item)

shortened_tags = []
for tag in new_tags:
    if tag[0]==' ':
        short_tag = tag[1:]
        shortened_tags.append(short_tag)
cleaned_tags = []
for tag in shortened_tags:
    if tag[0]=="[" and tag[-1]==']':
        clean_tag = tag[1:-1]
        clean_tag = clean_tag.replace(' ', '+')
        cleaned_tags.append(clean_tag)
    elif tag[0]=='[':
        print(tag)
        clean_tag = tag[1:]
        clean_tag = clean_tag.replace(' ', '+')
        cleaned_tags.append(clean_tag)
    elif tag[-1]==']':
        clean_tag = tag[:-1]
        clean_tag = clean_tag.replace(' ', '+')
        cleaned_tags.append(clean_tag)
    else:
        tag = tag.replace(' ', '+')
        cleaned_tags.append(tag)
print('clean tags are ', cleaned_tags)
old_tags = glob.glob(tag_dir + '*.md')
for tag in old_tags:
    os.remove(tag)
    
if not os.path.exists(tag_dir):
    os.makedirs(tag_dir)

for tag in cleaned_tags:
    tag_filename = tag_dir + tag + '.md'
    f = open(tag_filename, 'a')
    write_str = '---\nlayout: tagpage\ntitle: \"Tag: ' + tag + '\"\ntag: ' + tag + '\nrobots: noindex\n---\n'
    f.write(write_str)
    f.close()
print("Tags generated, count", cleaned_tags.__len__())
