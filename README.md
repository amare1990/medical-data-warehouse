# Medical Data Warehouse

> Medical Data Warehouse is a data science project focused on collecting, organizing, and analyzing medical data from multiple Telegram channels. The project utilizes web scraping techniques with Python and Telethon to extract medical-related information, such as text messages and images, and systematically store them in a structured format. The data is processed and stored in a dedicated warehouse, enabling efficient retrieval and analysis for insights, research, and decision-making in the healthcare domain. Additionally, images are scrapped and detected by pretrained YOLO5. Finally the collected data are exposed by fastapi rest api.
## Built With

- Major languages used: Python3
- Libraries: numpy, pandas, telethon, python-opencv, PyTorch
- Tools and Technlogies used: jupyter notebook, Google Colab, Git, GitHub, Gitflow, VS code editor.
- Pre-tained model: YOLO5

## Demonstration and Website

[Deployment link]()

## Getting Started

You can clone my project and use it freely, then contribute to this project.

- Get the local copy, by running `git clone https://github.com/amare1990/medical-data-warehouse.git` command in the directory of your local machine.
- Go to the repo main directory, run `cd medical-data-warehouse` command
- Create python environment by running `python3 -m venv venm-name`, where `ven-name` is your python environment you create
- Activate it by running:
   - `source venv-name/bin/activate` on linux os command prompt if you use linux os
   - `myenv\Scripts\activate` on windows os command prompt if you use windows os.

- After that you have to install all dependencies (already installed packages/libraries) by running `pip install -r requirements.txt`
- To automate the workflow and execute at a time, run the `python src/src.py` from the root directory of the repo or can be used for running the entire pipeline end-to-end without manual intervention.
- To run this project and experiment with individual components of the workflow, open each `jupyter notebook` command from the main directory of the repo and run it. The name of the notebook is carefully selected to match to the name of the script.

### Prerequisites

- You have to install Python (version 3.8.10 minimum), pip, git, vscode.

### Dataset

- Both text and image data are scrapped from the given telegram channels.
- Selected Telegram channels data are scrapped from.
  -  > https://t.me/DoctorsET \
      Chemed \
      https://t.me/lobelia4cosmetics \
      https://t.me/yetenaweg \
      https://t.me/EAHCI

- Images are scrapped from the following Telegram channels.
  - > Chemed \
      https://t.me/lobelia4cosmetics

### Project Requirements
- Git, GitHub setup, adding `pylint' in the GitHub workflows
- Scrapping both medica text and medical images from meidcal telegram channels
- Statistical and EDA analysis on the data, ploting
- Detection of scrapped medical images using YOLO
- Exposition of the collected data using FastAPI


#### GitHub Action and Following Python Coding Styles
- The `pylint` linters are added in the `.github/workflows` direcory of the repo, which is triggered while creating GitHub pill requests.
- Make it to check when Pull request is created
- Run `pylint scripts/example_script.py` to check if the code follows the standard format
- Run `autopep8 --in-place --aggressive --aggressive scripts/example_script.py` to automatically fix some linters errors


### Telegram Scrapping

Telegram Scraping is a component of the Medical Data Warehouse project, designed to extract relevant medical and cosmetic product information from selected Telegram channels. The scraper leverages Telethon for Telegram API interaction, efficiently fetching text messages and downloading images while filtering out non-image media. The extracted data is systematically stored in a structured format for further analysis and integration into the data warehouse.

- Setup:

    - Install required libraries:`pip install telethon`.
    - Create a `.env` file to store API_ID and API_HASH for Telegram authentication.

- Scraping Setup:

    - The TelegramScraper class allows for scraping messages from specified Telegram channels.
    - Channels to scrape are configured for both text and image types.

- Functions:

    - fetch_messages(channel): Fetches text messages or media from specified channels.
    - scrape_all_channels(): Scrapes all defined channels asynchronously.
    - store_data(channel, data): Stores text messages from a channel in .txt files.
    - download_image(message): Downloads images from channels with media.
    - append_scraped_data(): Aggregates data from .txt files and prepares it.
    - save_to_csv(): Converts the scraped data into a CSV file for easy analysis.

- Data Output:

    - Data is saved as scraped_data.csv in the data folder.
    - Scraped text data is stored in individual channel .txt files.

- Execution:

    Run the scraper by calling the run() method, which fetches and processes all data asynchronously.
    The entire process can be initiated using `await scraper.run()`.

### Data Cleaning and Transformation

- This process processes scrapped data. It uses the already scrapped data.
- Cleaning
  - Removes duplicate rows
  - Fills `""` for null values
- Saves the cleaned data as pandas dataformat, `data/cleaned_data.csv
- Stores the cleaned data in postgresql database
- Transfom the cleaned data using Data Build Tool (DBT)
  - Go to the root directory of the repo.
    - `cd medical-data-warehouse`
  - First install dbt by running `pip install dbt` command.
  - Initializes a DBT project using the name from .env. or running the command from the root direc, `dbt init my_project`
    - `my_project` dbt is created in the root directory
    - To run directoly from the terminal
      - `cd my_project`
      - To run dbt, run `dbt run`
      - To test dbt, run `dbt test`
      - To generate dbt documentation, run `dbt docs generate`
      - To serve the dbt documentation, run `dbt docs serve`
  - Log to track the scraping process, capture errors, and monitor progress

- The entire process is run by:

  > processor = DataProcessor() \
    processor.process_data()


### Object Detection Using YOLO5

- Install opencv by running `pip install opencv-python`
- Install PyTorch for YOLO5 detection, `pip install torch torchvision`
- To setup YOLO, run the following commands.
  - git clone https://github.com/ultralytics/yolov5.git
  - cd yolov5
  - pip install -r requirements.txt

- Load the YOLO5 model using PyTorch
- Use the model loaded and extract object detection results as DataFrame
- Extract relevant information such as bounding box, confidence score, and class label
- Store the extracted data into the postgresql database


### Exposing Collected Data using Fast API

FastAPI provides an easy way to create web APIs. We will create endpoints to allow users to access, post, and manipulate the collected data and object detection results. These endpoints will interact with the PostgreSQL database where the data is stored.

- Set up FastAPI:
    - Install FastAPI and Uvicorn with `pip install fastapi uvicorn`.

- Define Routes:
    - Use FastAPI to define routes for accessing the data. Example:
        - `@app.get("/detection_data/")`: Fetch collected detection data from the PostgreSQL database.
        - `@app.post("/detection_data/")`: Create new detection data in the database.

- Database Integration:
    - Ensure the FastAPI app connects to the PostgreSQL database using SQLAlchemy.
    - Use the get_db function to manage database connections.

- Testing:
    - Use FastAPI’s interactive Swagger documentation at `http://127.0.0.1:8000/docs` to test the API.

- Run the Server:
    - Launch the server with: `uvicorn main:app --reload`


> #### You can gain more insights by running the jupter notebook and view plots.


### More information
- You can refer to [this link]() to gain more insights about the reports of this project results.

## Authors

👤 **Amare Kassa**

- GitHub: [@githubhandle](https://github.com/amare1990)
- Twitter: [@twitterhandle](https://twitter.com/@amaremek)
- LinkedIn: [@linkedInHandle](https://www.linkedin.com/in/amaremek/)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](https://github.com/amare1990/medical-data-warehouse/issues).

## Show your support

Give a ⭐️ if you like this project, and you are welcome to contribute to this project!

## Acknowledgments

- Hat tip to anyone whose code was referenced to.
- Thanks to the 10 academy and Kifiya financial instituion that gives me an opportunity to do this project

## 📝 License

This project is [MIT](./LICENSE) licensed.
