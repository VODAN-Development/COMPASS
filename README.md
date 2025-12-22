## Overview

This project demonstrates a **real-time pipeline** that converts relational healthcare data into RDF and publishes it to **AllegroGraph** using **Ontop**.

New patient visits and diagnoses are incrementally detected, converted to RDF, and added to a knowledge graph without reprocessing old data.

### Main Objective

This project is intended as a **demonstration of real-time semantic data integration**, suitable for academic coursework and healthcare knowledge graph examples.

  
## Common Data Model

* **H2 Database**
  Stores Patient, Visit, and Diagnosis tables. An `is_processed` flag is used to track new data.

* **Ontop (`mapping-dataset01.ttl`)**
  Defines R2RML mappings from the relational schema to RDF.


## ETL Integration

* **Python Script (`final_ontop.py`)**
  Periodically checks for unprocessed diagnoses, triggers Ontop materialization, uploads RDF to AllegroGraph, and marks records as processed.

* **AllegroGraph**
  Stores and serves the resulting RDF knowledge graph.

  
## Installation and setup instructions

Install prerequisites
  - Python 3.8+, OpenJDK 17, H2 JAR, Ontop CLI
Install Python packages
  - pip install jaydebeapi JPype1
Configure paths and credentials
  - Set JAVA_HOME, H2 JAR path, Ontop directory, RDF output path
  - Update AllegroGraph endpoint and credentials
Run the script


### Prerequisites and dependencies

This project depends on Python + Java, uses H2 as the relational backend, Ontop for RDF materialization, and AllegroGraph as the RDF store. All listed components must be installed and correctly configured prior to execution.


## Usage guide

1. Initialize the H2 database using the provided SQL script.
2. Start the pipeline:

   ```bash
   python final_ontop.py
   ```
3. Every 60 seconds the script:

   * Fetches diagnoses where `is_processed = FALSE`
   * Generates RDF using Ontop
   * Uploads RDF to AllegroGraph
   * Marks diagnoses as processed
4. Adding new patients or diagnoses automatically updates the knowledge graph in near real-time.


## FAQ

FAQ / Link to the Wiki


## Example

```sparql
SELECT ?patient ?visit ?diagnosis
WHERE {
  ?patient <http://mydata.example.org/hasVisit> ?visit .
  ?visit <http://mydata.example.org/hasDiagnosis> ?diagnosis .
}
LIMIT 50
```


## Contributing & issue reporting

!UPDATE THE LINKS BELOW TO FIT WITH THIS REPOSITORY.!

For reuse see the [license](https://github.com/VODAN-Development/FAIR-Data-Point/blob/main/LICENSE).
For contributing to this project see the [contributor file](https://github.com/VODAN-Development/FAIR-Data-Point/blob/main/CONTRIBUTING.md).
For issue reporting use the [issue board](https://github.com/VODAN-Development/FAIR-Data-Point/issues).
