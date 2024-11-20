from google_images_search import GoogleImagesSearch

API_KEY = 'your_google_api_key'
CX = 'your_custom_search_engine_id'

def download_images(query, num_images, output_folder):
    gis = GoogleImagesSearch(API_KEY, CX)

    search_params = {
        'q': query,                  
        'num': num_images,           
        'fileType': 'jpg',          
        'safe': 'off',               
        'imgType': 'photo',          
        'imgSize': 'large',          
    }

    gis.search(search_params=search_params, path_to_dir=output_folder)

if __name__ == "__main__":
    query = input("Enter the search query: ")
    num_images = int(input("Enter the number of images to download: "))
    output_folder = './downloaded_images'

    download_images(query, num_images, output_folder)
    print(f"{num_images} images downloaded to {output_folder}")
