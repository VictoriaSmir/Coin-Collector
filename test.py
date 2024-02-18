import os
import json


def create_data_json():
    data = {"highest_score": 0}

    with open('data/data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("data.json created successfully.")


def load_data():
    if os.path.exists('data/data.json'):
        with open('data/data.json', 'r') as json_file:
            return json.load(json_file)
    else:
        print("data.json does not exist. Creating a new file.")
        create_data_json()
        return {"highest_score": 0}


def update_data(existing_data, score):
    existing_data["highest_score"] = score
    save_data(existing_data)


def save_data(data):
    with open('data/data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("data.json updated successfully.")


def main():
    existing_data = load_data()
    print(f'exisiting data from json = {existing_data}')
    score = 16
    print(existing_data['highest_score'])
    update_data(existing_data, score)
    existing_data["highest_score"] = score
    print(existing_data['highest_score'])

    # update_data(existing_data,12)


if __name__ == "__main__":
    main()
