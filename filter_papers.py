import json
from datetime import datetime
import pandas as pd

date_str = datetime.now().strftime("%y%m%d")
print(f"date_str: {date_str}")

def convert_pp_to_csv(all_papers):
    # Filter papers
    group_by_title = {}
    for paper in all_papers:
        title_lower = paper['info']['title'].lower()
        if title_lower not in group_by_title:
            group_by_title[title_lower] = []
        group_by_title[title_lower].append(paper)
    print(f"Number of unique papers: {len(group_by_title)}")

    # Process duplicates
    # keys_dict = ['author', 'title', 'venue', 'volume', 'year', 'type', 'access', 'key', 'doi', 'ee', 'url']
    # keys_dict = ['author', 'title', 'venue', 'volume', 'year', 'type', 'access', 'key', 'doi', 'ee', 'url']
    keys_dict = ['title', 'venue', 'year', 'author', 'volume', 'url']
    pp_dict = {k: [] for k in keys_dict}

    for title, papers in group_by_title.items():
        paper = papers[-1]['info']
        try:
            authors = paper['authors']['author']
            authors = [a['text'] for a in authors]
            authors = ', '.join(authors)
        except:
            authors = ''
        venue = paper.get('venue', '')
        if isinstance(venue, list):
            venue = ' - '.join(venue[::-1])
        pp_dict['author'].append(authors)
        pp_dict['title'].append(paper.get('title', ''))
        pp_dict['venue'].append(venue)
        pp_dict['year'].append(paper.get('year', ''))
        pp_dict['volume'].append(paper.get('volume', ''))
        pp_dict['url'].append(paper.get('ee', ''))

    df_pp = pd.DataFrame(pp_dict)
    
    # sort by year: descending, venue: ascending, title: ascending
    df_pp = df_pp.sort_values(by=['year', 'venue', 'title'], ascending=[False, True, True]).reset_index(drop=True)
    df_pp.to_csv(f'fl_papers_{date_str}.csv', index=False)
    return df_pp


def categorize_papers(df_pp):
    print(f"Number of venue: {len(df_pp['venue'].unique())}")
    topics = {
        'Benchmark, Dataset and Survey': ['benchmark', 'dataset', 'survey'],
        'Statistical Challenges: data distribution heterogeneity and label deficiency': ['data distribution', 'label deficiency'],
        'Trustworthiness: security, privacy, fairness, incentive mechanism, etc.': ['security', 'privacy', 'fairness', 'incentive mechanism', 'attack', 'defense'],
        'System Challenges: communication and computational resource constrained, software and hardware heterogeneity, and FL system': ['communication', 'computational resource', 'software', 'hardware', 'FL system'],
        'Models and Applications': ['model', 'application'],
        'Others': [],
        'Irrelevance': [],
        # 'Optimization and Learning': ['optimization', 'learning'],
        # 'Federated Learning Framework': ['federated learning', 'FL'],
    }

    data_cat = {k: [] for k in topics.keys()}

    for _, paper in df_pp.iterrows():
        default_cat = 'Others'
        year = int(paper['year'])
        default_cat = 'Irrelevance' if year <= 2015 else next((cat for cat, kw in topics.items() if any(w in paper['title'].lower() for w in kw)), default_cat)
        data_cat[default_cat].append(paper)

    for k, v in data_cat.items():
        print(k, len(v))

    data_fl_md = ""

    for kk, vv in data_cat.items():
        data_to_md = f'# {kk}\n'
        data_to_md += '|No. | Title | Venue | Year | Author | Volume | \n'
        data_to_md += '|----|-------|-------|------|--------|--------|\n'
        data_to_md += ''.join([f"| {id + 1} | [{pp['title']}]({pp['url']}) | {pp['venue']} | {pp['year']} | {pp['author']} | {pp['volume']} | {pp['url']} |\n" for id, pp in enumerate(vv)])
        data_fl_md += data_to_md

    with open(f'./fl_dblp_{date_str}.md', "w") as fw:
        fw.write(data_fl_md)

all_papers = json.load(open(f'fl_dblp_240510.json'))
print(f"Number of papers: {len(all_papers)}")

df_pp = convert_pp_to_csv(all_papers)

# categorize_papers(df_pp)




