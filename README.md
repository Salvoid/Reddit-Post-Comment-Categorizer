## Tool Name: Reddit Post Comment Categorizer
## Upload Date & Time: 07-14-2023 21:35:00
## Description: Reddit Post Comment Categorizer Tool using Negative Sampling and Quantization Topic Model

## Tool Documentation Title: Categorization of Reddit Post's Comments by Topic Modeling using Negative Sampling and Quantization Topic Model
## Tool Documentation: https://pupedu-my.sharepoint.com/:b:/g/personal/ectvalenzuela_iskolarngbayan_pup_edu_ph/EfKaM5N-fv5Is__3mvePXUYBjK04GSB13yutRwP0l2Hylg?e=n1afma

## Algorithm Documentation Title: Short Text Topic Modeling with Topic Distribution Quantization and Negative Sampling Decoder
## Algorithm Documentation: https://aclanthology.org/2020.emnlp-main.138.pdf
## Algorithm Source Code: https://github.com/BobXWu/NQTM

### Folders:
#### OriginalCode
-Contains the original source code of both the gui and batch verification versions.
#### ExecutableCode
-Contains the source code for the gui and the packaged gui version.
#### Executable
-Contains the packaged gui version.
#### TopicCoherenceEvaluation
-Contains the source code for the Normalized Pointwise Mutual Information (NPMI) Topic Coherence Measure Evaluation.

### Notes:
-Reddit Developer Account Credentials are required to access the Reddit API in order to fetch Reddit Posts and Comments. All credentials must be placed in the corresponding variables "in_client_id", "in_client_secret", "in_username", "in_password", and "in_user_agent" in the "init_reddit()" function inside the "main.py" file.