SELECT *
FROM read_json_auto('data/raw/apps.jsonl', format='newline_delimited')
