<!-- adapted from: https://github.com/othneildrew/Best-README-Template -->
<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<div align="center">
  <h1 align="center">quote-hero 💬</h1>
  <p align="center">Searching Wikiquote with Elasticsearch</p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about">About</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#how-to-play">How To Play</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About

![product-screenshot]

quote-hero is game where you attempt to match as many Wikiquote pages as possible using random words. Adding more words gives you a higher score, but is risky because you might not be able any pages. Depending on how confident you are in your set of words you can choose to match your words exactly or loosely.

quote-hero is made up of several applications orchestrated with Docker Compose:

- A single node Elasticsearch cluster is used to search for matching pages.
- The ingest process creates an ElasticSearch index and populates it with the most recent [dump][wikiquote-dump-url] published by Wikiquote.
- The api returns random words (using the top [10,000 most frequent][common-words-url] english language words), and returns the search results.
- The frontend allows users play quote-hero
- An nginx reverse proxy serves the frontend and api.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![Elasticsearch][Elasticsearch]][Elasticsearch-url]
[![Python][Python]][Python-url]
[![FastAPI][FastAPI]][FastAPI-url]
[![React][React]][React-url]
[![TailwindCSS][TailwindCSS]][TailwindCSS-url]
[![Vite][Vite]][Vite-url]
[![Docker][Docker]][Docker-url]
[![Nginx][Nginx]][Nginx-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

Installation is easy thanks to docker compose, you just need to clone this repository then run the `up` command.

### Prerequisites

Docker Compose must be installed on your machine. It can be installed through docker desktop or [docker engine][install-docker-url]. 

### Installation

1. Clone this repo
   ```sh
   git clone https://github.com/beakerandjake/quote-hero
   ```
2. Start the application
   ```sh
   docker compose up -d
   ```

To stop the application
   ```sh
   docker compose down
   ```

### Note

Depending on your computer and internet connection it may take a while for the application to start up. The ingest process particularly may take a long time, it must download the 300mb Wikiquote dump and then load that data into Elasticsearch. The ingest process only occurs the first time you start the project. 

To check on the progress of the ingest you can run the following command once the ingest container is running:

```sh
docker logs --follow ingest
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

After the project is running navigate to `http://localhost:8080` in your browser. 

### How To Play

 1. Click the "Add Word" button to get a random word. 
 2. Now you must decide if you want to keep adding words or to use the words you have. Keep in mind you cannot delete words, once you add a word you are stuck with it.
 3. Once you are satisfied with your words you have to choose how you want to match:
    - If you are confident about your words you can click the **Match Exact** button. This will search any pages with the exact phrase formed by the words.
    - Otherwise you can click the **Match Forgiving** button, this is a more lenient search. It finds any pages which contains all of the words at least once somewhere on the page.
    - _Note_: If you only have one word you are only presented with one match button. 
4. At any time you can click the **Reset** button to clear your words and the results and start over.

The goal is to use as many words as possible to match as many pages as possible.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[product-screenshot]: https://github.com/beakerandjake/quote-master/assets/1727349/20e74852-85b6-452e-9fb6-6c0a21f22e0c
[Nginx]: https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white
[Nginx-url]: https://nginx.org
[Docker]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[Vite]: https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white
[Vite-url]: https://vitejs.dev/
[React]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://react.dev/
[TailwindCSS]: https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white
[TailwindCSS-url]: https://tailwindcss.com/
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[ElasticSearch]: https://img.shields.io/badge/-ElasticSearch-005571?style=for-the-badge&logo=elasticsearch
[ElasticSearch-url]: https://www.elastic.co/elasticsearch
[install-docker-url]: https://docs.docker.com/engine/install/
[common-words-url]: https://github.com/first20hours/google-10000-english 
[wikiquote-dump-url]: https://dumps.wikimedia.org/
