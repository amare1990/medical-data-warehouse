# Medical Data Warehouse

> Medical Data Warehouse is a data science project focused on collecting, organizing, and analyzing medical data from various sources, including Telegram channels. The project utilizes web scraping techniques with Python and Telethon to extract medical-related information, such as text messages and images, and systematically store them in a structured format. The data is processed and stored in a dedicated warehouse, enabling efficient retrieval and analysis for insights, research, and decision-making in the healthcare domain.
## Built With

- Major languages used: Python3
- Libraries: numpy, pandas, matplotlib.pyplot, scikit-learn
- Tools and Technlogies used: jupyter notebook, Google Colab, Git, GitHub, Gitflow, VS code editor.

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

- After that you have to install all the necessary Python libraries and tools by running `pip install -r requirements.txt`
- To automate the workflow and execute at a time, run the `python main/main.py` from the root directory of the repo or can be used for running the entire pipeline end-to-end without manual intervention.
- To run this project and experiment with individual components of the workflow, open `jupyter notebook` command from the main directory of the repo and run it.

### Prerequisites

- You have to install Python (version 3.8.10 minimum), pip, git, vscode.

### Dataset

- Both text and image data are scrapped from the given telegram channels.

### Project Requirements
- Git, GitHub setup, adding `pylint' in the GitHub workflows
- Scrapping both medica text and medical images from meidcal telegram channels
- Statistical and EDA analysis on the data, ploting
- Detection of scrapped medical images using YOLO
- Exposition of the collected data using FastAPI


#### GitHub Action and Following Python Coding Styles
- The `pylint` linters are added in the `.github/workflows` direcory of the repo.
- Make it to check when Pull request is created
- Run `pylint scripts/telegram_scrapper.py` to check if the code follows the standard format
- Run `autopep8 --in-place --aggressive --aggressive scripts/telegram_scrapper.py` to automatically fix some linters errors


### Telegram Scrapping

Telegram Scraping is a component of the Medical Data Warehouse project, designed to extract relevant medical and cosmetic product information from selected Telegram channels. The scraper leverages Telethon for Telegram API interaction, efficiently fetching text messages and downloading images while filtering out non-image media. The extracted data is systematically stored in a structured format for further analysis and integration into the data warehouse.

### Data Cleaning and Transformation


### Object Detection Using YOLO5
- To setup YOLO, run the following commands.
  - git clone https://github.com/ultralytics/yolov5.git
  - cd yolov5
  - pip install -r requirements.txt


### Future Works
- Data cleaning and transformation
- Conducting Exploratory data analysis on data scrapped
- Detecting scrapped images using YOLO
- Exposing collected data using Fast API


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
