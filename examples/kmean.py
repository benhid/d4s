from d4s import Data4Science, StoreHubClient
from d4s.service import DataMinerKmeans

options = {
    'token': 'GCUBE-TOKEN'
}

with Data4Science(options) as d4s:
    storeHub = StoreHubClient()

    # creates and uploads a folder in the workspace
    folder_id = storeHub.create_folder(name='iris-test')
    file = storeHub.upload_file(folder_id=folder_id, file_path='./iris.csv', name='iris')

    print(file.public_url)

    # run k-means against file in workspace
    kmeans = DataMinerKmeans()
    results = kmeans.run(file, feature='variety')

print(results)
