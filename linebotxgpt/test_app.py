from openai import OpenAI
import my_config

api_key = my_config.section['OPEN_AI']
client = OpenAI(api_key=api_key)

# fn = client.files.create(
#   file=open("training_data.jsonl", "rb"),
#   purpose="fine-tune"
# )
# print(fn.id)

# model = client.fine_tuning.jobs.create(
#   training_file=fn.id, 
#   model="gpt-4o-mini-2024-07-18"
# )
# print(model.id)

# file-4IjdsLx1nxI6lSbaTjchiim0
# ftjob-h9DWXR82IK6JOdWZ19lDZ5wL

# List 10 fine-tuning jobs
# jobs = client.fine_tuning.jobs.list(limit=10)
# print(jobs)

# # Retrieve the state of a fine-tune
# client.fine_tuning.jobs.retrieve("ftjob-abc123")

# # Cancel a job
# client.fine_tuning.jobs.cancel("ftjob-abc123")

# List up to 10 events from a fine-tuning job

status = client.fine_tuning.jobs.list_events(fine_tuning_job_id="ftjob-Oqj2BZZLJfFoPYdhLKBUqKE3", limit=1)
print(status)

# # Delete a fine-tuned model (must be an owner of the org the model was created in)
# client.models.delete("ft:gpt-3.5-turbo:acemeco:suffix:abc123")


# from lib.gpt_helper import MyGPT
# gpt = MyGPT()

# r = gpt.FineTurnCalGPT('9.11跟9.9哪一個比較大?')

# print(r)