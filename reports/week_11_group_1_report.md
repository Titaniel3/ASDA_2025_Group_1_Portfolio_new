#  Spotify 5000 songs Dataset Analysis Project Report 

## 0. Authors of the report

| Name | Contribution |
|------|--------------|
| Shreyas Krishnamurthy     |  |
| Daniel Lichtmannecker     |  Creating the Spotify playlists, creating the report |
|  Tobias Demming    |   Performing the clustering analysis |
| Ranjit Singh     | Performing the clustering analysis |

## 1. Dataset Overview

Numbers refer to the final version of the dataset used for creating the playlists on Spotify.

| Item                | Description                                                                                                                                                                   |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Number of rows      | 5235                                                                                                                                                                         |
| Number of columns   |  75                                                                                                                                                                         |
| Format file (.csv, .txt, etc) | .csv                                                                                                                                                                        |
| Creator of the dataset | Same as the authors of the report                                                                                                                                             |
| Source (name)       | spotify_playlist_for_class.csv                                                                                                                                                                |
| Source (link)       | [Final Dataset](../datasets/spotify_playlists_for_class.csv) 
| Date/Time | 12.01.2026/ 11.20 am       

## 2. Dataset Structure & Descriptive Statistics

| Column          | Data type | Number of unique values | Example values |
|-----------------|-----------|-------------------------|----------------|
| name            | object    | 5011                    | Ravel: Boléro, M 81                                                                                                              |
| artist          | object    | 2176                    | Maurice Ravel                                   
| html            | object    | 5171                    | https://open.spotify.com/track/3HoO8VUfyXwkgqwaIrVM7u |
| dbscan_cluster  | int64     | 5                       | 1, 0, 3 |
| playlist_name   | object    | 4                       | Feel Good Pop, High Energy Hits, Late Night Moods |


## 3. Cluster Analysis

For clusterin the songs in different playlists we used two different approaches. First, we used K-Means Clustering and later a DBSCAN clustering.

### 3.1. K-Means Clustering

With this method, we received seven different clusters, which differed for the musical variables. The differences between clusters are more striking for some variables (f.e. "energy") than for other variables (f.e. "tempo"). 