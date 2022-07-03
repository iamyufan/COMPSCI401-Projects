import json
import pandas as pd

import pandas as pd
data_test = pd.read_csv('./test.csv', delimiter=";")
data_test = data_test[['text', 'country_code']]
data_test['target_id'] = data_test['country_code'].apply(lambda x: int(x == 'US'))
data_test.drop(['country_code'], axis=1, inplace=True)
data_test

with open('./test.json', 'w') as jsonfile:
    final_data = {}
    counter = 0
    for i in range(data_test.shape[0]):
        final_data[counter] = {
            "text":data_test.loc[i, "text"],
            "target":str(data_test.loc[i, "target_id"])
        }
        counter += 1
    json.dump(final_data, jsonfile)
    jsonfile.write('\n')