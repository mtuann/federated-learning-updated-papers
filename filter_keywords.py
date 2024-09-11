import pandas as pd
import re


def get_info_pp(pp):
    info = {}
    info['title'] = pp['title']
    info['authors'] = pp['author']
    info['publish_date'] = pp['publish_date']
    try:
        info['url'] = re.findall(r'href="(.*?)"', pp['url'])[0]
    except:
        info['url'] = ''
    try:
        info['code'] = re.findall(r'href="(.*?)"', pp['code'])[0]
    except:
        info['code'] = ''
    try:
        venue_name = re.findall(r'<li><span.*?>(.*?)</span></li>', pp['venue_name'])
        info['venue_name'] = venue_name[0]
        for i, v in enumerate(venue_name):
            if v != 'arXiv':
                info['venue_name'] = v
                break
        if info['venue_name'] == 'CoRR':
            info['venue_name'] = 'arXiv'
                
    except:
        info['venue_name'] = ''
    return info


# https://raw.githubusercontent.com/mtuann/research-papers/main/data/papers_fl.csv
df_paper = pd.read_csv('./papers_fl.csv')
print(f"Total papers: {len(df_paper)}")

# select the papers that "code" is not empty
df_paper_code = df_paper[df_paper['code'].notnull()]
print(f"Total papers with code: {len(df_paper_code)}")

# sort by publish date
df_paper_code = df_paper_code.sort_values(by='publish_date', ascending=False)

data_paper_md = '|No.|Title|Authors|Publish Date|Venue|Code|URL|\n|---|---|---|---|---|---|---|\n'
for idx, (_, pp) in enumerate(df_paper_code.iterrows()):
    info_pp = get_info_pp(pp)
    data_paper_md += '|{}|{}|{}|{}|{}|{}|{}|\n'.format(idx + 1, info_pp['title'], info_pp['authors'], info_pp['publish_date'], info_pp['venue_name'], info_pp['code'], info_pp['url'])

with open('./papers_fl.md', 'w') as f:
    f.write(data_paper_md)
print(f"Saved to papers_fl.md")
