from jinja2 import Environment, FileSystemLoader
import datetime as dt
import json
import os
import re
import pandas as pd

def write_html_index(template, configs):
    root = os.path.dirname(os.path.abspath(__file__))
    # root = path to output directory
    os.makedirs(os.path.join(root, "deploy"), exist_ok=True)
    filename = os.path.join(root, "deploy", "table.html")
    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(template.render(configs=configs))


def load_template():
    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, "templates")
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("table.html")
    return template


def write_templates(configs):
    template = load_template()
    write_html_index(template, configs)

def main(configs):
    df = pd.read_csv('website_status.csv')
    column = [col for col in df.columns if re.search('status', str(col))]
    checkmark = '<span>&#9989;</span>'
    xmark = '<span>&#10060;</span>'
    df.loc[df[column[0]]=='200',['functioning']] = [checkmark]
    df.loc[(df[column[0]]=='403') | (df[column[0]]!='200'),['functioning']] = [xmark]
    configs['table'] = df.to_html(table_id="table", 
                                  columns=['URL','functioning',column[0]], 
                                  index=False, 
                                  escape=False,
                                  classes="styled-table",
                                  justify='left',
                                  render_links=True)
        
    write_templates(configs)

if __name__ == "__main__":
    configs = {
            "title": "Table of website status",
            }
    main(configs)