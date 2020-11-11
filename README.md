![](https://img.shields.io/github/workflow/status/samayer12/Interleave/CI) ![](https://img.shields.io/github/languages/count/samayer12/Interleave) ![](https://img.shields.io/github/last-commit/samayer12/Interleave) 

Messing around with Github CI and PDF processing.

This program will take two PDF files and match all paragraphs (which SHOULD be numbered) and store the matched pairs in a .csv. file.

**Example usage**
`python interleave.py file1.pdf file2.pdf output.csv`

**Example output**
```
Document1,Document2
1. First Entry.,1. First Entry
2. Second Entry.,2. Second Entry
3. Third Entry,3. Third Entry
```

**Current Status**

`106/1088` paragraphs (`9/74%`) in test data have an anomaly.
Here's a tabular representation of the anomalies.

|     | 1/2 | 3/4*| 5/6 | 7/8 | Total |
|-----|-----|-----|-----|-----|-------|
|EJ   | 18  | 10  | 10  | 16  | 54    |
|EPA  | 15  | 4   | 18  | 15  | 52    |
|Total| 33  | 14  | 28  | 31  | 106   |
