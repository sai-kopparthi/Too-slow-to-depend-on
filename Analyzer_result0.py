import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime
import json
import pickle

###################################
# EDIT THESE CONSTANTS
###################################

GROUP = "ecs260-31"
DB_PASSWORD = "phrasing-litany-guttural-invest"
ANALYZER_NAME = "ecs260-31/js-dependencies"
ANALYZER_VERSION = "0.0.1"
CORPUS_NAME = "r2c-1000-monthly"

###################################
# END EDIT SECTION
###################################

# Canonical SQL query to get job-specific results back.
JOB_QUERY = 
 SELECT (result.extra#>>'{name}')::name,commit_metadata.committed_at,result.check_id,commit_corpus.repo_url,result.extra FROM result,  commit_corpus,commit_metadata WHERE result.commit_hash = commit_corpus.commit_hash AND commit_metadata.commit_hash=result.commit_hash AND analyzer_name = 'r2c/js-dependencies'  AND analyzer_version = '1.0.3'  AND corpus_name = 'r2c-1000-monthly';


QUERY_PARAMS = {
    "corpus_name": CORPUS_NAME,
    "analyzer_name": ANALYZER_NAME,
    "analyzer_version": ANALYZER_VERSION
}

# Connect to PostgreSQL host and query for job-specific results
engine = create_engine(f'postgresql://notebook_user:{DB_PASSWORD}@{GROUP}-db.massive.ret2.co/postgres')
job_df = pd.read_sql(JOB_QUERY, engine, params=QUERY_PARAMS)

print(job_df)
job_df.to_pickle("./dummy.pkl")
print(type(job_df))


r={}
job_df=pd.read_pickle("./dummy.pkl")
table1={}
#print(type(job_df.extra[0]))
print(job_df)


for i in range(job_df.size):
    try:
        if job_df.check_id[i] == 'package-json-dev-dependency' or job_df.check_id[i] == 'package-json-dependency' or job_df.check_id[i] == 'package-json-peer-dependency' or job_df.check_id[i] == 'package-json-optional-dependency' or job_df.check_id[i] == 'package-json-bundled-dependency':
            a = job_df.extra[i]['specifiedVersion']
            if len(a) > 0:
                if a[0]>'9':
                     a = a[1:6]
        else:
            a = job_df.extra[i]['resolvedVersion']
        if job_df.extra[i]['name'] in table1:
            val = table1.get(job_df.extra[i]['name'])
            if a > val[0]:
                table1[job_df.extra[i]['name']] = [a,job_df.committed_at[i]]
            if a == val[0]:
                if job_df.committed_at[i] < val[1]:
                    table1[job_df.extra[i]['name']] = [a, job_df.committed_at[i]]
        else:
            table1[job_df.extra[i]['name']] = [a, job_df.committed_at[i]]
    except:
        print("name not found")


print(table1)

with open('filename.pickle', 'wb') as handle:
    pickle.dump(table1, handle, protocol=pickle.HIGHEST_PROTOCOL)


with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)

#print(b)
table1=b

fmt = '%Y-%m-%d %H:%M:%S'
table2={}
result={}
for i in range(job_df.size):
    try:
        if job_df.check_id[i] == 'package-json-dev-dependency' or job_df.check_id[i] == 'package-json-dependency' or job_df.check_id[i] == 'package-json-peer-dependency' or job_df.check_id[i] == 'package-json-optional-dependency' or job_df.check_id[i] == 'package-json-bundled-dependency':
            if job_df.repo_url[i] in table2:
                c = table1[job_df.extra[i]['name']]
                t1=datetime.strptime(str(c[1]), fmt)
                t2=datetime.strptime(str(table2[job_df.repo_url[i]]), fmt)
                t3=datetime.strptime(str(job_df.committed_at[i]),fmt)
                if t1>t2 and t1>t3:
                    table2[job_df.repo_url[i]]=c[1]
                    a=(t1-t2)
                    print(a)
                    result[job_df.repo_url[i]]=a
            else:
                c = table1[job_df.extra[i]['name']]
                table2[job_df.repo_url[i]]=job_df.committed_at[i]
                
    except:
        continue

print(result)

with open('result.pickle', 'wb') as handle:
    pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('result.pickle', 'rb') as handle:
    b = pickle.load(handle)
print(b)




