SELECT *
FROM read_json_auto('data/raw/reviews.jsonl', format='newline_delimited')
