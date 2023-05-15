import openai
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

# from tqdm import tqdm
import backoff

# Replace 'your_api_key' with your actual API key
openai.api_key = os.environ.get("OPENAI_API_KEY")


def backoff_hdlr(details):
    print(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


@backoff.on_exception(
    backoff.expo, openai.error.RateLimitError, max_tries=50, on_backoff=backoff_hdlr
)
def translate_text(value):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Translate the following JSON objects string values into Finnish, do not translate string "
                           "keys. No english string values are accepted.",
            },
            {
                "role": "user",
                "content": f"{json.dumps(value)}'",
            },
        ],
        max_tokens=1024,
        temperature=0,
    )
    return response.choices[0]["message"]["content"].strip()


def translate_item(item):
    translated_item = translate_text(item)
    return translated_item


# Maximum number of parallel requests
MAX_PARALLEL_REQUESTS = 20

# Assuming the input JSON is in a file named 'input.json'
with open("../data/alpaca_data_cleaned_archive.json", "r") as f:
    data = json.load(f)

lock = Lock()
start = 15024
end = 51785
translated_data = []
data = data[start:end]
tasks_completed = 0


# simple progress indicator callback function
def progress_indicator(future):
    global lock, tasks_completed
    # obtain the lock
    with lock:
        try:
            translated_data.append(json.loads(future.result()))
            # update the counter
            tasks_completed += 1
            # report progress
            print(
                f"{tasks_completed}/{len(futures)} completed, {len(futures) - tasks_completed} remain."
            )

            # if tasks_completed is divisable by 1000 save snapshot
            if tasks_completed % 1000 == 0:
                # Save the translated data to a new JSON file named 'translated_data.json'
                with open(f"translated_data_up_to_{start}_to_{end}.json", "w") as f:
                    json.dump(translated_data, f, ensure_ascii=False, indent=4)

                print(
                    f"Translation snapshot is saved in 'translated_data_from_{start}_to_{tasks_completed}.json'"
                )
        except Exception as e:
            print(f"exception: {e}")
            pass


with ThreadPoolExecutor(max_workers=MAX_PARALLEL_REQUESTS) as executor:
    futures = {executor.submit(translate_item, item): item for item in data}

    for future in futures:
        future.add_done_callback(progress_indicator)

# Finally save the translated data to a new JSON file named 'translated_data.json'
with open(f"translated_data_up_to_{start}_to_{end}.json", "w") as f:
    json.dump(translated_data, f, ensure_ascii=False, indent=4)

print(
    f"Translation complete. The translated data is saved in 'translated_data_from_{start}_to_{end}.json'"
)

#%%
