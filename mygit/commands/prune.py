import os

def run():
    index_path = '.mygit/index'
    if not os.path.exists(index_path):
        print("No index file found. Nothing to prune.")
        return

    with open(index_path, 'r') as f:
        lines = f.read().splitlines()
    referenced_hashes = set(line.split(' ')[0] for line in lines)

    objects_dir = '.mygit/objects'
    if not os.path.exists(objects_dir):
        print("No objects directory found. Nothing to prune.")
        return

    all_objects = set(os.listdir(objects_dir))
    unused_objects = all_objects - referenced_hashes

    if not unused_objects:
        print("No unused objects to prune.")
        return

    for obj in unused_objects:
        obj_path = os.path.join(objects_dir, obj)
        try:
            os.remove(obj_path)
            print(f"Deleted unused object: {obj}")
        except Exception as e:
            print(f"Error deleting {obj}: {e}")
