# **User Manual Guidelines**



## Here is the url of our presentation video and Game demo video：



https://abdn.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=c3d90ea0-6f46-4c2d-a660-b19100da5343

## Overview of Structure 

![image-20240609202938036](https://github.com/HugoLee99/Text_Advanture_base_gpt3.5_finetune/blob/main/image/image-20240609202938036.png)



## Install Required Packages

First, ensure you have Flask and the OpenAI Python client library installed. You can install them using in shell:

```sh
pip install flask openai
```

Then, ensure other pyhton library are installed. You can install them using:

```sh
pip install Flask request jsonify render_template session
```



## Environment Configuration

Make sure you set your OpenAI API key in the environment variable before running the Flask app. You can add the following line to your `.bashrc` or `.bash_profile` file (assuming you're using Linux or macOS):

```sh
export OPENAI_API_KEY='your_openai_api_key'
```



## Version Control

There are 2 version of our software:

 `app_version1.py`  has been intricately engineered to deliver a user-centric experience, meticulously designed to present a curated selection comprising three distinct options, ensuring that users engage with a refined and focused set of choices every time they interact with the software.

 `app_version2.py`  is a standard generative  model, user can creatively enter your text and idea, and interact with our fine-tuning models to generate script. （we use`app_version1.py` below as example.）



## Self Design Prompt Engineer （optional）

In this part, user can change their story background of each motifs, which offered a more playable and creative user experience. Increase our software has a lot of extensibility.

![image-20240609201910860](https://github.com/HugoLee99/Text_Advanture_base_gpt3.5_finetune/blob/main/image/image-20240609201910860.png)



## Set up the server

run the `app_version1.py'`file by using the instruction in shell:

```sh
python app_version1.py
```



![image-20240609185839325](https://github.com/HugoLee99/Text_Advanture_base_gpt3.5_finetune/blob/main/image/image-20240609185839325.png)



Now, you can open your web browser and by going to  the second row  IP address: `http://192.168.10.115:5000`.(here just an example) This address points to the machine's network interface on the local network (LAN).  Accessible from other devices within the same local network (e.g., other computers, smartphones, tablets connected to the same router or network segment)



![image-20240609195950433](https://github.com/HugoLee99/Text_Advanture_base_gpt3.5_finetune/blob/main/image/image-20240609195950433.png)

By enter the IP address you can access our software home page.

## Trello is used to manage the project processing, recording teams develop log and contribution of each team member:
[https://trello.com/b/Ea5aU5kK/intelligent-software-project-kanban](https://trello.com/b/Ea5aU5kK)



















