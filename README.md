# edu-sharing to SKOS converter

This converter converts the edu-sharing topic collections developed by the Fachportalmanger\*innen to SKOS vocabularies.

If you run `python src/main.py` it will also push the vocabularies to a dedicated repository (defined in `.env`) and repeat its run every two hours.

You can also the scripts as standalone (see below)

First install requirements: `pip install -r requirements.txt`.
Then run scripts depending on what you want.

To run it with docker, first build the container then run it with `docker run --rm convertcollectiontoskos:latest`


## `convert_collection_to_skos.py`:
This will list all topics with their IDs.
You can then copy one and paste it in the command-line dialog.

## `auto_convert_collection_to_skos`:
This will take the `start_collection_id` from the `env`-file and convert all its children collections.

## Available Topics and their IDs

```json
{
  "11bdb8a0-a9f5-4028-becc-cbf8e328dd4b" : "Spanisch",
  "15dbd166-fd31-4e01-aabd-524cfa4d2783" : "Englisch",
  "15fce411-54d9-467f-8f35-61ea374a298d" : "Biologie",
  "26105802-9039-4add-bf21-07a0f89f6e70" : "Türkisch",
  "2643cff3-80bf-4848-a132-19244ffe9c30" : "Informatik (alt!)",
  "26a336bf-51c8-4b91-9a6c-f1cf67fd4ae4" : "Deutsch als Zweitsprache",
  "324f24e3-6687-4e89-b8dd-2bd0e20ff733" : "Geschichte",
  "4940d5da-9b21-4ec0-8824-d16e0409e629" : "Chemie",
  "5e40e372-735c-4b17-bbf7-e827a5702b57" : "Main-Collection (All)",
  "66c667bc-8777-4c57-b476-35f54ce9ff5d" : "Religion",
  "69f9ff64-93da-4d68-b849-ebdf9fbdcc77" : "Deutsch",
  "6a3f5881-cce0-4e8d-b123-26392b3f1c19" : "Kunst",
  "742d8c87-e5a3-4658-86f9-419c2cea6574" : "Informatik",
  "7998f334-9311-491e-9a58-72baf2a7efd2" : "Darstellendes Spiel",
  "94f22c9b-0d3a-4c1c-8987-4c8e83f3a92e" : "Physik",
  "a87c092d-e3b5-43ef-81db-757ab1967646" : "Open Educational Resources (OER)",
  "bd8be6d5-0fbe-4534-a4b3-773154ba6abc" : "Mathematik",
  "d0ed50e6-a49f-4566-8f3b-c545cdf75067" : "Nachhaltigkeit",
  "ea776a48-b3f4-446c-b871-19f84b31d280" : "Sport",
  "eef047a3-58ba-419c-ab7d-3d0cfd04bb4e" : "Medienbildung",
  "ffd298b5-3a04-4d13-9d26-ddd5d3b5cedc" : "Politische Bildung",
}
```
