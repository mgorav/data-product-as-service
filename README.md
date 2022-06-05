# Smart Analytics

Every body talks about Data engineering is software problem. That's ture. In the world of software, application are 
built using APIs first approach, that is, micro-services  based architecture combined with micro-front end architecture.
Micro-frontends are intended to bring the same benefits of microservices to the UI layer. By breaking up a complex 
system into smaller, more manageable pieces, teams can rapidly develop and release new features and functionality with
agility & end to end automation - software excellence. This style of application development is referred to as
[12-factor-app](https://12factor.net)

Micro-frontends architecture really shine in project with many of developers working together in a large business domain 
and with a goal to reduce the complexity by dividing into multiple subdomains, independently deploy different parts of 
the applications without creating communication and coordination overhead across teams. 

> _micro-service + micro-frontend = agility & end to automation = simplicity_


The analytics is all about finding answers to a question using data, also called **_data product with interactive 
visualization_**. Multiple team make data product and visualization teams using this data product provides visualization.
This visualization provides insight into the business.

Visualization is at the heart of data analysis. The engineers of data visualization applications are choosing 
between two options:

- No-code BI visualization tools, with a drag-n-drop interface and some possible extensions for customization, e.g. Tableau
- Web frameworks with rich visualization capabilities in high-level programming languages, such as JS, Python etc

We are living in the world of interactive visualization, with the rise of framework like Dash and Streamlit, building 
visualization using Python (programing language of choice for the data teams), is becoming very attractive option.


> So analytics world is on the same cross-roads as application team were.

How can we make analytics development simpler, automated and thereby empowering the engineering teams.

> Hold on: Isn't it micro-services + micro-front architecture provide this.

The question arises, how can we convert data product as a service, so that micro-frontends can be build. These 
micro-front can be:
- traditional, eg tableau, powerBI
- modern UI, eg reactJS, Streamlit 

This blog demonstrates, Data Product As Service using Databricks SQL endpoint and analytics visualization using 
Streamlit


Sections
=================

 * [Architecture](#Architecture)
 * [Prerequisites](#Prerequisites)
 * [Demo](#Demo)
 * [Setup](#Setup)
 * [References](#References)


## Architecture

Following picture shows the reference architecture for building analytics using micro-services + micro-frontend 
architecture - *_termed as "Smart Analytics"_*

![Architecture](architecture/archicture.png)

The above architecture is composed of the following:

- **_Data Product_**
  
  A "Data Product" typical lives in a data lake/lakehouse and storge is typically
  object storage (AWS - S3 bucket). In Databricks, it's stored as Delta table on 
  delta lake.
  ![DeltaLake](architecture/lakehouse.png)

- **_Data Product As Service_**
  
  This demonstration uses Deltalake/Databricks extensively, as result, making data product **_as a service_**, is achieved using 
  Databricks SQL Endpoint. Wrapping Data Product As Service, helps in providing horizontal
  concerns like authentication (e.g. OAUTH/OKTA), authorization (e.g. Ranger)
  ![Data Product As Service](architecture/DataProductAsService.png)
  Databricks provide ability to access data product using SQL endpoint, agnostic of the underlying protocol, as shown 
  in the configuration below:
  ![SQLEndpoint](architecture/sqlendpoint_config.png)
  Further, using SQL Endpoint, it's possible on one hand possible to connect with traditional visualization tools like 
  Tableau, PowerBI, Arcion, Fivetran, Infoworks, Qlik, Rivery, Stitch, StreamSets, Syncsort etc or custom UI using 
  Streamlit or Dash

- **_Micro-frontend_**
  The final component of the reference architecture - visualization using **_"micro-frontend architecture"_**. This in 
  simple terminology means injecting traditional visualization and custom-built UI in the browser, as shown below:
  ![Visualization](architecture/micro_frontend.png)

> What is Micro Frontend?
> - developing frontend using micro-services architecture principles
> - think micro-frontend application as composition of different capabilities (cross functional teams)
> - domain driven design development in action
> ![MicroFrontEnd](architecture/micro_frontend_1.png)



## Prerequisites

- Databricks SQL endpoint
  The demo using New York yellow taxi data
- Free Mapbox token  - accessible token [here](https://www.mapbox.com/)
- Locally: Docker, Makefile

## Demo

![Demo](demo/SmartAnalyticsAppDatabricks.gif)

> NOTE: Use [mp4](https://github.com/mgorav/data-product-as-service/blob/main/SmartAnalyticsApp.mp4) demo for better visual experience

## Setup 

1. Create or start an existing DBX SQL endpoint in the workspace
2. Create a query and define the database and table (Data Product):

```sql
CREATE DATABASE IF NOT EXISTS streamlit_demo_db;
CREATE TABLE IF NOT EXISTS streamlit_demo_db.nyctaxi_yellow 
USING DELTA
LOCATION "dbfs:/databricks-datasets/nyctaxi/tables/nyctaxi_yellow";
```

3. Change`.env` file as per your configuration 
4. On local machine, launch `make docker-run` to launch the server
5. Open http://localhost:9999 and it's time to play :) 

## References

- [Databricks SQL](https://databricks.com/product/databricks-sql)
- [Streamlit](https://streamlit.io/)
- [Mapbox](https://www.mapbox.com/)
- [NYC Taxi Dataset](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Markdown TOC](https://github.com/ekalinin/github-markdown-toc)