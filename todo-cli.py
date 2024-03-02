#!/usr/bin/env python

import argparse
import json
import urllib.request
import concurrent.futures

def fetch_todo(todo_id):
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching TODO {todo_id}: {e}")
        return None

def main(num_todos):
    even_todo_ids = [i for i in range(2, num_todos * 2 + 1, 2)]  # Generate even todo IDs
    todo_data = []

    # Concurrently fetch TODOs
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_todo = {executor.submit(fetch_todo, todo_id): todo_id for todo_id in even_todo_ids}
        for future in concurrent.futures.as_completed(future_to_todo):
            todo_id = future_to_todo[future]
            todo = future.result()
            if todo:
                todo_data.append(todo)
    # Sort TODOs by ID in ascending order
    todo_data.sort(key=lambda x: x['id'])

    # Output title and completion status
    for todo in todo_data:
        title = todo.get('title', 'N/A')
        completed = todo.get('completed', False)
        print(f"Title: {title}, Completed: {'Yes' if completed else 'No'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num_todos", nargs='?', default=20, type=int)
    args = parser.parse_args()

    main(args.num_todos)
