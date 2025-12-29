
## Helath Data API - main.py

#### Put items in db

```http
  PUT /healthdata
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | **Required**. PRIMARY KEY |
| `name` | `str` | Username |
| `app_name` | `str` | Applocation name for fetching the data |
| `oxygen` | `str` | fetch oxygen level from the app data|
| `calories` | `str` | calories fetch from app |
| `distance` | `str` | distance fetch from app device |
| `steps` | `int` | step count fetch from app |

#### Get item from db

```http
  GET /healthdata
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id` | `int` | **Required**. PRIMARY KEY |
| `name` | `str` | Username |
| `app_name` | `str` | Applocation name for fetching the data |
| `oxygen` | `str` | fetch oxygen level |
| `calories` | `str` | fetch calories   |
| `distance` | `str` | fetch distance  |
| `steps` | `int` | fetch step count |


## Image Uploading API - fileupload.py

#### Put image in db
Storing the image file into the folder also with writefile in folder 

```http
  PUT /upload
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | **Required**. PRIMARY KEY |
| `filename` | `str` | Image in a string formate |


#### Get image in db
Storing the roatated image file into the folder with writefile in folder to display that in the browser

```http
  PUT /upload
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `int` | **Required**. PRIMARY KEY |
| `filename` | `str` | Image in a string formate |