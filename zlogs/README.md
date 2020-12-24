# PyTAF V2- Logger

Current implementation creates pytaf.log and keep appending same file until reaches to default Max size(10 MB).

If you want new log file for each test run then update config/logger_config.json to add {time} placeholder
in filename. Ex. "filename": "pytaf-{time}.log"