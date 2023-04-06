# CMPT733-Airbnb-Project

> Tentative Project Title: 
> Insights for New Airbnb Hosts: A Data-Driven Analysis of Toronto's Airbnb Dataset

Members: Guanghua Yang, Jianan Li, Kewei Li, Ningyi Ke, Wenbin Li

<br>

## Files

 - `Descriptive Analysis.ipynb` : Q1 Part 1

 - `Q1 part 2.ipynb`: Q1 Part 2

 - ` `

 - ` `


<br>

## Current Project Design

**Q1: In general what are the statistics that a new Airbnb host should know? - Freya & Kelvin**

*(Part 1 - Descriptive Analysis) - Freya*
 
- Which areas and room types are more popular?
    - Map heatmap: room rates, availability
    - Room type vs popularity mapping

- What is the distribution of prices in different regions and room types?

     - Distribution subplot of prices

- Is public transit needed to be considered for popular areas?
     - Analyze geographical distribution of Airbnb in popular regions
     - Distribution of transits that largely affect Airbnb in popular regions 


*(Part 2 - Research Questions) - Kelvin*

- Are there any Airbnb renters who are always writing bad reviews? (done)

    - Using detailed review data to do sentiment analysis

- Optional: Comparison of the ratio of positive/bad reviews in different regions

- Optional: What is the growth rate of Airbnb hosts in the past 4 quarters?

- The language usage distribution of airbnb users? (done)

<br><br>

**Q2: Has the accommodation preference of Airbnb renters changed on a time scale? - Stella**

*Note: The data can be based on a non-detail review data, and listing data JOIN to get location and room type information*

 - Seasonality: Is there a season where a certain type of Airbnb is particularly popular?

 - Airbnb development: whether there is a certain room type/area that renters increasingly disfavour or increasingly favour as real estate development and people's preferences have changed in the last decade 

(e.g. xx neighbourhoods were popular around 2015, but have become less popular since then)

<br><br>

**Q3: What factors influence Airbnb pricing? - Gavin & Lexi**

*Note: Because the model is for new Airbnb hosts, it should not contain information such as review score, availability, etc. It needs to start from the property itself (location, neighbourhood, etc.)*

 - Online deployment of trained pricing model

 - Feature importance

 - Model interpretation: Why that price / How can the price be improved 
 
    - Shapley

