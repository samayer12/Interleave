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
|EJ   | 17  | 6   | 8   | 17  | 48    |
|EPA  | 15  | 3   | 21  | 15  | 54    |
|Total| 32  | 9   | 29  | 32  | 102   |
