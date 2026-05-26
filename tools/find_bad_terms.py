import glob, re
terms = '염격|남각|침 찌르기|통타|가시 방어구|디터미네이션|가시 갑옷|검무|속참'
out = open('bad_terms.txt', 'w', encoding='utf-8')
for f in glob.glob('**/*KR*.md', recursive=True):
    text = open(f, encoding='utf-8').read()
    if re.search(terms, text):
        out.write(f'=== {f} ===\n')
        for l in text.splitlines():
            if re.search(terms, l):
                out.write(l.strip() + '\n')
out.close()
